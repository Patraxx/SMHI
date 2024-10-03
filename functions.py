import requests

base_url = "https://opendata-download-metobs.smhi.se/api"

def get_parameters():
    url = f"{base_url}/version/1.0.json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        parameters = data['resource']
        parameter_keys = []
        for parameter in parameters:
            key = parameter['key']
            title = parameter['title']
            parameter_keys.append(key)
            print(f"{key}: {title}")
        return parameter_keys
    else:
        print("Failed to retrieve parameters:", response.status_code)
        return []

def print_all_stations(parameter_key):
    url = f"{base_url}/version/1.0/parameter/{parameter_key}.json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        stations = data['station']
        for station in stations:
            station_id = station['key']
            station_name = station['name']
            print(f"{station_id}: {station_name}")
    else:
        print(f"Failed to retrieve stations for parameter {parameter_key}:", response.status_code)

if __name__ == "__main__":
    get_parameters()
