import socket
import struct

# Create a socket and connect
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('localhost', 1225))

# Float to send
my_float = 3.14159

try:
    while True:
        # Pack float into bytes
        packed = struct.pack('!f', my_float)  # ! for network byte order, f for float

        # Send the bytes
        sock.sendall(packed)
        break  # Exit the loop after sending once
finally:
    sock.close()  # Ensure the socket is closed