import fepd2in13
import epd4in2
from PIL import Image, ImageFont, ImageDraw
from smbpi.encoder import EncoderThread
import time
import RPi.GPIO as GPIO

HORIZONTAL_SCREEN = 0
VERTICAL_SCREEN =1

PIN_ENC_A = 20
PIN_ENC_B = 21

PIN_ENC_A2 = 12
PIN_ENC_B2 = 16

PIN_BUTTON = 23

def drawPoints(framebuf, epd, points):
    for point in points:
        y = point[0]
        x = point[1]
        framebuf[(x + y * epd.width) / 8] &= ~(0x80 >> (x % 8))

def calculateBoundingBox(points):
    minX=None
    minY=None
    maxX=None
    maxY=None
    for point in points:
        y=point[0]
        x=point[1]
        if (minX is None) or (x<minX):
            minX=x
        if (minY is None) or (y<minY):
            minY=y
        if (maxX is None) or (x>maxX):
            maxX=x
        if (maxY is None) or (y>maxY):
            maxY=y
    return (minX,minY,maxX,maxY)

def main():
    epd = epd4in2.EPD() #fepd2in13.EPD()
    epd.Init()

    print "width", epd.width, "height", epd.height

    GPIO.setup(PIN_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    last_button_state = GPIO.input(PIN_BUTTON)
    
    encoder = EncoderThread(encoders
                            =[{"pin_a": PIN_ENC_A, "pin_b": PIN_ENC_B, "min_pos": 0, "max_pos": epd.height-1},
                              {"pin_a": PIN_ENC_A2, "pin_b": PIN_ENC_B2, "min_pos": 0, "max_pos": epd.width-1, "invert": True}],
                            store_points = True)
    encoder.start()

    framebuf = [0xFF] * (epd.width * epd.height / 8)
    epd.DisplayPartialScott(framebuf, 0, 0, epd.width, epd.height)

    while (True):
        button_state = GPIO.input(PIN_BUTTON)
        if (button_state != last_button_state):
            if not button_state:
                framebuf = [0xFF] * (epd.width * epd.height / 8)
                epd.DisplayPartialScott(framebuf, 0, 0, epd.width, epd.height)
            last_button_state = button_state

        points = encoder.get_points()
        if points:
            points = [(p[0], p[1]) for p in points]
            drawPoints(framebuf, epd, points)
            (minX,minY,maxX,maxY) = calculateBoundingBox(points)
            #print "bounding", minX,minY,maxX,maxY
            minX=(minX/8)*8
            maxX=(maxX/8)*8

            #print "update", minX,minY,maxX+8,maxY+1
            epd.DisplayPartialScott(framebuf, minX, minY, maxX + 8, maxY + 1, black=False)
        time.sleep(0.01)

    epd.Sleep()

if __name__ == '__main__':
    main()
