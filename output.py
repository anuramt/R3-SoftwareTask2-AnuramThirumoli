"""
Name:           Anuram Thirumoli
Date:           October 24th, 2021
Language:       Python
Project:        R3 - Software Task 2 (input.py) (client)
Description:    Program written for R3 Software Task 2. Using keyboard input, sends a
                formatted command using TCP to a rover that has 4 wheels. Send the command
                from a client (input and command formatting) program over to the rover
                (server) program. Contols directions using WASD keys and controls speed as
                increments from values 0 to 5.
"""

import socket   # to get formatted command over network using TCP (from client program)

if __name__ == "__main__":
    HOST = '127.0.0.1'  # standard loopback interface address (localhost)
    PORT = 21420        # port to listen on (non-privileged ports are 1024 to 65535)

    # initializes socket object with IPv4 and TCP, connects to ip address and port
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))

    server.listen()     # waits until client has connected
    
    # gets socket to recieve and transmit data and the ip address the socket is connected to
    data_socket, address = server.accept()

    # using the socket recieve and print data
    with data_socket:
        """Recieves, decodes, and prints data from client program until connection is closed
        or an error occurs."""
        while True: 
            received_data = data_socket.recv(1024)

            if not received_data:
                break

            print(received_data.decode())   # prints formatted command from client program