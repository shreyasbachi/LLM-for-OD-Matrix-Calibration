import pandas as pd
import ast
import os

mapping_path    = 'data/od_links_mapping.csv'
link_perf_path  = 'data/link_performance_odlink.csv'
demand_path     = 'data/demand.csv'
output_path     = 'data/link_performance_odlink.csv'

# Load the OD links mapping
mapping_df = pd.read_csv(mapping_path)

# Build link_od_map: link_id -> list of (o_zone, d_zone)
link_od_map = {}
for _, row in mapping_df.iterrows():
    o_zone = row['o_zone_id']
    d_zone = row['d_zone_id']
    # parse the links column
    try:
        links = ast.literal_eval(row['links'])
    except Exception:
        links = [l.strip() for l in row['links'].strip("[]").split(',') if l.strip()]
    for link in links:
        lid = str(link)
        link_od_map.setdefault(lid, []).append((int(o_zone), int(d_zone)))

# load demand.csv and extract its zone labels
demand_df = pd.read_csv(demand_path, index_col=0)
# demand_df.index are origin zone IDs
# demand_df.columns are destination zone IDs
zone_rows = [str(z) for z in demand_df.index]
zone_cols = [str(z) for z in demand_df.columns]

# Build link_idx_map: link_id -> list of (i, j) matrix indices
link_idx_map = {}
for lid, zone_pairs in link_od_map.items():
    idx_set = set()
    for (oz, dz) in zone_pairs:
        oz_s = str(oz)
        dz_s = str(dz)
        if oz_s in zone_rows and dz_s in zone_cols:
            i = zone_rows.index(oz_s)
            j = zone_cols.index(dz_s)
            idx_set.add((i, j))
        else:
            print(f"Warning: zone pair ({oz},{dz}) not found in demand.csv")
    link_idx_map[lid] = sorted(idx_set)

link_perf_df = pd.read_csv(link_perf_path, dtype={'link_id': str})
link_perf_df['od_pairs']       = ""   # will hold "(i,j),(i2,j2),..."
link_perf_df['od_zone_pairs']  = ""   # will hold "(oz,dz),(oz2,dz2),..."

# helpers to format lists of tuples
def fmt_idx(pairs):
    return ",".join(f"({i},{j})" for i,j in pairs)

def fmt_zone(pairs):
    return ",".join(f"({oz},{dz})" for oz,dz in pairs)

# Fill in both columns
for idx, row in link_perf_df.iterrows():
    lid = row['link_id']
    # get new index pairs and zone pairs (or empty lists)
    idx_pairs  = link_idx_map.get(lid, [])
    zone_pairs = link_od_map.get(lid, [])
    link_perf_df.at[idx, 'od_pairs']       = fmt_idx(idx_pairs)
    link_perf_df.at[idx, 'od_zone_pairs']  = fmt_zone(zone_pairs)

# Save your updated file
if os.path.exists(output_path):
    os.remove(output_path)
link_perf_df.to_csv(output_path, index=False)
print("link_performance_odlink_updated.csv written successfully.")
