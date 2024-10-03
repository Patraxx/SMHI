import requests
from datetime import datetime


# Define the URL endpoint
base_url = "https://opendata-download-metobs.smhi.se/api"   

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
     
if __name__ == "__main__":
      endpoint = f"{base_url}/version/1.0/parameter/1/station/98230/period/latest-hour.json"

      metadata = fetch_data(endpoint)

      if metadata:
          
            data_link = None
            for link in metadata.get('data', [])[0].get('link', []):
                if link['type'] == 'application/json':
                  data_link = link['href']
                  break
              
            if data_link:
                actual_data = fetch_data(data_link)
                if actual_data:
                    print_latest_hour_temp(actual_data)
            else:
                print("No data link found")

                
                
    

# meterological observations = temp specifik plats
# om platsen inte ligger nära en smhi station, använd mesan, meterologiska analyser, ange punkt och få tillbaka senaste 24 timmarna
# metrologisk forecast, prognos annars. 
#97100: Tullinge A  
#Piteå  161790
#Stockholm Observatoriekullen 982130 