"""Chronological transfer check with public modeled and measured wind power."""

import argparse
import csv
import hashlib
import io
import json
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import urlopen
from zipfile import ZipFile

import numpy as np
from scipy.io import netcdf_file

from check_face_residuals import compare, DELTA
from censored_newsvendor.coalition_audit import exact_excess, forecast_rule
from censored_newsvendor.face_residuals import empirical_law


ROOT = Path(__file__).resolve().parents[1]
SOURCES = ROOT / "configs/residual_wind_sources.json"


def verified_file(cache, name, spec):
    cache.mkdir(parents=True, exist_ok=True)
    path = cache / name
    def check(data):
        if len(data) != spec["bytes"]:
            raise ValueError(f"Wrong size for {name}")
        digest = hashlib.sha256(data).hexdigest()
        if "sha256" in spec and digest != spec["sha256"]:
            raise ValueError(f"Unexpected SHA-256 for {name}")
        if "git_blob" in spec:
            header = b"blob " + str(len(data)).encode() + b"\0"
            if hashlib.sha1(header + data).hexdigest() != spec["git_blob"]:
                raise ValueError(f"Unexpected Git blob for {name}")
        return digest
    if path.exists():
        return path, check(path.read_bytes())
    with urlopen(spec["url"], timeout=45) as response:
        data = response.read()
    digest = check(data)
    with tempfile.NamedTemporaryFile(dir=cache, delete=False) as tmp:
        temp_path = Path(tmp.name)
        try:
            tmp.write(data)
        except BaseException:
            temp_path.unlink(missing_ok=True)
            raise
    os.replace(temp_path, path)
    return path, digest


def epoch(year):
    return int(datetime(year, 1, 1, tzinfo=timezone.utc).timestamp())


def texas(cache, sources):
    start, end = epoch(2007), epoch(2009)
    sites = sources["texas_sites"]
    columns, hashes = [], {}
    for site in sites:
        path, sha = verified_file(cache, str(site["site_id"]) + ".nc", site)
        hashes[path.name] = sha
        with netcdf_file(path, mmap=False) as dataset:
            origin = int(dataset.start_time)
            if int(dataset.sample_period) != 300 or (start - origin) % 300:
                raise ValueError("Unexpected WIND Toolkit time grid")
            begin, finish = (start - origin) // 300, (end - origin) // 300
            if begin < 0:
                raise ValueError("Missing initial five-minute timestamp")
            power = dataset.variables["power"][begin:finish].astype(float).copy()
        if len(power) != (end - start) // 300 or not np.isfinite(power).all():
            raise ValueError("Incomplete WIND Toolkit source")
        if power.min() < 0 or power.max() > site["capacity_mw"] + .001:
            raise ValueError("Invalid WIND Toolkit production")
        columns.append(power.reshape(-1, 12).mean(axis=1))
    times = np.arange(start, end, 3600).astype("datetime64[s]")
    panel = np.stack(columns, axis=1)
    rated = np.array([site["capacity_mw"] + .001 for site in sites])
    return times, panel, rated, {"source_sha256": hashes, "hours": len(panel),
                                "sites": [site["site_id"] for site in sites], "unit": "MW",
                                "type": "modeled WIND Toolkit production"}


def france(cache, sources):
    spec = sources["france"]
    path, digest = verified_file(cache, "la_haute_borne.zip", spec)
    start, end = epoch(2014), epoch(2016)
    slots = (end - start) // 600
    data, seen = {}, {}
    counts = dict(rows=0, outside_window=0, duplicates=0, nonfinite=0, clipped_below=0, clipped_above=0)
    with ZipFile(path) as archive, archive.open("la-haute-borne-data-2014-2015.csv") as f:
        for row in csv.DictReader(io.TextIOWrapper(f, encoding="utf-8-sig")):
            counts["rows"] += 1
            time = datetime.fromisoformat(row["Date_time"])
            if time.tzinfo is None:
                raise ValueError("SCADA timestamp lacks UTC offset")
            seconds = int(time.timestamp()) - start
            if seconds < 0 or seconds >= end - start:
                counts["outside_window"] += 1
                continue
            if seconds % 600:
                raise ValueError("Unexpected ten-minute timestamp")
            pos = seconds // 600
            turbine = row["Wind_turbine_name"]
            if turbine not in data:
                data[turbine] = np.full(slots, np.nan)
                seen[turbine] = np.zeros(slots, dtype=bool)
            if seen[turbine][pos]:
                counts["duplicates"] += 1
                continue
            seen[turbine][pos] = True
            value = float(row["P_avg"]) if row["P_avg"].strip() else np.nan
            if not np.isfinite(value):
                counts["nonfinite"] += 1
                continue
            counts["clipped_below"] += int(value < 0)
            counts["clipped_above"] += int(value > 2050)
            data[turbine][pos] = min(2050., max(0., value)) / 1000
    ids = sorted(data)
    if len(ids) != 4:
        raise ValueError(f"Expected four turbines, saw {ids}")
    readings = np.stack([data[t] for t in ids], axis=1).reshape(-1, 6, 4)
    complete = np.isfinite(readings).all(axis=(1, 2))
    panel = readings[complete].mean(axis=1)
    times = np.arange(start, end, 3600).astype("datetime64[s]")[complete]
    counts["absent_turbine_slots"] = sum(int((~s).sum()) for s in seen.values())
    return times, panel, np.full(4, 2.05), {"source_sha256": {path.name: digest},
        "unit": "MW", "turbines": ids, "type": "ENGIE measured SCADA, bounded export",
        "hours": len(panel), "discarded_incomplete_hours": int((~complete).sum()), "processing_counts": counts}


def run_panel(name, years, prepared):
    time, y, rated, provenance = prepared
    months = time.astype("datetime64[M]").astype(int)
    provenance["hourly_panel_sha256"] = hashlib.sha256(
        time.astype("<i8").tobytes() + np.asarray(y, dtype="<f8").tobytes()).hexdigest()
    runs = []
    for year in years:
        calendar = 1970 + months // 12 == year
        masks = [calendar & ((months % 12) // 3 == k) for k in range(4)]
        training, pilot, validation, followup = [y[mask] for mask in masks]
        if min(map(len, [training, pilot, validation, followup])) < 2:
            raise ValueError("Insufficient chronological block")
        forecast = empirical_law(training)
        rule = forecast_rule(forecast, rated)
        result, _ = compare(rule, forecast, pilot, validation, DELTA)
        external = exact_excess(rule, empirical_law(followup))
        runs.append({"year": year, "quarters": [{"hours": int(mask.sum()), "first_utc": str(time[mask][0]),
                     "last_utc": str(time[mask][-1])} for mask in masks],
                     "offer_mw": rule.offer, "weights": rule.weights.tolist(), "maximum_loss": rule.loss_range,
                     "audit": result, "future_empirical": external,
                     "future_inside_primary_interval": bool(result["primary"]["lower"] - 1e-9 <= external["excess"] <=
                                                           result["primary"]["upper"] + 1e-9)})
    return {"panel": name, "provenance": provenance, "years": runs}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cache", required=True, type=Path)
    args = parser.parse_args()
    sources = json.loads(SOURCES.read_text())
    panels = [run_panel("Texas modeled", [2007, 2008], texas(args.cache, sources)),
              run_panel("France measured", [2014, 2015], france(args.cache, sources))]
    files = ["scripts/check_wind_residuals.py", "scripts/check_face_residuals.py",
             "src/censored_newsvendor/face_residuals.py", "src/censored_newsvendor/coalition_audit.py",
             "configs/residual_wind_sources.json", "docs/residual_protocol.md"]
    payload = {"scope": "Chronological transfer. Intervals on these time series are descriptive.",
               "sha256": {f: hashlib.sha256((ROOT / f).read_bytes()).hexdigest() for f in files},
               "panels": panels}
    out = ROOT / "results/residuals"
    out.mkdir(parents=True, exist_ok=True)
    p = out / "wind.json"
    p.write_text(json.dumps(payload, indent=2, allow_nan=False) + "\n")
    saved = json.loads(p.read_text())["panels"]
    lines = ["# Chronological wind check", "", "Unit imbalance penalty; all values are expressed in MW-equivalent cost units.",
             "The January–March rule is frozen. Audit prices use April–June, validation uses July–September, and the empirical reference uses October–December.",
             "", "| Panel | Year | Lower | Face upper | Original moment, pilot+validation | Exhaustive, pilot+validation | Future maximum excess | Future within interval |",
             "| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |"]
    for panel in saved:
        for year in panel["years"]:
            v = year["audit"]
            lines.append(f"| {panel['panel']} | {year['year']} | {v['primary']['lower']:.5g} | {v['primary']['upper']:.5g} | "
                         f"{v['upper']['forecast_grand_full']:.5g} | {v['upper']['enumeration_full']:.5g} | "
                         f"{year['future_empirical']['excess']:.5g} | {year['future_inside_primary_interval']} |")
    for panel in saved:
        lines += ["", f"{panel['panel']} retained {panel['provenance']['hours']} joint hours."]
    lines += ["", "ENGIE SCADA is transformed to bounded export. The WIND Toolkit panel is modeled production.",
              "Each future maximum is an empirical optimum on its own quarter. The four comparisons have temporal dependence and seasonal shifts.", ""]
    md = "\n".join(lines)
    (out / "wind.md").write_text(md)
    print(md)


if __name__ == "__main__":
    main()

