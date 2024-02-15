import socket

# Connect to microcontroller server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('206.12.179.20', 8080))

# Send request for temperature reading
client_socket.send(b'TEMP')

# Receive response
response = client_socket.recv(1024)
print(response.decode())

# Close connection
client_socket.close()


