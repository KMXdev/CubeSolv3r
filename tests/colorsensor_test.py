from pybricks.hubs import EV3Brick
from pybricks.ev3devices import ColorSensor
from pybricks.parameters import Port, Stop, Direction, Button, Color

# font definitions
bigFont = Font(size = 25, bold = True)
smallFont = Font(size = 18)

# Lego® Mindstorms® EV3-Brick object
ev3 = EV3Brick()

colorSensor = ColorSensor(Port.S2)

# display any given text to the EV3's screen
def print_rgb(rgb):
    ev3.screen.clear()
    ev3.screen.set_font(bigFont)
    ev3.screen.draw_text(1, 1, rgb[0], Color.BLACK, None)
    ev3.screen.draw_text(ev3.screen.height/2, 1, rgb[0], Color.BLACK, None)
    ev3.screen.draw_text(ev3.screen.height-5, 1, rgb[0], Color.BLACK, None)

def cc_sensor():
    ev3.screen.clear()
    ev3.screen.draw_text(0, 0, 'Calibrating', Color.BLACK, None)
    wait(1000)
    colorSensor.calibrate_white()
    wait(1000)



wait(1000)
cc_sensor()

while True:
    raw = colorSensor.rgb()
    print_rgb(raw)
    wait(100)
