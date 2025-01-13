import socket
import threading


# Function to handle client connections
def handle_client(client_socket, client_address):
    print(f"Connection established with {client_address}")

    try:
        # Receive the request data from the client
        request = client_socket.recv(1024).decode('utf-8')

        if not request.startswith("GET "):
            raise ValueError("Unsupported method")

        if request:
            print(f"Request from {client_address}:\n{request.splitlines()[0]}\n{request.splitlines()[1]}\n{request.splitlines()[2]}")
            print("user-agent:", end=" ")
            print(next((line.split(": ", 1)[1].split(" ")[0] for line in request.splitlines() if line.lower().startswith("user-agent:")), None)
)
            request_line = request.splitlines()[0]
            path = request_line.split(" ")[1]



            if path == "/":
                response_body = "Welcome to the Home Page!"
                status_code = "200 OK"
            elif path == "/user-agent":
                user_agent = "Unknown"
                for line in request.splitlines():
                    if line.lower().startswith("user-agent:"):
                        user_agent = line.split(": ", 1)[1].split(" ")[0]
                        break
                response_body = f"User-Agent: {user_agent}"
                status_code = "200 OK"

            else:
                response_body = "404 Not Found"
                status_code = "404 Not Found"


            # Prepare an HTTP response
            headers = (
                f"HTTP/1.1 {status_code}\r\n"
                "Content-Type: text/plain\r\n"
                f"Content-Length: {len(response_body)}\r\n"
                "Connection: close\r\n"
                "\r\n"
            )
            print(">")
            print("headers sent")
            print(headers)
            # Send the HTTP response
            client_socket.sendall(headers.encode('utf-8') + response_body.encode('utf-8'))

        else:
            print(f"Empty request from {client_address}")
    except Exception as e:
        print(f"Error handling client {client_address}: {e}")
    finally:
        client_socket.close()

# Create a server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 6969  )
server_socket.bind(server_address)

server_socket.listen(5)  # Allow up to 5 connections in the queue
print("Server is listening on http://localhost:6969...")

while True:
    client_socket, client_address = server_socket.accept()
    # Create a new thread for each client
    client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
    client_thread.start()
