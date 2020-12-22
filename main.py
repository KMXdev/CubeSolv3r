#!/usr/bin/env pybricks-micropython

"""
Lego® Mindstorms® EV3 Robot to solve a Rubik's Cube®
----------------------------------------------------

written by: Quirin Möller & Jakob Schönlinner
Based on the .ev3 program written by David Gilday

Building instructions and original program can be found at:
https://www.mindcuber.com/mindcub3r/mindcub3r.html

(c) Jakob Schönlinner and Quirin Möller 2020
License: GPL-3.0 License
"""


from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, ColorSensor, InfraredSensor
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.media.ev3dev import Font, SoundFile, ImageFile

from copy import deepcopy

from rubik.cube import Cube

# c = 3*(10**8)

# font definitions
bigFont = Font(size = 25, bold = True)
smallFont = Font(size = 18)

# Lego® Mindstorms® EV3-Brick object
ev3 = EV3Brick()

# Motor objects
tiltMotor = Motor(Port.A, Direction.CLOCKWISE)
tableMotor = Motor(Port.B, Direction.CLOCKWISE)         # [12, 36]
colorMotor = Motor(Port.C, Direction.COUNTERCLOCKWISE)  # [12, 36]

# Sensor objects
infraredSensor = InfraredSensor(Port.S1)
colorSensor = ColorSensor(Port.S2)


# display the logo and authors
def banner():
    ev3.screen.clear()
    ev3.screen.set_font(bigFont)
    ev3.screen.draw_text(1, 1, 'CubeSolv3r', Color.BLACK, None)
    ev3.screen.set_font(smallFont)
    ev3.screen.draw_text(1, 30, 'by Quirin und Jakob', Color.BLACK, None)

# display any given text to the EV3's screen
def message(text):
    ev3.screen.clear()
    ev3.screen.set_font(bigFont)
    ev3.screen.draw_text(1, 1, text, Color.BLACK, None)

# calibrate the motor which is responsible for moving the color sensor
def scanCal():
    colorMotor.run_until_stalled(500, Stop.COAST, 40)
    colorMotor.run_until_stalled(-500, Stop.COAST, 40)
    wait(250)
    colorMotor.run_angle(500, 340, Stop.BRAKE, True)

# calibrate the motor which is responsible for moving the cube arm
def tiltCal():
    tiltMotor.run_angle(500, 10, Stop.BRAKE, True)
    tiltMotor.run_until_stalled(-200, Stop.COAST, 40)


# draw the code (input)
def draw_input(input, selected):
    ev3.screen.clear()
    y = ev3.screen.height / 2 - (ev3.screen.height / 14)
    for i in range(len(input)):
        x = (ev3.screen.width / 7) * ((i + 1) * 2) - (ev3.screen.width / 11)
        ev3.screen.set_font(bigFont)
        if i == selected:
            ev3.screen.draw_text(x, y, str(input[i]), Color.WHITE, Color.BLACK)
        else:
            ev3.screen.draw_text(x, y, str(input[i]), Color.BLACK, None)


# entprellen
def entprell():
    while ev3.buttons.pressed():
        wait(10)
        pass
    return
 

# # code lock
# def code_lock():
#     # define variables for code-lock
#     code = [0,0,0]
#     c_input = [0,0,0]
#     calib_code = [5,8,2]
#     selected = 0
#     # initialize code input
#     draw_input(c_input, selected)
#     while True:
#         pressed = ev3.buttons.pressed()        
#         if Button.LEFT in pressed:
#             selected -= 1
#             selected %= 3
#             entprell()
#         if Button.RIGHT in pressed:
#             selected += 1
#             selected %= 3
#             entprell()
#         if Button.UP in pressed:
#             c_input[selected] += 1
#             c_input[selected] %= 10
#             entprell()
#         if Button.DOWN in pressed:
#             c_input[selected] -= 1
#             c_input[selected] %= 10
#             entprell()
#         if pressed:
#             draw_input(c_input, selected)
#         if Button.CENTER in pressed:
#             entprell()
#             if c_input == code:
#                 return True
#             else:
#                 if c_input == calib_code:
#                     cc_sensor()
#                 return False

# calibrate color sensor
def cc_sensor():
    ev3.screen.clear()
    ev3.screen.draw_text(0, 0, 'Calibrating', Color.BLACK, None)
    wait(1000)
    colorSensor.calibrate_white()
    wait(1000)

# check if the cube is inserted
def cubeCheck():
    ev3.screen.clear()
    x0 = 100
    x1 = 100
    while (x0 > 22) and (x1 > 22):
        x0 = 100
        x1 = 100
        ev3.screen.draw_text(1,1, 'Insert Cube', Color.BLACK, None)
        ev3.light.on(Color.YELLOW)
        x0 = infraredSensor.distance()
        wait(2500)
        x1 = infraredSensor.distance()
    ev3.screen.clear()
    ev3.screen.draw_text(1,1, 'Cube inserted', Color.BLACK, None)


# scan all faces of the cube and store them
def scanCube():
    faces = [[]] * 6
    for i in range(4):
        scanned_face = scanFace()
        faces[i] = deepcopy(scanned_face)
        tilt()
    turn()
    tilt()
    scanned_face = scanFace()
    faces[4] = deepcopy(scanned_face)
    tilt()
    wait(1000)
    tilt()
    scanned_face = scanFace()
    faces[5] = deepcopy(scanned_face)


# scan a single face
def scanFace():
    face = [[6]] * 9
    
    movetomiddle = 435
    middletoedge = -200
    edgetocorner = -80
    tablestep = -135
    
    ev3.screen.clear()
    ev3.screen.print(colorMotor.angle())
    colorMotor.run_angle(500, movetomiddle, Stop.BRAKE, True)
    
    # scan the middle tile
    face[0] = getColor(colorSensor.rgb())
    colorMotor.run_angle(500, middletoedge, Stop.HOLD, True)
    wait(300)
    
    for i in range(4):
        # edges
        face[i*2+1] = getColor(colorSensor.rgb())
        colorMotor.run_angle(300, edgetocorner, Stop.HOLD, False)
        tableMotor.run_angle(200, tablestep, Stop.BRAKE, True)
        
        # corners
        face[i*2+2] = getColor(colorSensor.rgb())
        colorMotor.run_angle(300, -(edgetocorner), Stop.HOLD, False)
        tableMotor.run_angle(200, tablestep, Stop.BRAKE, True)
    
    # reset the scanner position
    colorMotor.run_angle(300, -235, Stop.HOLD, True)
    return face


# calculate a color value from an rgb input
def getColor(rgb):
    # translate rgb to colorcode 0=black 1=blue 2=green 3=yellow 4=red 5=white 6=none
    # ev3.screen.clear()
    # ev3.screen.print(rgb)
    return rgb

# # tilt the cube
# def tilt():
#     tiltMotor.run_target(200, 85, Stop.BRAKE, True)
#     tiltMotor.run_target(200, 195, Stop.BRAKE, True)
#     tiltMotor.run_target(200, 60, Stop.BRAKE, True)
#     tiltMotor.run_target(200, 85, Stop.BRAKE, True)

# tilt the cube
def tilt():
    tiltMotor.run_angle(175, 190, Stop.BRAKE, True)
    tiltMotor.run_until_stalled(-175, Stop.COAST, 40)

#turn the cube 90deg clockwise
def turn():
    tableMotor.run_angle(200, 270, Stop.BRAKE, True)


# ------ program start ------

ev3.light.on(Color.RED)
banner()
wait(1000)

# # request code
# unlocked = False
# while not unlocked:
#     if code_lock():
#         unlocked = True
#     else:
#         ev3.screen.clear()
#         ev3.screen.draw_text(ev3.screen.width/2, ev3.screen.height/2, 'falsch!!!', Color.BLACK, None)
#         ev3.speaker.set_speech_options('de', 'm5', 10, 30)
#         ev3.speaker.set_volume(100, '_all_')
#         ev3.speaker.say('Das wars komplett')

message('Reset Scan')
scanCal()

message('Reset Tilt')
tiltCal()

cubeCheck()

wait(1000)

scanCube()

wait(3000)



# ˇˇˇˇˇˇ hier wird der Würfel gelöst-hoffentlich ˇˇˇˇˇˇˇˇˇ
