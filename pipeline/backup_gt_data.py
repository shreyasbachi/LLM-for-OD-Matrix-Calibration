# read all link_performance_{timestamp} files and save as .json

"""
Script to extract link_id and obs_count columns from each
link_performance_{timestamp}.csv in datasets/link_performance,
and write them to a single JSON backup file.
"""
import os
import glob
import pandas as pd
import json

# Directory containing the timestamped CSVs
INPUT_DIR = "datasets/link_performance"
# Output JSON file
OUTPUT_FILE = "data/ground_truth_obs_count.json"

backup = {}

# Find all CSV files matching the pattern
pattern = os.path.join(INPUT_DIR, "link_performance_*.csv")
for filepath in glob.glob(pattern):
    filename = os.path.basename(filepath)
    # Extract timestamp from filename
    timestamp = filename.replace("link_performance_", "").replace(".csv", "")

    # Read CSV, strip extra spaces
    df = pd.read_csv(filepath, skipinitialspace=True)
    df.columns = df.columns.str.strip()

    # Ensure required columns exist
    if "link_id" not in df.columns or "obs_count" not in df.columns:
        print(f"Warning: Missing 'link_id' or 'obs_count' in {filename}, skipping.")
        continue

    # Build list of entries: link_id + obs_count
    entries = []
    for _, row in df.iterrows():
        entry = {
            "link_id": str(row["link_id"]),
            "obs_count": row["obs_count"]
        }
        entries.append(entry)

    # Store under its timestamp key
    backup[timestamp] = entries

# Write out to JSON
with open(OUTPUT_FILE, "w") as f:
    json.dump(backup, f, indent=2)

print(f"Wrote ground truth backup to {OUTPUT_FILE}")