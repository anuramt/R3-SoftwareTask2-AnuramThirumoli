# R3-SoftwareTask2-AnuramThirumoli
Program written for R3 Software Task 2. Using keyboard input, sends a formatted command using TCP to a rover that has 4 wheels. Send the command from a client (input and command formatting) program over to the rover (server) program. Contols directions using WASD keys and controls speed as increments from values 0 to 5.

**1. The Client (input.py)** \
The program uses pygame to get keyboard input and socket to send data over network using TCP to the server program, output.py. 
```
import pygame   # to get keyboard input
import socket   # to sent data over network using TCP (to server program)
```

The program uses one custom function called *format_command*. It use is to return a formatted string that we can send to the rover. The rover then uses the command to control its four motors using PWM. *format_command* takes two parameters: *direction* and *speed*. *direction* is the characters wasd which are used ot determine how the four motors will turn (forwards or backwards) to achieve the desired rover motion. *speed* is an integer ranging from 0 to 5 (inclusive) which sets the speed of the motor. The function checks what direction and what speed is being passed as arguments to the function and uses if statments to determine the motion of the motors and the PWM speed.
```
if direction == '' or speed == 0:   # no movement
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
```


When the program starts, it initializes pygame and creates a window (which you must have open to detect keyboard input). It also creates a pygame clock object which controls the speed at which the window updates. A tuple with the RGB values for a shade of blue is assigned to *color_blue* to change the window background to blue so the users can easily identify the window for keyboard inputs.
```
pygame.init()       # initialize pygame

screen = pygame.display.set_mode((100, 100))    # sets the size of the pygame window
clock = pygame.time.Clock()     # initialize clock, controls speed of window updates

color_blue = (0, 177, 247)      # used to fill window so users can identify input window
```

The *direction* variable is the character represetation of the direction key being pressed and will be used as a parameter for the function *format_command*. The *direction_inputs* variable is a dictionary with all the valid keys that are used for changing the directions (wasd), and for each valid key, there is a character representation of that key.
```
direction = ''          # which direction key is being pressed (wasd)
direction_inputs = {    # pygame's keyboard constants to direction character (wasd)
    pygame.K_w: 'w',
    pygame.K_s: 's',
    pygame.K_a: 'a',
    pygame.K_d: 'd'
}
```

The *speed* variable is an integer value from 0 to 5 which represents the speed the motor runs at. This means that 0 means the motors are not turning, until 5 where the motors turn at full speed. The *speed_inputs* variable is a dictionary with all the valid keys that are used for changing the speed (integers 0 to 5, both on the top keyboard row and the numpad). For each valid key, there is a character representation of that key.
```
speed = 0           # speed the motors to run at (integer from 0 to 5)
speed_inputs = {    # pygame's keyboard constants to speed values (0 to 5)
    pygame.K_0: 0, pygame.K_KP0: 0,
    pygame.K_1: 1, pygame.K_KP1: 1,
    pygame.K_2: 2, pygame.K_KP2: 2,
    pygame.K_3: 3, pygame.K_KP3: 3,
    pygame.K_4: 4, pygame.K_KP4: 4,
    pygame.K_5: 5, pygame.K_KP5: 5
}
```

The *HOST* variable is the ip address to connect to when sending data over network. The ip address '127.0.0.1" is used because that is the localhost for most computers, meaning that we connect only to the current computer using its loopback network interface. This means that other computers will not be able to connect to the client or server and disrupt the processes. We then assign the *PORT* variable as 21420. We are connecting to a non-privileged port (those from 1024 to 65535) because we don't need to get root permissions. 
```
HOST = '127.0.0.1'  # standard loopback interface (localhost)
PORT = 21420        # port to listen on (non-privileged ports are 1024 to 65535)
```

We then create a *client* variable which will be a socket to connect to the server. We use the parameters *socket.AF_INET* to use IPv4 ip addresses, and *socket.SOCK_STREAM* to send data using TCP, and use the *PORT* and *HOST* variables to connect to the server.
```
# initializes socket object with IPv4 and TCP, connects to ip address and port
client =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)     
client.connect((HOST, PORT))
```

Now we arrive at our main loop, which will be constantly detecting keyboard inputs until the pygame window is closed. We first make sure the *direction* variable is an empty string, in case no keyboard inputs are detected during this iteration of the loop.
```
# which direction key is being pressed (wasd), '' if no direction key is pressed
direction = ''
```

Then we check if any events have been triggered using *pygame.event.get()*. This will return all the events that were triggered in the previous iteration of the loop in a list format. Using a for loop, we check all the triggered events. If the event is *pygame.QUIT*, the user closed the pygame window, so we tell the rover to stop by sending a formatted command that the speed is 0. To do this, we use the *format_command* function and use the parameters '' as the *direction* and 0 as the *speed*. We then use the *str.encode()* function because we can only send data along the network in a binary format, and the *str.encode()* function does that.

**2. The Server (output.py)** \


**3. The Output** \


**4. So, how is this README relevant to my project?**
Well, this README will allow you to understand the project's code. This README is a step by step reasoning of the implementation of variables, functions, libraries etc. used. Read this as a plain English version of the code.

**THANK YOU FOR READING!** You can find the demonstrative video to download under the master branch, or watch below:

https://user-images.githubusercontent.com/59899086/138617054-7b25e987-eb7a-4d34-a9f2-26be59e82ad7.mp4

