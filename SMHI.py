import requests
from datetime import datetime
from tabulate import tabulate


# Define the URL endpoint
base_url = "https://opendata-download-metobs.smhi.se/api"   
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

def print_latest_hour_temp(data):

    if 'value' in data and len(data['value']) > 0:
        latest_entry = data['value'][0]
        temperature = latest_entry.get('value')
        timestamp = latest_entry.get('date')
        human_readable_timestamp = convert_timestamp(timestamp)
        print(f"Temperature: {temperature} degrees Celsius at {human_readable_timestamp}")
    else:
        print("No temperature data found")

       
data = fetch_data(endPointAll)

def chooseStation(station_name):
    matches = []
    for station in data ['station']:
        if  station_name.lower() in station['name'].lower():
            matches.append(station)
    if matches:
            table = []
            for match in matches:
                table.append([match['name'], match['key'], match['latitude'], match['longitude']])
            print(tabulate(table, headers=["Name", "Key", "Latitude", "Longitude"], tablefmt="pretty"))
            return matches
    else:  
        print(f"Station {station_name} not found")
        return None
def chooseStationInput():
  print(" ")
  return input("Enter station name: ")

def citiesbycoords(lat, lon):
    for station in data['station']:
        if station['latitude'] == lat and station['longitude'] == lon:
            print(f"{station['name']} ({station['key']}) - Lat: {station['latitude']} Long: {station['longitude']}")
            return station['key']
    print("No station found for the given coordinates")
    return None


def calculateCoordinateSpan(stations):
    if not stations:
        return None

    min_lat = min(station['latitude'] for station in stations)
    max_lat = max(station['latitude'] for station in stations)
    min_lon = min(station['longitude'] for station in stations)
    max_lon = max(station['longitude'] for station in stations)

    return {
        'min_latitude': min_lat,
        'max_latitude': max_lat,
        'min_longitude': min_lon,
        'max_longitude': max_lon
    }

def getCoords():
    lat = float(input("Enter latitude: "))
    lon = float(input("Enter longitude: "))
    return lat, lon

coordminmax = 0.6

def citiesFromCoords(lat, lon):
    data = fetch_data(endPointAll)
    matching_stations = []
    for station in data['station']:
        if station['latitude'] > lat - coordminmax and station['latitude'] < lat + coordminmax and station['longitude'] > lon - coordminmax and station['longitude'] < lon + coordminmax:
            matching_stations.append(station)
    if matching_stations:
        table = []
        for match in matching_stations:
            table.append([match['name'], match['key'], match['latitude'], match['longitude']])
        print(tabulate(table, headers=["Name", "Key", "Latitude", "Longitude"], tablefmt="pretty"))
        return matching_stations
    else:
        print("No stations nearby given coordinates")
      
        return None

    

   

if __name__ == "__main__":
   
   lat, lon = getCoords()
   matching_stations = citiesFromCoords(lat, lon)




   # chooseStation('lund')
   while(True):
         
    station_name = chooseStationInput()
    matching_stations = chooseStation(station_name)

    if matching_stations: 
       coordinate_span = calculateCoordinateSpan(matching_stations)
       if coordinate_span:
            print(f"Coordinate span for  {station_name}:")
            print(f"Latitude: {coordinate_span['min_latitude']:.2f} - {coordinate_span['max_latitude']:.2f}")
            print(f"Longitude: {coordinate_span['min_longitude']:.2f} - {coordinate_span['max_longitude']:.2f}")
            print(f"Longitude span is {coordinate_span['max_longitude'] - coordinate_span['min_longitude']:.2f}")
            print(f"Latitude span is {coordinate_span['max_latitude'] - coordinate_span['min_latitude']:.2f}")

  ##  print(fetch_latest_hour_temp_stockholm())

#nynäshamn  58.9159, longitud: 17.9342"

#Saarikoski 68.8032, longitud: 21.2468
#trelleborg 55.3811, longitud: 13.1195
#smögen     58.3536, longitud: 11.2178 
#haparanda  65.8237, longitud: 24.1112

#lowest lat: 55.3811, long: 13.1195


     
#skarpnäck lat: 59.2637287, long: 18.1106868
                

                
                
    

# meterological observations = temp specifik plats
# om platsen inte ligger nära en smhi station, använd mesan, meterologiska analyser, ange punkt och få tillbaka senaste 24 timmarna
# metrologisk forecast, prognos annars. 
#97100: Tullinge A  
#Piteå  161790
#Stockholm Observatoriekullen 98230