import requests

server_url = "http://192.168.10.183:8080/message"  #public ip egentligen    

def send_message(content):
    try:
        data = {
            "content": content
        }
        response = requests.post(server_url, json=data)
        response.raise_for_status()
        print(f"Sent message to server: {data}")
        print(f"Server response: {response.text}")
    except requests.RequestException as e:
        print(f"Error sending message to server: {e}")

if __name__ == "__main__":
    message = "Hello, Go server!"
    send_message(message)
    




#192.168.10.183