#!/usr/bin/env python3
"""
For each demand_calibrate_<timestamp>.xlsx in datasets/demand_calibrate/:
 1. Load the calibrated OD matrix (using extrac_column_info).
 2. Overwrite data_path/demand.csv with it.
 3. Run the simulation executable.
 4. Copy the baseline link_performance.csv (unchanged) into datasets/link_performance/ as link_performance_<timestamp>.csv.
 5. In that copy, overwrite each row’s obs_count with its volume as ground truth.
"""

import os
import json
import re
import subprocess
import timeit
import shutil
from pathlib import Path
import pandas as pd
from dotenv import load_dotenv
from utils import extrac_column_info

#  ENV & CONFIG
load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parent.parent
with open(PROJECT_ROOT / "config" / "config.json") as f:
    config = json.load(f)

exe_path = Path(PROJECT_ROOT) / config["paths"]["exe_path"]
data_path = Path(PROJECT_ROOT) / config["paths"]["data_path"]
baseline_lp_csv = Path(PROJECT_ROOT) / config["paths"]["link_performance"]

# where to drop  new per‑timestep link_performance files:
datasets_dir = Path(PROJECT_ROOT) / config["paths"]["datasets_dir"]
calibrate_dir = datasets_dir / "demand_calibrate"
out_lp_dir = datasets_dir / "link_performance"
out_lp_dir.mkdir(exist_ok=True)


def sanitize_timestamp(name: str) -> str:
    """Make a safe stamp for filenames: letters, digits, underscore, hyphen."""
    return re.sub(r"[^A-Za-z0-9_-]", "_", name)

def run_one_simulation(cal_file: Path):
    timestamp_raw = cal_file.stem.split("demand_calibrate_", 1)[1]
    safe_stamp    = sanitize_timestamp(timestamp_raw)
    print(f"\n=== Simulating for {timestamp_raw} ===")

    # 1. load the calibrated demand & overwrite demand.csv
    df_cal = extrac_column_info(str(cal_file))
    (data_path / "demand.csv").write_text("")
    df_cal.to_csv(data_path / "demand.csv", index=True)

    # 2. run the simulation
    start_sim = timeit.default_timer()
    subprocess.run(["wine64", str(exe_path)], cwd=data_path, check=True)
    sim_time = timeit.default_timer() - start_sim
    print(f"Simulation time: {sim_time:.2f}s")

    # 3. copy baseline link_performance into your timestamped output folder
    dest_lp = out_lp_dir / f"link_performance_{safe_stamp}.csv"
    shutil.copy(baseline_lp_csv, dest_lp)
    print(f"Copied baseline → {dest_lp.name}")

    # 4. overwrite obs_count in that copy with its own volume
    df_lp = pd.read_csv(dest_lp)
    df_lp["obs_count"] = df_lp["volume"]
    df_lp.to_csv(dest_lp, index=False)
    print(f"Updated obs_count from volume in {dest_lp.name}")

    # no return needed any more

#  MAIN LOOP
if __name__ == "__main__":
    pattern = "demand_calibrate_*.xls*"
    files = sorted(calibrate_dir.glob(pattern))
    if not files:
        raise FileNotFoundError(f"No files found in {calibrate_dir} matching {pattern}")

    for cal in files:
        run_one_simulation(cal)

    print("\nAll simulations complete. New link_performance files are in:")
    print(f"{out_lp_dir}")
