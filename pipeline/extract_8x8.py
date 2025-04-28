#!/usr/bin/env python3
import os
import pandas as pd
import numpy as np

full_demand_path = "data/demand.csv"
zone_subset = [623, 624, 625, 626, 627, 650, 651, 2061]
out_folder = "datasets/demand_8x8"
out_path = os.path.join(out_folder, "demand_8x8.csv")

# Load full OD matrix
df_full = pd.read_csv(full_demand_path, index_col=0)
# ensure zone IDs are ints (or castable)
df_full.index = df_full.index.astype(int)
df_full.columns = df_full.columns.astype(int)
df8 = df_full.loc[zone_subset, zone_subset].copy()

np.fill_diagonal(df8.values, 0.0)
os.makedirs(out_folder, exist_ok=True)
df8.to_csv(out_path)

print(f"8×8 OD matrix saved to {out_path}")

baseline_path = "datasets/demand_8x8/demand_8x8.csv"
output_folder = "datasets/demand_8x8"
os.makedirs(output_folder, exist_ok=True)

# 2. Timeslot factors
hourly_scale_factors = {
    "5:00 AM": 0.020,
    "6:00 AM": 0.030,
    "7:00 AM": 0.068,
    "8:00 AM": 0.076,
    "9:00 AM": 0.060,
    "10:00 AM":0.050,
    "11:00 AM":0.050,
    "12:00 PM":0.058,
    "1:00 PM": 0.058,
    "2:00 PM": 0.050,
    "3:00 PM": 0.050,
    "4:00 PM": 0.068,
    "5:00 PM": 0.086,
    "6:00 PM": 0.078,
    "7:00 PM": 0.058,
    "8:00 PM": 0.050,
    "9:00 PM": 0.040,
    "10:00 PM":0.030,
    "11:00 PM":0.020
}

# load baseline 8×8
df_base = pd.read_csv(baseline_path, index_col=0)

# scale & save
for timeslot, factor in hourly_scale_factors.items():
    df_scaled = df_base * factor
    # we'll embed the timeslot in the filename:
    filename  = f"demand_8x8_{timeslot}.csv"
    path      = os.path.join(output_folder, filename)
    df_scaled.to_csv(path)
    print(f"Saved scaled OD for {timeslot} to {path}")

print("All hourly 8×8 OD matrices generated.")
