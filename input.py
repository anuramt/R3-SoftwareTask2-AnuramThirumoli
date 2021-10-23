import pygame
import socket

def format_command(direction, speed):
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

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((500, 500), 0, 32)

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
                client.sendall(format_command(direction, speed))
                client.close()

                pygame.quit()
                break
            
            if event.type == pygame.KEYDOWN:
                for valid_speeds in speed_inputs:
                    if event.key == valid_speeds:
                        speed = speed_inputs[valid_speeds]

        for valid_directions in direction_inputs:
            if pygame.key.get_pressed()[valid_directions]:
                direction = direction_inputs[valid_directions]

        client.sendall(format_command(direction, speed).encode())

        pygame.display.flip()