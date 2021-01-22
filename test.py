import sh1106 #display lib
from time import sleep
i2c = I2C(scl=Pin(5), sda=Pin(4), freq=400000) #i2c settings
display = sh1106.SH1106_I2C(128, 64, i2c, Pin(16), 0x3c) #Load the driver and set it to "display"
display.sleep(False) #activate display
display.fill(0) #clear display
temp = 1
hum = 2
pres = 3
volt = 3
Hallo world

def display_output(): #print to display
  display.rotate(flag=1) #rotate display 180°
  display.fill(0)
  display.text('HOT: ' + str(temp), 0, 1)
  display.text('AIR: ' + str(hum), 0, 15)
  display.text('PRES: ' + str(pres), 0, 30)
  display.text('HUMI: ' + str(volt), 0, 45)
  display.show()

while True: #main body
  display_output() #calls function to print data to display
  sleep(60)