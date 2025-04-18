# converts the od matrix in demand.csv to demand_calibrate.xlsm

import re
from pathlib import Path
import pandas as pd

#  CONFIGURATION
SRC_DIR  = Path("datasets/demand")          
DEST_DIR = Path("datasets/demand_calibrate")
DEST_DIR.mkdir(exist_ok=True)

#  HELPERS
def wide_to_long(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert a wide OD matrix (origins as index, destinations as columns)
    into long form [o_zone_id, d_zone_id, volume], keeping zeros.
    """
    long_df = (
        df
        .reset_index()  # origin IDs become a column
        .melt(
            id_vars=df.index.name or "index",
            var_name="d_zone_id",
            value_name="volume"
        )
        .rename(columns={df.index.name or "index": "o_zone_id"})
        .astype({"o_zone_id": int, "d_zone_id": int, "volume": float})
        .sort_values(["o_zone_id", "d_zone_id"])
        .reset_index(drop=True)
    )
    return long_df

def sanitize_sheet_name(name: str) -> str:
    """
    Excel sheet titles must be ≤31 chars and may not contain:
      : \\ / ? * [ ]
    Replace them with '_' and truncate to 31 chars.
    """
    cleaned = re.sub(r'[:\\/\?\*\[\]]', '_', name)
    return cleaned[:31]

def sanitize_filename(name: str) -> str:
    """
    Filenames on most file systems may not contain colon, slash, or spaces.
    Replace any non-[A-Za-z0-9_-] with '_'.
    """
    return re.sub(r'[^A-Za-z0-9_-]', '_', name)

def ensure_numeric_index_cols(df: pd.DataFrame, fname: str) -> None:
    """
    Force index & columns to ints, or raise on failure.
    """
    try:
        df.index   = pd.to_numeric(df.index,   errors="raise").astype(int)
        df.columns = pd.to_numeric(df.columns, errors="raise").astype(int)
    except ValueError:
        raise ValueError(f"{fname}: first row & column must be numeric zone IDs")


#  MAIN
for csv_path in SRC_DIR.glob("demand_*.csv"):
    # derive timestamp from filename:
    timestamp_raw = csv_path.stem.split("_", 1)[1]

    # sheet names need one kind of sanitization
    sheet_name = sanitize_sheet_name(timestamp_raw)
    safe_stamp = sanitize_filename(timestamp_raw)
    out_path = DEST_DIR / f"demand_calibrate_{safe_stamp}.xlsx"

    df_wide = pd.read_csv(csv_path, index_col=0)

    # 2. ensure numeric zone IDs
    ensure_numeric_index_cols(df_wide, csv_path.name)

    # 3. pivot to long form
    df_long = wide_to_long(df_wide)

    # 4. write out .xlsm, single sheet named after the sanitized timestamp
    with pd.ExcelWriter(out_path, engine="openpyxl") as writer:
        df_long.to_excel(writer, sheet_name=sheet_name, index=False)

    print(f"Wrote {out_path.name}  —  sheet “{sheet_name}”  ({len(df_long):,} rows)")

print("✅ All files generated without invalid characters in names.")
