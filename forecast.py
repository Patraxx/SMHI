import requests
import json
from datetime import datetime, timedelta


base_url = "https://opendata-download-metfcst.smhi.se/api"

endpoint = f"{base_url}/category/pmp3g/version/2/geotype/point/lon/18.0549/lat/59.3417/data.json"

response = requests.get(endpoint)

# Sample JSON response (replace this with your actual data)
data = response.json()

# Get the current time and calculate the target time (3 hours from now)
current_time = datetime.strptime(data['referenceTime'], '%Y-%m-%dT%H:%M:%SZ')
target_time = current_time + timedelta(hours=3)

# Filter time series for the next 3 hours
filtered_time_series = [
    entry for entry in data['timeSeries']
    if datetime.strptime(entry['validTime'], '%Y-%m-%dT%H:%M:%SZ') <= target_time
]

# Limit to only 3 entries
filtered_time_series = filtered_time_series[:3]

# Output the filtered results
for entry in filtered_time_series:
    print(json.dumps(entry, indent=4))

#wd	degree	hl	10	Wind direction	Integer







#Latitud: 59.3417, longitud: 18.0549