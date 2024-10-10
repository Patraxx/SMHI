import requests
from datetime import datetime

base_url = "https://opendata-download-metobs.smhi.se/api"

time_periods = {'latest-hour', 'latest-day', 'latest-months'}

def convert_timestamp(timestamp):
    dt_object = datetime.fromtimestamp(timestamp / 1000)
    return dt_object.strftime("%Y-%m-%d %H:%M:%S")

def get_parameters():
    url = f"{base_url}/version/1.0.json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        parameters = data['resource']
        parameter_keys = []
        parameter_titles  = []
        for parameter in parameters:
            key = parameter['key']
            title = parameter['title']
            parameter_keys.append(key)
            parameter_titles.append(title)
          #  print(f"{key}: {title}")
        return parameter_keys, parameter_titles
    else:
        print("Failed to retrieve parameters:", response.status_code)
        return []
    
def fetch_latest_data(station_id, parameter_key):
    period_url = f"{base_url}/version/1.0/parameter/{parameter_key}/station/{station_id}/period/latest-hour/data.json"
   # GET /api/version/1.0/parameter/1/station/159880/period/latest-months.atom
    response = requests.get(period_url)
    if response.status_code == 200:
        data = response.json()
        if 'value' in data and len(data['value']) > 0:
            latest_entry = data['value'][0]      
            return latest_entry.get('value', 'no data')
    return 'No data'

def print_all_stations(parameter_key):
    url = f"{base_url}/version/1.0/parameter/{parameter_key}.json"  ##lägg ihop url med parametrar
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        stations = data['station']
        raw_title = data.get('title', 'Unknown')
        parameter_title = raw_title.split(':')[0] if ':' in raw_title else raw_title      
      #  parameter_data = data['parameter']
        for station in stations:
            station_id = station['key']
            station_name = station['name']
            latest_value = fetch_latest_data(station_id, parameter_key)
            if latest_value == 'No data':
                continue
            print(f"{station_id}: {station_name} - {parameter_title} - Latest Value: {latest_value}")
    else:
        print(f"Failed to retrieve stations for parameter {parameter_key}:", response.status_code)

def print_station_info(station_id, time_period):
    url = f"{base_url}/version/1.0/parameter/1/station/{station_id}/period/{time_period}.json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        station_name = data['station']['title']
        print(f"Station: {station_name}")


def print_hardcoded_stationtemp_latestHour(parameter_key,station_id):
    url = f"{base_url}/version/1.0/parameter/{parameter_key}/station/{station_id}/period/latest-hour/data.json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        station_name = data['station']['name']
        station_temp = data['value'][0]['value']
        timestamp = station_temp.get('date')
        print(f"Station: {station_name} - Temperature: {station_temp} at {timestamp}")
    else:
        print("Failed to retrieve data:", response.status_code)


   
 
 

if __name__ == "__main__":
  
  
  print_hardcoded_stationtemp_latestHour(1, 97400)

  
  

   # parameter_keys,parameter_titles,  = get_parameters()
    #for key, title in zip(parameter_keys, parameter_titles):  ##kika mer på denna
     #   print(f"{key}: {title}")
   
  
        
   # get_parameters()
   # print_all_stations(1)
  # print_station_info(97400)
   # latest_value = fetch_latest_data(97400, 1)
   # print(latest_value)

    # GET /api/version/1.0/parameter/1/station/159880/period/latest-months.atom

    #Stockholm -Arlanda 97400
    #Stockholm -Bromma 97200
    #Stockholm -Observatoriekullen A 98230
    #Stockholm -Observatoriekullen  98210


