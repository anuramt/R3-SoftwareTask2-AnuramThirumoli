import socket

if __name__ == "__main__":
    HOST = '127.0.0.1'  # standard loopback interface address (localhost)
    PORT = 65432        # port to listen on (non-privileged ports are 1024 to 65535)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    conn, addr = server.accept()

    with conn:
        print('Connected by', addr)

        while True:
            recv_data = conn.recv(1024)
            if not recv_data:
                break
            print(recv_data)