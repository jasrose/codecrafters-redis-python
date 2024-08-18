import socket
import threading

def main():
    print("Starting server...")

    # Create a server socket that listens on localhost and port 6379
    server_socket = socket.create_server(("localhost", 6379), reuse_port=True)

    while True:
        # Wait for a client to connect
        client, addr = server_socket.accept()
        print(f"Accepted connection from {addr[0]}:{addr[1]}")

        # Start a new thread to handle the client connection
        client_thread = threading.Thread(target=handle_client, args=(client,))
        client_thread.start()

def handle_client(connection: socket.socket) -> None:
    with connection:
        buffer = ""
        while True:
            # Receive data from the client
            data = connection.recv(1024).decode()
            if not data:
                print("Client disconnected.")
                break

            # Append received data to the buffer
            buffer += data
            print(f"Buffered data: {buffer}")

            # Check if the buffer contains a complete command
            if buffer.endswith("\r\n"):
                response = determine_response(buffer)
                connection.sendall(response.encode())
                buffer = ""  # Clear the buffer after processing

def determine_response(command: str) -> str:
    # Split the command by line breaks
    parts = command.strip().split("\r\n")
    
    # Check if the command is PING
    if parts == ["*1", "$4", "PING"]:
        return "+PONG\r\n"
    
    # Check if the command is ECHO
    elif len(parts) == 5 and parts[2] == "ECHO":
        message = parts[4]
        return build_echo_response(message)

    # Default response for unrecognized commands
    return "-ERR unknown command\r\n"

def build_echo_response(message: str) -> str:
    # Calculate the length of the message
    message_length = len(message)

    # Construct the RESP bulk string response with only the message
    return f"${message_length}\r\n{message}\r\n"

if __name__ == "__main__":
    main()