import socket

ESP_IP = "192.168.10.127" # ersätt med riktig adress
ESP_PORT = 1349

def send_tcp_message(message):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((ESP_IP, ESP_PORT))
        sock.sendall(message.encode('utf-8'))
        sock.close()
        print("Message sent to esp")
    except Exception as e:
        print("Failed to send message:", e)

 