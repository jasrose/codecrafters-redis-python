import socket
import threading



def main():
    print("Logs from your program will appear here!")

    
    server_socket = socket.create_server(("localhost", 6379), reuse_port=True)
    
    

    while True:
        client, addr = server_socket.accept() # wait for client
        print(f"accepted connection = {addr[0]}:{addr[1]}")
        
        thread: threading.Thread = threading.Thread(target=connect, args=[client])
        thread.start()


def connect(connection: socket.socket) -> None:
    with connection:
        while True:
            command: str = connection.recv(1024).decode()
            print(f"recieved - {command}")
            connected = bool(command)
        
            response: str
            match command:
                case "*1\r\n$4\r\nPING\r\n":
                    response = "+PONG\r\n"
            print(f"responding with - {response}")
            connection.sendall(response.encode())

if __name__ == "__main__":
    main()
