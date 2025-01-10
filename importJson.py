import json
import csv

# Load the JSON data
with open('tags.json', 'r') as json_file:
    data = json.load(json_file)

# Function to recursively parse the JSON and extract data
def parse_json(obj, parent_key='', rows=[]):
    if isinstance(obj, dict):
        for key, value in obj.items():
            if isinstance(value, (dict, list)):
                parse_json(value, f"{parent_key}.{key}" if parent_key else key, rows)
            else:
                if len(rows) == 0:
                    rows.append({})
                rows[-1][f"{parent_key}.{key}" if parent_key else key] = value
    elif isinstance(obj, list):
        for item in obj:
            rows.append({})
            parse_json(item, parent_key, rows)
    return rows

# Extract data and flatten it
flattened_data = parse_json(data)

# Specify CSV headers (adjust based on the data fields you want to include)
headers = set()
for row in flattened_data:
    headers.update(row.keys())
headers = sorted(headers)

# Write to a CSV file
with open('output.csv', 'w', newline='', encoding='utf-8') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=headers)
    writer.writeheader()
    writer.writerows(flattened_data)

print("JSON data has been converted to CSV and saved as 'output.csv'")