# test gui
import sh1106 #display lib
from machine import Pin, I2C, PWM
from time import sleep
import gc
#import framebuf
print(gc.mem_free())
i2c = I2C(scl=Pin(5), sda=Pin(4), freq=400000) #i2c settings
display = sh1106.SH1106_I2C(128, 64, i2c, Pin(16), 0x3c) #Load the driver and set it to "display"
display.sleep(False) #activate display
display.fill(0) #clear display
display.rotate(flag=1) #rotate display 180°
display.fill(0)

#def load_image(filename):
  #  with open(filename, 'rb') as f:
    #    f.readline()
    #    f.readline()
    #    width, height = [int(v) for v in f.readline().split()]
    #    data = bytearray(f.read())
   # return framebuf.FrameBuffer(data, width, height, framebuf.MVLSB)

#humidity_pbm = load_image('humidity.pbm')
#display.blit(humidity_pbm, 24, 4)
#Display: x/w=0-127, y/h=0-63, 
#display.text('Time: ', 0, 48)
#display.hline(x, y, w, c)
#display.vline(x, y, h, c)
#display.line(x1, y1, x2, y2, c)
#display.rect(x, y, w, h, c)
#display.fill_rect(x, y, w, h, c)
#display.pixel(x, y[, c])
#display.scroll(xstep, ystep)
#display.text(s, x, y[, c]) #Text
#display.blit(fbuf, x, y[, key]) #Ueberlagert andere Symbole

#display.text('Bask v1.0', 30, 1) #Ueberschrift
#display.text('HOT: 25C', 0, 1)

#Display-FIX
display.vline(20, 0, 10, 1) #Trennlinie unterhalb Temp
display.hline(20, 10, 90, 1) #Trennlinie vor Temp
display.vline(109, 0, 10, 1) #Trennlinie vor Temp
display.text('25,1C 30,1%', 21, 0)
display.text('100,1h',21 ,55)
display.text('B', 0, 5) #Beschriftung Bodenfeuchte
display.rect(0, 15, 10, 48, 1) #Rahmen Bodenfeuchte
display.hline(0, 31, 12, 1) #vertikale Markierung Feuchte
display.hline(0, 47, 12, 1) #vertikale Markierung Feuchte
display.text('T', 119, 5) #Beschriftung Tank
display.rect(118, 15, 10, 48, 1) #Rahmen Tank
print('Display Fix')
#print(gc.mem_free())
#Display-Variabel
display.text('Status: ok', 20, 20, 1)
display.text('G', 105, 55) #Beschriftung Giessen
# p-run, leer, ok, INR

# Fuellstand Bodenfeuchte
#display.fill_rect(1, 16, 8, 7, 1) #Block 6 fill = feucht
#display.fill_rect(1, 24, 8, 7, 1) #Block 5 fill
#display.fill_rect(1, 32, 8, 7, 1) #Block 4 fill
#display.fill_rect(1, 40, 8, 7, 1) #Block 3 fill
#display.fill_rect(1, 48, 8, 7, 1) #Block 2 fill
display.fill_rect(1, 56, 8, 7, 1) #Block 1 fill = trocken
print('Fuellstand Boden')
#print(gc.mem_free())
# Fuellstand Tank
#display.fill_rect(119, 16, 8, 7, 1) #Block 6 fill = voll
#display.fill_rect(119, 24, 8, 7, 1) #Block 5 fill
display.fill_rect(119, 32, 8, 7, 1) #Block 4 fill
display.fill_rect(119, 40, 8, 7, 1) #Block 3 fill
display.fill_rect(119, 48, 8, 7, 1) #Block 2 fill
display.fill_rect(119, 56, 8, 7, 1) #Block 1 fill = fast leer
print('Fuellstand Tank')
display.show()
print(gc.mem_free())