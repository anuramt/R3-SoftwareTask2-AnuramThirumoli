# R3-SoftwareTask2-AnuramThirumoli
Program written for R3 Software Task 2. Using keyboard input, sends a formatted command using TCP to a rover that has 4 wheels. Send the command from a client (input and command formatting) program over to the rover (server) program. Contols directions using WASD keys and controls speed as increments from values 0 to 5.

**1. The Client (input.py)** \
The program uses pygame to get keyboard input and socket to send data over network using TCP to the server program, output.py. When the program starts, it initializes pygame and creates a window (which you must have open to detect keyboard input). It also creates a pygame clock object which controls the speed at which the window updates. A tuple with the RGB values for a shade of blue is assigned to *color_blue* to change the window background to blue so the users can easily identify the window for keyboard inputs.

The *direction* variable is the character represetation of the direction key being pressed and will be used as a parameter for the function *format_command*. The *direction_inputs* variable is a dictionary with all the valid keys that are used for changing the directions (wasd), and for each valid key, there is a character representation of that key.

The *speed* variable is an integer value from 0 to 5 which represents the speed the motor runs at. This means that 0 means the motors are not turning, until 5 where the motors turn at full speed. The *speed_inputs* variable is a dictionary with all the valid keys that are used for changing the speed (integers 0 to 5, both on the top keyboard row and the numpad). For each valid key, there is a character representation of that key.

The *HOST* variable is the ip address to connect to when sending data over network. The ip address '127.0.0.1" is used because that is the localhost for most computers, meaning that we connect only to the current computer using its loopback network interface. This means that other computers will not be able to connect to the client or server and disrupt the processes. We then assign the *PORT* variable as 21420. We are connecting to a non-privileged port (those from 1024 to 65535) because we don't need to get root permissions. 

We then create a *client* variable which will be a socket to connect to the server. We use the parameters *socket.AF_INET* to use IPv4 ip addresses, and *socket.SOCK_STREAM* to send data using TCP. Next, we use the *PORT* and *HOST* variables to connect to the server.



**2. The Server (output.py)** \


**3. The Output** \


**4. So, how is this README relevant to my project?**
Well, this README will allow you to understand the project's code. This README is a step by step reasoning of the implementation of variables, functions, libraries etc. used. Read this as a plain English version of the code.

**THANK YOU FOR READING!** You can find the demonstrative video to download under the master branch, or watch below:

https://user-images.githubusercontent.com/59899086/138617054-7b25e987-eb7a-4d34-a9f2-26be59e82ad7.mp4

