import socket

class Server:
    def __init__(self, host='0.0.0.0', port=9238):
        self.host = host
        self.port = port
        self.server_socket = None
        self.conn = None
        self.addr = None

    def start(self):
        """Start the server and wait for a connection."""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(1)
        print(f"Server started, waiting for connection on {self.host}:{self.port}...")
        self.conn, self.addr = self.server_socket.accept()
        print(f"Connected by {self.addr}")

    def read_message(self):
        """Read a message from the client."""
        if self.conn:
            data = self.conn.recv(1024)
            if data:
                message = data.decode()
                print(f"Received from client: {message}")
                return message
            else:
                print("No data received. Closing connection.")
                self.close_connection()
                return None
        else:
            print("No active connection.")
            return None

    def send_message(self, message):
        """Send a message to the client."""
        if self.conn:
            self.conn.send(message.encode())
            print(f"Sent to client: {message}")
        else:
            print("No active connection to send message.")

    def close_connection(self):
        """Close the client connection."""
        if self.conn:
            self.conn.close()
            self.conn = None
            print("Connection closed.")

    def shutdown(self):
        """Shutdown the server."""
        self.close_connection()
        if self.server_socket:
            self.server_socket.close()
            print("Server shut down.")

