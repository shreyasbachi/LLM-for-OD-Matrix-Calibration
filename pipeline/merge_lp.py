# merging gt data from link_performance_{timestamp} files into link_performance.csv as columns

import os
import glob
import pandas as pd

# where main link_performance.csv exists
DATA_DIR = "data"                                      
MASTER_FILE = os.path.join(DATA_DIR, "link_performance.csv")
# folder containing link_performance_<TS>.csv
TS_DIR = "datasets/link_performance" 

def main():
    # 1) load the master link_performance.csv in-place
    master = pd.read_csv(MASTER_FILE, dtype={"link_id": str})

    # 2) for each timestamped file, merge its obs_count
    pattern = os.path.join(TS_DIR, "link_performance_*.csv")
    for ts_path in sorted(glob.glob(pattern)):
        ts_name = os.path.basename(ts_path)
        # extract the timestamp key
        ts = ts_name.replace("link_performance_", "").replace(".csv", "")

        # read only link_id + obs_count from the timestamped file
        df_ts = pd.read_csv(
            ts_path,
            usecols=["link_id", "obs_count"],
            dtype={"link_id": str}
        )

        # rename its obs_count column to obs_count_<ts>
        new_col = f"obs_count_{ts}"
        df_ts = df_ts.rename(columns={"obs_count": new_col})

        # merge into master (left join keeps all master rows)
        master = master.merge(df_ts, on="link_id", how="left")
        print(f"Merged {new_col} from {ts_path}")

    # 3) overwrite the original link_performance.csv with the augmented frame
    master.to_csv(MASTER_FILE, index=False)
    print(f"Updated in-place: {MASTER_FILE}")

if __name__ == "__main__":
    main()