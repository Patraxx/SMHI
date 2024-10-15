import requests
from datetime import datetime

base_url = "https://opendata-download-metobs.smhi.se/api"
base_url_forecast = "https://opendata-download-metfcst.smhi.se/api"
time_periods = {'latest-hour', 'latest-day', 'latest-months'}

endpointsthlm = f"{base_url}/version/1.0/parameter/1/station/98230/period/latest-hour/data.json"
endPointAll = f"{base_url}/version/1.0/parameter/1/station-set/all/period/latest-hour/data.json"

def fetch_data(endpoint):
    response = requests.get(endpoint)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to retrieve data:", response.status_code)
        return None

def convert_timestamp(timestamp):
    dt_object = datetime.fromtimestamp(timestamp / 1000)
    return dt_object.strftime("%Y-%m-%d %H:%M:%S")


def fetch_latest_hour_temp_stockholm():
    metadata = fetch_data(endpointsthlm)
    if 'value' in metadata and len(metadata['value']) > 0:
        latest_entry = metadata['value'][0]
        temperature = latest_entry.get('value')
        timestamp = latest_entry.get('date')
        human_readable_timestamp = convert_timestamp(timestamp)
      #  print(f"Temperature: {temperature} degrees Celsius at {human_readable_timestamp}")
        return float(temperature)
    else:
        print("No temperature data found")

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


def get_nearest_available_point_data(longitude, latitude):
    pointsearchurl: f"{base_url_forecast}/category/pmp3g/version/2/geotype/point/lon/{longitude}/lat/{latitude}/data.json"
    response = requests.get(pointsearchurl)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print("Failed to retrieve data:", response.status_code)
        return None



   
 
 

if __name__ == "__main__":

    longitude = input("Enter longitude: ")
    latitude = input("Enter latitude: ")
    data = get_nearest_available_point_data(longitude, latitude)

  
   
  

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


