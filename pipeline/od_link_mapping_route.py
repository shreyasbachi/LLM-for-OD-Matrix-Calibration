# od link mappings from route_assignment.csv

import pandas as pd
import os
import ast

route_assignment = pd.read_csv('data/route_assignment.csv')
output_path = 'data/od_links_mapping.csv'
# Create a dictionary to collect links for each (o_zone_id, d_zone_id)
od_links_dict = {}

# Iterate through each row
for idx, row in route_assignment.iterrows():
    o_zone = row['o_zone_id']
    d_zone = row['d_zone_id']
    link_sequence = str(row['link_sequence'])
    
    # Skip if link_sequence is missing or NaN
    if link_sequence.lower() == 'nan':
        continue
    
    # Split link sequence into a list (semicolon-separated)
    links = link_sequence.strip().split(';')

    # Remove empty strings if any (because the line ends with ';')
    links = [link for link in links if link]

    # Create a key for origin-destination pair
    od_pair = (o_zone, d_zone)

    # Initialize the set if first time seeing this OD pair
    if od_pair not in od_links_dict:
        od_links_dict[od_pair] = set()

    # Add all links for this path into the OD pair set
    for link_id in links:
        od_links_dict[od_pair].add(link_id.strip())  # Keep as string

# Step 4: Now, prepare the result for saving
records = []

for (o_zone, d_zone), link_set in od_links_dict.items():
    records.append({
        'o_zone_id': o_zone,
        'd_zone_id': d_zone,
        'links': sorted(list(link_set))
    })

result_df = pd.DataFrame(records)

# Save to CSV 
if os.path.exists(output_path):
    os.remove(output_path)
result_df.to_csv(output_path, index=False)
print("Finished building OD to links mapping!")