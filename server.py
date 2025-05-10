import socket

# Set IP and port
HOST = '0.0.0.0'  # Listen on all interfaces
PORT = 9238       # Must match the client's port

# Create socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)

print(f"Server started, waiting for connection on {HOST}:{PORT}...")

conn, addr = server_socket.accept()
print(f"Connected by {addr}")

try:
    while True:
        data = conn.recv(1024)
        if not data:
            print("No data received. Closing connection.")
            break
        flag = data.decode()
        print(f"Received from client: {flag}")

        # Reply to client
        response = f"Server received: {flag}"
        conn.send(response.encode())
except KeyboardInterrupt:
    print("Server shutting down.")
finally:
    conn.close()
    server_socket.close()
