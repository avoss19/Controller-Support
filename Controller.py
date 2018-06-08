# --------------------------------File on Latop---------------------------------
# Reads controller input and connects to robot
import os, sys, socket
import pygame
from time import sleep

#### Global Variables ####

socketRate = .1 # Make larger number to slow do info sent to Robot; larger number creates more latency; Too low of number sents too much info

# left and right joystick dead zones (current dead zone for ps4 controller)
xDeadZoneLeft = 0.06
yDeadZoneLeft = 0.06
xDeadZoneRight = 0.06
yDeadZoneRight = 0.06

# motor speeds (assumes there is the same possible speeds going in reverse)
maxMotorL = 500
maxMotorR = 500

######################
## 0. Initialization
######################
pygame.init()
pygame.display.init()
pygame.joystick.init()


######################
## 1. UI
######################
def ui():
    print "#"*60
    print "Welcome to the BSM robot controller support python program!"
    print "#"*60
    controller = open('controllerASCII', "r")
    print controller.read()
    print "#"*60
    print "For support please visit https://github.com/BSMRKRS/Controller-Support.git"
    print "#"*60
    print "To controll use the left and right joystick."
    print "Hit Enter to begin!"
    raw_input("$: ")
    print "#"*60

    
######################
## 2. Controller Reading
######################
def controllerInput():
    global xAxisLeft, yAxisLeft, xAxisRight, yAxisRight
    dpadleft = 0
    dpadright = 0
    dpaddown = 0
    dpadup = 0

    pygame.event.get()

    try:
        joystick = pygame.joystick.Joystick(0)
    except:
        print "ERROR: Controller not found!"
        print "#" * 60
        exit()

    joystick.init()

    xAxisLeft = joystick.get_axis(0)
    yAxisLeft = joystick.get_axis(1)

    xAxisRight = joystick.get_axis(2)
    yAxisRight = joystick.get_axis(3


######################
## 3. Inturpret Joystick
######################
def driveMotors():
    global motorL, motorR

    if -yDeadZoneRight < yAxisRight < yDeadZoneLeft:
        motorSpeedL = 0
        motorSpeedR = 0
    else:
        motorSpeedL = maxMotorL * -yAxisRight
        motorSpeedR = maxMotorR * -yAxisRight

    if -xDeadZoneLeft < xAxisLeft < xDeadZoneLeft:
        motorL = motorSpeedL
        motorR = motorSpeedR

    elif xAxisLeft <= 0:
        motorL = motorSpeedL - (motorSpeedL * (-xAxisLeft))
        motorR = motorSpeedR
    elif xAxisLeft > 0:
        motorL = motorSpeedL
        motorR = motorSpeedR + (motorSpeedR * (-xAxisLeft))

    return motorL, motorR


######################
## 4. Convert to KitBot
######################
def speedConvert(speed):
    if speed == 1024:
        return 2047
    if speed > 0:
        speed = speed + 1024
        return speed
    else:
        return -speed


######################
## 5. Connect to Network
######################
try:
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port on the server given by the caller
    server_address = (sys.argv[1], 10000)
    print >>sys.stderr, 'connecting to %s port %s' % server_address
    sock.connect(server_address)
except:
    print "#" * 60
    print "ERROR: Failed to connect to host"
    print "#" * 60
    exit()


######################
##      Main        ##
######################
ui()
while True:
    controllerInput()
    drive = driveMotors()

    print str('%04.0f' % int(drive[0])) + ' ' + str('%04.0f' % int((drive[1])))

    try:
        sock.sendall(str('%04.0f' % int(speedConvert(-drive[0]))) + ' ' + str('%04.0f' % int(speedConvert(drive[1]))))
        sleep(socketRate)

    except:
        print "Error: Failed to connect to Robot"
        exit()

    os.system('clear')
    print "#"*60
    print "##", " "*20, "Motor Values", " " *20, "##"
    print "#"*60
    print "motorL: ", drive[0], "motorR: ", drive[1]
