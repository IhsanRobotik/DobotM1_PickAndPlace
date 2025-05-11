import socket
import struct

# Create socket and bind/listen
server = socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 12345))
server.listen(1)

conn, addr = server.accept()

try:
    # Receive 4 bytes (size of a float)
    while True:
        data = conn.recv(4)
        if not data:  # Break if the connection is closed
            break
        received_float = struct.unpack('!f', data)[0]  # Unpack bytes to float

        print("Received float:", received_float)
finally:
    conn.close()  # Ensure the connection is closed
    server.close()