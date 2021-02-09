import sh1106 #display lib
from machine import Pin, I2C, PWM
from time import sleep
import gc

#import framebuf
#print(gc.mem_free())
i2c = I2C(scl=Pin(5), sda=Pin(4), freq=400000) #i2c settings
display = sh1106.SH1106_I2C(128, 64, i2c, Pin(16), 0x3c) #Load the driver and set it to "display"
display.sleep(False) #activate display
display.fill(0) #clear display
display.rotate(flag=1) #rotate display 180°
display.fill(0)

temp = 20.20120
'%.1f' % temp
temp2 = 0.0012
temp3 = temp - temp2
print(temp3)
press = 12

var = "T {:3.1f} ".format(temp)
print(var)
display.text(var, 21, 0)
test = 1.0
thisdict =	{1.2 : 16, 1 : 24, 0.8 : 32, 0.6 : 40, 0.4 : 48, 0.2 : 56, 0 : 63}
print(thisdict[test])


#display.text('Time: ' + str(temp/60/60), 0, 48)
display.show()
print(gc.mem_free())