import pygame   # to get keyboard input
import socket   # to sent data over network using TCP


def format_command(direction, speed):
    """
    Input:  direction,  characters wasd used to determine how the motors will turn (forward
                        or backwards) to achieve rover motion
            speed,      integer ranging from 0 to 5, used to control speed with PWM
    Uses direction characters wasd and speed from 0 to 5 to determine each motors turning
    direction and the speed using PWM. Returns a string with the formatted command for the
    rover to use to control the motors.
    """

    if direction == '' or speed == 0:
        return '[f0][f0][f0][f0]'
    elif direction == 'w':
        return "[f{}][f{}][f{}][f{}]".format(speed*51, speed*51, speed*51, speed*51)
    elif direction == 's':
        return "[r{}][r{}][r{}][r{}]".format(speed*51, speed*51, speed*51, speed*51)
    elif direction == 'a':
        return "[r{}][r{}][f{}][f{}]".format(speed*51, speed*51, speed*51, speed*51)
    elif direction == 'd':
        return "[f{}][f{}][r{}][r{}]".format(speed*51, speed*51, speed*51, speed*51)


if __name__ == "__main__":
    pygame.init()

    screen = pygame.display.set_mode((100, 100))    # sets the size of the pygame window
    clock = pygame.time.Clock()     # initialize clock, controls speed of window updates

    color_blue = (0, 177, 247)      # used to fill window so users can identify input window

    direction = ''
    direction_inputs = {
        pygame.K_w: 'w',
        pygame.K_s: 's',
        pygame.K_a: 'a',
        pygame.K_d: 'd'
    }

    speed = 0
    speed_inputs = {
        pygame.K_0: 0,
        pygame.K_KP0: 0,
        pygame.K_1: 1,
        pygame.K_KP1: 1,
        pygame.K_2: 2,
        pygame.K_KP2: 2,
        pygame.K_3: 3,
        pygame.K_KP3: 3,
        pygame.K_4: 4,
        pygame.K_KP4: 4,
        pygame.K_5: 5,
        pygame.K_KP5: 5
    }

    HOST = '127.0.0.1'  # standard loopback interface (localhost)
    PORT = 65432        # port to listen on (non-privileged ports are 1024 to 65535)

    client =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))

    while True:
        direction = ''

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                speed = 0
                client.sendall(format_command(direction, speed).encode())
                client.close()

                pygame.quit()
                exit()
            
            if event.type == pygame.KEYDOWN:
                for valid_speeds in speed_inputs:
                    if event.key == valid_speeds:
                        speed = speed_inputs[valid_speeds]

        for valid_directions in direction_inputs:
            if pygame.key.get_pressed()[valid_directions]:
                direction = direction_inputs[valid_directions]

        client.sendall(format_command(direction, speed).encode())

        screen.fill(color_blue)
        pygame.display.flip()