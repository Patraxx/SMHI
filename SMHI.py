import requests
from datetime import datetime


# Define the URL endpoint
base_url = "https://opendata-download-metobs.smhi.se/api"   
endpoint = f"{base_url}/version/1.0/parameter/1/station/98230/period/latest-hour/data.json"

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


def fetch_latest_hour_temp_stockholm():
    metadata = fetch_data(endpoint)
    if 'value' in metadata and len(metadata['value']) > 0:
        latest_entry = metadata['value'][0]
        temperature = latest_entry.get('value')
        timestamp = latest_entry.get('date')
        human_readable_timestamp = convert_timestamp(timestamp)
      #  print(f"Temperature: {temperature} degrees Celsius at {human_readable_timestamp}")
        return float(temperature)
    else:
        print("No temperature data found")
       



if __name__ == "__main__":

    print(fetch_latest_hour_temp_stockholm())
    
   

     

                

                
                
    

# meterological observations = temp specifik plats
# om platsen inte ligger nära en smhi station, använd mesan, meterologiska analyser, ange punkt och få tillbaka senaste 24 timmarna
# metrologisk forecast, prognos annars. 
#97100: Tullinge A  
#Piteå  161790
#Stockholm Observatoriekullen 98230