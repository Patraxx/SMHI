import requests
import json
from datetime import datetime, timedelta
from tabulate import tabulate
from parameters import parameter_descriptions, pcat_meanings, wsymb2_meanings


base_url = "https://opendata-download-metfcst.smhi.se/api"

approvedTime = "/api/category/{category}/version/{version}/approvedtime.json"

endpoint = f"{base_url}/category/pmp3g/version/2/geotype/point/lon/18.400/lat/59.100/data.json"

#/category/pmp3g/version/2/geotype/point/lon/18.063240/lat/59.334591/data.json

response = requests.get(endpoint)

# Sample JSON response (replace this with your actual data)
data = response.json()


# Get the current time and calculate the target time (3 hours from now)
current_time = datetime.now()

parameters_to_include = {"msl", "t","wd", "ws", "r", "gust","Wsymb2", "pcat"}

def getFiveHours(data):
    table_data
    count = 0
    for entry in data['timeSeries']:
        valid_time = entry['validTime'].replace("T", " ").replace("Z", "")
        valid_time_dt = datetime.strptime(valid_time, '%Y-%m-%d %H:%M:%S')  ##glöm inte att vi tagit bort T och Z
        if valid_time_dt > current_time:
            for param in entry['parameters']:
                if param['name'] in parameters_to_include:
                    param_name = parameter_descriptions.get(param['name'], param['name'])       
                    if param['name'] == "wsymb2":
                        param_value = wsymb2_meanings.get(param['values'][0], param['values'][0])
                    elif param['name'] == "pcat":
                        param_value = pcat_meanings.get(param['values'][0], param['values'][0])
                    else:
                        param_value = param['values'][0]
                    
                    table_data.append([
                        valid_time,
                        param_name,
                        param['levelType'],
                        param['level'],
                        param['unit'],
                        param_value
                    ])
            count += 1
            if count >= 5:
                break
    return table_data
     

def group_data(table_data):
    grouped_data = {}
    for row in table_data:
        date = row[0]
        if date not in grouped_data:
            grouped_data[date] = []
        grouped_data[date].append(row[1:])
    return grouped_data
# Output the filtered results
if __name__ == "__main__":

    table_data= getFiveHours(data)
    grouped_data = group_data(table_data)

    for date, rows in grouped_data.items():
        print(f"Date: {date}")
        print(tabulate(rows, headers=["Time", "Parameter", "Level Type", "Level", "Unit", "Value"], tablefmt="grid"))
        print("\n")
