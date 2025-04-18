import os
import pandas as pd

# read the baseline OD matrix
df_baseline = pd.read_csv("data/demand.csv", index_col=0)

# define time-of-day scale factors from llm logs
hourly_scale_factors = {
    "5:00 AM": 0.020,
    "6:00 AM": 0.030,
    "7:00 AM": 0.068,
    "8:00 AM": 0.076,
    "9:00 AM": 0.060,
    "10:00 AM": 0.050,
    "11:00 AM": 0.050,
    "12:00 PM": 0.058,
    "1:00 PM": 0.058,
    "2:00 PM": 0.050,
    "3:00 PM": 0.050,
    "4:00 PM": 0.068,
    "5:00 PM": 0.086,
    "6:00 PM": 0.078,
    "7:00 PM": 0.058,
    "8:00 PM": 0.050,
    "9:00 PM": 0.040,
    "10:00 PM": 0.030,
    "11:00 PM": 0.020
}

# for each timeslot, multiply the baseline matrix by the factor and save
output_folder = "datasets/demand"
if not os.path.exists(output_folder):
    os.makedirs(output_folder, exist_ok=True)

for timeslot, factor in hourly_scale_factors.items():
    df_scaled = df_baseline * factor
    output_path = os.path.join(output_folder, f"demand_{timeslot}.csv")
    df_scaled.to_csv(output_path)

print("Hourly scaled OD matrices have been saved.")