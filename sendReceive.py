from serverClass import Server
import time

if __name__ == "__main__":
    server = Server()
    try:
        server.start()
        # Send "hello" to the client
        while True:
            server.send_message("hello")
            print(server.read_message())
            time.sleep(1)
    except KeyboardInterrupt:
        print("Server shutting down.")
    finally:
        server.shutdown()