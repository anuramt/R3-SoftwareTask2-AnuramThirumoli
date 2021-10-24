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


import pygame   # to get keyboard input
import socket   # to sent data over network using TCP (to server program)


def format_command(direction, speed):
    """
    Input:  direction,  characters wasd used to determine how the four motors will turn
                        (forward or backwards) to achieve rover motion
            speed,      integer ranging from 0 to 5, used to control speed with PWM
    Uses direction characters wasd and speed from 0 to 5 to determine each motors turning
    direction and the speed using PWM. Returns a string with the formatted command for the
    rover to use to control the four motors.
    """

    if direction == '' or speed == 0:   # no movement
        return '[f0][f0][f0][f0]'

    elif direction == 'w':          # moving forward
        return "[f{}][f{}][f{}][f{}]".format(speed*51, speed*51, speed*51, speed*51)

    elif direction == 's':          # moving backward
        return "[r{}][r{}][r{}][r{}]".format(speed*51, speed*51, speed*51, speed*51)

    elif direction == 'a':          # turning left
        return "[r{}][r{}][f{}][f{}]".format(speed*51, speed*51, speed*51, speed*51)
        
    elif direction == 'd':          # turning right
        return "[f{}][f{}][r{}][r{}]".format(speed*51, speed*51, speed*51, speed*51)


if __name__ == "__main__":
    pygame.init()       # initialize pygame

    screen = pygame.display.set_mode((100, 100))    # sets the size of the pygame window
    clock = pygame.time.Clock()     # initialize clock, controls speed of window updates

    color_blue = (0, 177, 247)      # used to fill window so users can identify input window

    direction = ''          # which direction key is being pressed (wasd)
    direction_inputs = {    # pygame's keyboard constants to direction character (wasd)
        pygame.K_w: 'w',
        pygame.K_s: 's',
        pygame.K_a: 'a',
        pygame.K_d: 'd'
    }

    speed = 0           # speed the motors to run at (integer from 0 to 5)
    speed_inputs = {    # pygame's keyboard constants to speed values (0 to 5)
        pygame.K_0: 0, pygame.K_KP0: 0,
        pygame.K_1: 1, pygame.K_KP1: 1,
        pygame.K_2: 2, pygame.K_KP2: 2,
        pygame.K_3: 3, pygame.K_KP3: 3,
        pygame.K_4: 4, pygame.K_KP4: 4,
        pygame.K_5: 5, pygame.K_KP5: 5
    }

    HOST = '127.0.0.1'  # standard loopback interface (localhost)
    PORT = 21420        # port to listen on (non-privileged ports are 1024 to 65535)

    # initializes socket object with IPv4 and TCP, connects to ip address and port
    client =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)     
    client.connect((HOST, PORT))

    # runs until the program exits after pygame.QUIT event happens (pygame window is closed)
    while True:
        # which direction key is being pressed (wasd), '' if no direction key is pressed
        direction = ''

        # gets and checks all the events in queue
        for event in pygame.event.get():
            if event.type == pygame.QUIT:   # window gets closed
                client.sendall(format_command('', 0).encode())  # stop rover movement
                client.close()  # closes connection

                pygame.quit()   # stops pygame
                exit()          # exits/stops program
            
            elif event.type == pygame.KEYDOWN:  # a key was pressed (not held)
                """Checks if any pressed key is a key that changes motor speed for rover
                (integer from 0 to 5). If it is, speed is the value corresponding to the key."""
                for valid_speeds in speed_inputs:
                    if event.key == valid_speeds:
                        speed = speed_inputs[valid_speeds]

        """Checks if any directions keys (wasd) keys are being pressed. If it is, direction
        is the character corresponding to the key."""
        for valid_directions in direction_inputs:
            if pygame.key.get_pressed()[valid_directions]:
                direction = direction_inputs[valid_directions]

        # send the formatted instruction for the four motors to the rover server
        client.sendall(format_command(direction, speed).encode())

        screen.fill(color_blue)     # change window background color to blue
        pygame.display.flip()       # update display