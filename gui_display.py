# test gui
import sh1106 #display lib
from machine import Pin, I2C, PWM
from time import sleep

i2c = I2C(scl=Pin(5), sda=Pin(4), freq=400000) #i2c settings
display = sh1106.SH1106_I2C(128, 64, i2c, Pin(16), 0x3c) #Load the driver and set it to "display"

display.sleep(False) #activate display
display.fill(0) #clear display
display.rotate(flag=1) #rotate display 180°
display.fill(0)

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

display.text('Basilikum v1.0', 0, 1) #Ueberschrift
display.hline(0, 10, 113, 1) #Trennlinie
#display.text('HOT: 25C', 0, 1)
display.text('25,1C', 2, 13)
display.text('30,1%', 2, 26)
display.text('100,1h',2 ,39)



display.hline(0, 52, 113, 1) #Trennlinie oberhalb Feuchte
display.text('B', 0, 55) #Beschriftung Bodenfeuchte
display.rect(10, 54, 90, 10, 1) #Rahmen Bodenfeuchte

display.vline(112, 11, 41, 1) #vertikale rechts
display.vline(0, 11, 41, 1) #vertikale links

display.text('T', 118, 0) #Beschriftung Tank
display.rect(118, 16, 10, 48, 1) #Rahmen Tank
display.fill_rect(119, 17, 8, 6, 1) #Block 6 fill = voll
display.fill_rect(119, 25, 8, 6, 1) #Block 5 fill
display.fill_rect(119, 33, 8, 6, 1) #Block 4 fill
display.fill_rect(119, 41, 8, 6, 1) #Block 3 fill
display.fill_rect(119, 49, 8, 6, 1) #Block 2 fill
display.fill_rect(119, 57, 8, 6, 1) #Block 1 fill = fast leer

display.text('G', 105, 55) #Beschriftung Giessen

display.show()