import pandas as pd
import numpy as np
import os
import glob

# Base paths
demand_csv_path = "data/demand.csv"
demand_xlsx_path = "datasets/demand_calibrate/demand_calibrate_1_00_PM.xlsx"
demand_folder = "/home/sbachira/llm_od/datasets/demand"

# Load demand.csv
df_csv = pd.read_csv(demand_csv_path, index_col=0)
matrix_csv = df_csv.values
csv_min, csv_max = np.min(matrix_csv), np.max(matrix_csv)
print(f"demand.csv: min={csv_min}, max={csv_max}")

# Load demand_calibrate Excel file
df_xlsx = pd.read_excel(demand_xlsx_path, index_col=0)
matrix_xlsx = df_xlsx.values
xlsx_min, xlsx_max = np.min(matrix_xlsx), np.max(matrix_xlsx)
print(f"demand_calibrate_1_00_PM.xlsx: min={xlsx_min}, max={xlsx_max}")

# Now process all .csv files in datasets/demand/
csv_files = glob.glob(os.path.join(demand_folder, "*.csv"))

for file_path in csv_files:
    df = pd.read_csv(file_path, index_col=0)
    matrix = df.values
    file_min, file_max = np.min(matrix), np.max(matrix)
    file_name = os.path.basename(file_path)
    print(f"{file_name}: min={file_min}, max={file_max}")
