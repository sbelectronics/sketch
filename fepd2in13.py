##
 #  @filename   :   fepd2in13.py
 #  @brief      :   Implements for Dual-color e-paper library
 #  @author     :   Yehui from Waveshare
 #
 #  Copyright (C) Waveshare     July 24 2017
 #
 # Permission is hereby granted, free of charge, to any person obtaining a copy
 # of this software and associated documnetation files (the "Software"), to deal
 # in the Software without restriction, including without limitation the rights
 # to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 # copies of the Software, and to permit persons to  whom the Software is
 # furished to do so, subject to the following conditions:
 #
 # The above copyright notice and this permission notice shall be included in
 # all copies or substantial portions of the Software.
 #
 # THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 # IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 # FITNESS OR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 # AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 # LIABILITY WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 # OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 # THE SOFTWARE.
 #
import epdif
from PIL import Image
import RPi.GPIO as GPIO

# Display resolution
WIDTH       = 104
HEIGHT      = 212

IMAGE_ROTATE_0   = 0
IMAGE_ROTATE_90  = 1
IMAGE_ROTATE_180 = 2
IMAGE_ROTATE_270 = 3

class EPD:
    def __init__(self):
        self.Reset_pin = epdif.RST_PIN
        self.dc_pin = epdif.DC_PIN
        self.busy_pin = epdif.BUSY_PIN
        self.width = WIDTH
        self.height = HEIGHT
        
    lut_vcomDC = [  
        0x00, 0x08, 0x00, 0x00, 0x00, 0x02,
        0x60, 0x28, 0x28, 0x00, 0x00, 0x01,
        0x00, 0x14, 0x00, 0x00, 0x00, 0x01,
        0x00, 0x12, 0x12, 0x00, 0x00, 0x01,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00,
    ]

    lut_ww = [  
        0x40, 0x08, 0x00, 0x00, 0x00, 0x02,
        0x90, 0x28, 0x28, 0x00, 0x00, 0x01,
        0x40, 0x14, 0x00, 0x00, 0x00, 0x01,
        0xA0, 0x12, 0x12, 0x00, 0x00, 0x01,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    ]

    lut_bw = [  
        0x40, 0x17, 0x00, 0x00, 0x00, 0x02,
        0x90, 0x0F, 0x0F, 0x00, 0x00, 0x03,
        0x40, 0x0A, 0x01, 0x00, 0x00, 0x01,
        0xA0, 0x0E, 0x0E, 0x00, 0x00, 0x02,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    ]

    lut_wb = [
        0x80, 0x08, 0x00, 0x00, 0x00, 0x02,
        0x90, 0x28, 0x28, 0x00, 0x00, 0x01,
        0x80, 0x14, 0x00, 0x00, 0x00, 0x01,
        0x50, 0x12, 0x12, 0x00, 0x00, 0x01,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    ]

    lut_bb = [ 
        0x80, 0x08, 0x00, 0x00, 0x00, 0x02,
        0x90, 0x28, 0x28, 0x00, 0x00, 0x01,
        0x80, 0x14, 0x00, 0x00, 0x00, 0x01,
        0x50, 0x12, 0x12, 0x00, 0x00, 0x01,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    ]
    
    lut_vcom1 = [  
        0x00, 0x19, 0x01, 0x00, 0x00, 0x01,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00,
    ]

    lut_ww1 = [  
        0x00, 0x19, 0x01, 0x00, 0x00, 0x01,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    ]

    lut_bw1 = [  
        0x80, 0x19, 0x01, 0x00, 0x00, 0x01,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    ]

    lut_wb1 = [
        0x40, 0x19, 0x01, 0x00, 0x00, 0x01,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    ]

    lut_bb1 = [ 
        0x00, 0x19, 0x01, 0x00, 0x00, 0x01,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    ]

    def digital_write(self, pin, value):
        epdif.epd_digital_write(pin, value)

    def digital_read(self, pin):
        return epdif.epd_digital_read(pin)

    def delay_ms(self, delaytime):
        epdif.epd_delay_ms(delaytime)

    def SendCommand(self, command):
        self.digital_write(self.dc_pin, GPIO.LOW)
        # the parameter type is list but not int
        # so use [command] instead of command
        epdif.spi_transfer([command])

    def SendData(self, data):
        self.digital_write(self.dc_pin, GPIO.HIGH)
        # the parameter type is list but not int
        # so use [data] instead of data
        epdif.spi_transfer([data])
        
    def WaitUntilIdle(self):
        while(self.digital_read(self.busy_pin) == 0):      # 0: idle, 1: busy
            self.SendCommand(0x71)
            self.delay_ms(100)

    def Reset(self):
        self.digital_write(self.Reset_pin, GPIO.LOW)         # module Reset
        self.delay_ms(200)
        self.digital_write(self.Reset_pin, GPIO.HIGH)
        self.delay_ms(200)
        
    def Init(self):
        if (epdif.epd_init() != 0):
            return -1
        self.Reset()

        self.SendCommand(0x01)	#POWER SETTING
        self.SendData(0x03)
        self.SendData(0x00)
        self.SendData(0x2b)
        self.SendData(0x2b)
        self.SendData(0x03)

        self.SendCommand(0x06)	#boost soft start
        self.SendData(0x17)     #A
        self.SendData(0x17)     #B
        self.SendData(0x17)     #C

        self.SendCommand(0x04)
        # self.WaitUntilIdle()

        self.SendCommand(0x00)	#panel setting
        self.SendData(0xbf)    # LUT from OTP,128x296
        self.SendData(0x0d)     #VCOM to 0V fast

        self.SendCommand(0x30)	#PLL setting
        self.SendData(0x3a)     # 3a 100HZ   29 150Hz 39 200HZ	31 171HZ

        self.SendCommand(0x61)	#resolution setting
        self.SendData(WIDTH)
        self.SendData((HEIGHT >> 8) & 0xff)
        self.SendData(HEIGHT& 0xff)

        self.SendCommand(0x82)	#vcom_DC setting
        self.SendData(0x28)

        # self.SendCommand(0X50)			#VCOM AND DATA INTERVAL SETTING
        # self.SendData(0xb7)		#WBmode:VBDF 17|D7 VBDW 97 VBDB 57		WBRmode:VBDF F7 VBDW 77 VBDB 37  VBDR B7
        return 0
      
    def SetFullReg(self):
        self.SendCommand(0x82)
        self.SendData(0x00)
        self.SendCommand(0X50)
        self.SendData(0x97)
        
        self.SendCommand(0x20)         # vcom
        for count in range(0, 44):
            self.SendData(self.lut_vcomDC[count])
        self.SendCommand(0x21)         # ww --
        for count in range(0, 42):
            self.SendData(self.lut_ww[count])
        self.SendCommand(0x22)         # bw r
        for count in range(0, 42):
            self.SendData(self.lut_bw[count])
        self.SendCommand(0x23)         # wb w
        for count in range(0, 42):
            self.SendData(self.lut_wb[count])
        self.SendCommand(0x24)         # bb b
        for count in range(0, 42):
            self.SendData(self.lut_bb[count])
    
    def SetPartReg(self):
        self.SendCommand(0x82)
        self.SendData(0x03)
        self.SendCommand(0X50)
        self.SendData(0x47)
        
        self.SendCommand(0x20)         # vcom
        for count in range(0, 44):
            self.SendData(self.lut_vcom1[count])
        self.SendCommand(0x21)         # ww --
        for count in range(0, 42):
            self.SendData(self.lut_ww1[count])
        self.SendCommand(0x22)         # bw r
        for count in range(0, 42):
            self.SendData(self.lut_bw1[count])
        self.SendCommand(0x23)         # wb w
        for count in range(0, 42):
            self.SendData(self.lut_wb1[count])
        self.SendCommand(0x24)         # bb b
        for count in range(0, 42):
            self.SendData(self.lut_bb1[count])

    def TurnOnDisplay(self):
        self.SendCommand(0x12)
        self.delay_ms(10)

        self.WaitUntilIdle()

    def Clear(self):
        self.SendCommand(0x10)
        for i in range(0, self.width * self.height / 8):
            self.SendData(0x00)
        self.delay_ms(10)
        
        self.SendCommand(0x13)
        for i in range(0, self.width * self.height / 8):
            self.SendData(0xFF)
        self.delay_ms(10)
        
        self.SetFullReg()
        self.TurnOnDisplay()
        
    def GetFrameBuffer(self, image):
        buf = [0] * (self.width * self.height / 8)
        # Set buffer to value of Python Imaging Library image.
        # Image must be in mode 1.
        image_monocolor = image.convert('1')
        imwidth, imheight = image_monocolor.size
        '''
        if imwidth != self.width or imheight != self.height:
            raise ValueError('Image must be same dimensions as display \
                ({0}x{1}).' .format(self.width, self.height))
        '''
        pixels = image_monocolor.load()
        for y in range(self.height):
            for x in range(self.width):
                # Set the bits for the column of pixels at the current position.
                if pixels[x, y] != 0:
                    buf[(x + y * self.width) / 8] |= 0x80 >> (x % 8)
        return buf    
        
    def DisplayFull(self, frame_buffer):    
        if (Image == None):
			return
            
        self.SendCommand(0x10)
        for i in range(0, self.width * self.height / 8):
            self.SendData(0x00)
        self.delay_ms(10)
        
        self.SendCommand(0x13)
        for i in range(0, self.width * self.height / 8):
            self.SendData(frame_buffer[i])
        self.delay_ms(10)
        
        self.SetFullReg()
        self.TurnOnDisplay()
        
    def DisplayPartial(self, frame_buffer, Xstart, Ystart, Xend, Yend):   
        if (Image == None):
			return
            
        self.SetPartReg()
        self.SendCommand(0x91)
        self.SendCommand(0x90)
        self.SendData(Xstart)
        self.SendData(Xend - 1)

        self.SendData(Ystart / 256)
        self.SendData(Ystart % 256)
        self.SendData(Yend / 256)
        self.SendData(Yend % 256 - 1)
        self.SendData(0x28)

        self.SendCommand(0x10)
        for i in range(0, self.width * self.height / 8):
            # print(frame_buffer[i],'%d','0x10')
            self.SendData(frame_buffer[i])
        self.delay_ms(10)
        
        self.SendCommand(0x13)
        for i in range(0, self.width * self.height / 8):
            #print(~frame_buffer[i],'%d','0x13')
            self.SendData(~frame_buffer[i])
        self.delay_ms(10)
        
        #self.SetFullReg()        
        self.TurnOnDisplay()

    def DisplayPartialScott(self, frame_buffer, Xstart, Ystart, Xend, Yend):
        if (Image == None):
            return

        self.SetPartReg()
        self.SendCommand(0x91)
        self.SendCommand(0x90)
        self.SendData(Xstart)
        self.SendData(Xend - 1)

        self.SendData(Ystart / 256)
        self.SendData(Ystart % 256)
        self.SendData(Yend / 256)
        self.SendData(Yend % 256 - 1)
        self.SendData(0x28)

        width = Xend-Xstart
        height = Yend-Ystart

        pitch = self.width/8

        self.SendCommand(0x10)
        for y in range(0, height):
            for x in range(0, width/8):
                self.SendData(frame_buffer[x+((y+Ystart)*pitch)])
        self.delay_ms(10)

        self.SendCommand(0x13)
        for y in range(0, height):
            for x in range(0, width/8):
                self.SendData(~frame_buffer[x+((y+Ystart)*pitch)])
        self.delay_ms(10)

        # self.SetFullReg()
        self.TurnOnDisplay()

    # after this, call epd.init() to awaken the module
    def Sleep(self):
        self.SendCommand(0X50)
        self.SendData(0xf7)
        self.SendCommand(0X02)         #power off
        self.SendCommand(0X07)         #deep sleep  
        self.SendData(0xA5)

### END OF FILE ###




























