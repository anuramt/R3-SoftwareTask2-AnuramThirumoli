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

Then we check if any events have been triggered using *pygame.event.get()*. This will return all the events that were triggered in the previous iteration of the loop in a list format. Using a for loop, we check all the triggered events. If the event is *pygame.QUIT*, the user closed the pygame window, so we tell the rover to stop by sending a formatted command that the speed is 0. To do this, we use the *format_command* function and use the parameters '' as the *direction* and 0 as the *speed*. We then use the *str.encode()* function because we can only send data along the network in a binary format, and the *str.encode()* function does that. \
If the event is not *pygame.QUIT*, we check if the event is *pygame.KEYDOWN*. If it is, a key got pressed (not held down). We check if the key for the event is a valid speed key (using *speed_inputs*), and if it is, uses the dictionary value for that key as the speed.
```
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
```

Next, we check if a direction key (wasd) got pressed (is held down). We do this by checking if any of the valid direction keys that are in the dictionary *direction_inputs* are being held down. We check which keys are being held down by using *pygame.key.get_pressed()*, which returns an array with all the pygame key constants and a boolean value whether or not they are being held down or not. If a direction key is being held down, we use the dictionary value for that key as the direction.
```
 """Checks if any directions keys (wasd) keys are being pressed. If it is, direction
is the character corresponding to the key."""
for valid_directions in direction_inputs:
    if pygame.key.get_pressed()[valid_directions]:
        direction = direction_inputs[valid_directions]
```

We send the formatted instruction to the rover with our desired direction and speed using the function *format_command*. We use the *str.encode()* function because we can only send data along the network in a binary format, and the *str.encode()* function does that. \
Finally, we set the window fill colour to a shade of blue and update the display.
```
# send the formatted instruction for the four motors to the rover server
client.sendall(format_command(direction, speed).encode())

screen.fill(color_blue)     # change window background color to blue
pygame.display.flip()       # update display
```

**2. The Server (output.py)** \
The program uses socket to get data over network using TCP from the client program, input.py.
```
import socket   # to get formatted command over network using TCP (from client program)
```

The *HOST* variable is the ip address to connect to when recieving data over network. The ip address '127.0.0.1" is used because that is the localhost for most computers, meaning that we connect only to the current computer using its loopback network interface. This means that other computers will not be able to connect to the client or server and disrupt the processes. We then assign the *PORT* variable as 21420. We are connecting to a non-privileged port (those from 1024 to 65535) because we don't need to get root permissions. 
```
HOST = '127.0.0.1'  # standard loopback interface (localhost)
PORT = 21420        # port to listen on (non-privileged ports are 1024 to 65535)
```

Then create a *server* variable which will be a socket that the client connects to. We use the parameters *socket.AF_INET* to use IPv4 ip addresses, and *socket.SOCK_STREAM* to send data using TCP, and bind the server to *PORT* and *HOST* variables.
```
 # initializes socket object with IPv4 and TCP, connects to ip address and port
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
```

Next we listen until the client is connected. This is a blocking call, which means that the client must connect first before the program to continue. When the client connects, it will output a tuple with another socket to get data and the ip address of the computer connecting to the server. We use the variables *data_socket* and *address* to assign the tuples values to it.
```
server.listen()     # waits until client has connected
    
# gets socket to recieve and transmit data and the ip address the socket is connected to
data_socket, address = server.accept()
```

Finally, using the socket we got from *server.listen()*, we can recieve data from the client. We use a while loop to recieve data until the connection ends, where we break out of the loop. In the loop, every time we recieve data, we print the data. However, we first decode it to a string format using *decode()* which takes binary value and converts it to a string. This print statement prints the formatted command which the client sent based on keyboard input.
```
# using the socket recieve and print data
with data_socket:
    """Recieves, decodes, and prints data from client program until connection is closed
    or an error occurs."""
    while True: 
        received_data = data_socket.recv(1024)

        if not received_data:
            break

        print(received_data.decode())   # prints formatted command from client program
```

**5. The Output** \
***NO MOVEMENT*** \
[f0][f0][f0][f0]

***FORWARD*** \
[f51][f51][f51][f51] \
[f102][f102][f102][f102] \
[f153][f153][f153][f153] \
[f204][f204][f204][f204] \
[f255][f255][f255][f255]

***REVERSE*** \
[r51][r51][r51][r51] \
[r102][r102][r102][r102] \
[r153][r153][r153][r153] \
[r204][r204][r204][r204] \
[r255][r255][r255][r255]

***LEFT*** \
[r51][r51][f51][f51] \
[r102][r102][f102][f102] \
[r153][r153][f153][f153] \
[r204][r204][f204][f204] \
[r255][r255][f255][f255]

***RIGHT*** \
[f51][f51][r51][r51] \
[f102][f102][r102][r102] \
[f153][f153][r153][r153] \
[f204][f204][r204][r204] \
[f255][f255][r255][r255]

**4. Ensuring the program works:** \
This program only uses keyboard inputs! Also, ensure the program works by first starting the server (output.py), then starting the client (input.py). This is because the client will encounter an error if it does not connect to a server. 

**5. So, how is this README relevant to my project?** \
Well, this README will allow you to understand the project's code. This README is a step by step reasoning of the implementation of variables, functions, libraries etc. used. Read this as a plain English version of the code.

**THANK YOU FOR READING!** You can find the demonstrative video to download under the master branch, or watch below:

https://user-images.githubusercontent.com/59899086/138617054-7b25e987-eb7a-4d34-a9f2-26be59e82ad7.mp4

