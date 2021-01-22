#ESP8266/Wemos D1 mini v3, Date:2020-12-28,v0.0.1
#Micropython v1.13, immer ESPins benutzen, project: plant care, owner: MHu

from machine import Pin, I2C, PWM
import time
from time import sleep
import BME280 #sensor t,c,hum lib
import sh1106 #display lib
import ads1x15 #Capacitive Soil Sensor/CSensor

class MyMachine:
  # physical interfaces
  i2c = None
  display = None
  bme = None
  pump = None
  pump_reverse = None
  button = None
  adc = None
  # sensor variables
  temp = None
  hum = None
  pres = None
  volt = None
  water_storage = None
  water_storage_max = 1.2
  time_current = None
  epoche = 0 #Epoche
  # fixed values
  addr = 0x48
  gain = 1
  time_start = time.ticks_ms() #start Wert des internen Zählers
  #config
  i2c = I2C(scl=Pin(5), sda=Pin(4), freq=400000) #i2c settings
  display = sh1106.SH1106_I2C(128, 64, i2c, Pin(16), 0x3c) #Load the driver and set it to "display"
  display.sleep(False) #activate display
  display.fill(0) #clear display
  bme = BME280.BME280(i2c=i2c) #sensor function 
  pumpe = PWM(Pin(14), freq=0, duty=0) #create PWM objekt and configure pump forward
  pumpe_reverse = PWM(Pin(12), freq=0, duty=0) #create PWM objekt and configure pump backwards
  button = Pin(0, Pin.IN, Pin.PULL_UP)  #initialize button
  addr = 0x48
  gain = 1
  adc = ads1x15.ADS1115(i2c, addr, gain) #create analog-digtial converter object to read analog humidity sensor
  i = 0
  start = time.ticks_ms() #start Wert des internen Zaehlers
  autosetinterval = 25200 #counter
  reset = 0 #reset for time counter
  #epoche = 0 #Epoche
  #functions

def epochetime(): #Checkt die Epoche
  global epoche
  epoche = 0
  current = time.ticks_ms()/1000 #speichert aktuelle Zeit
  if time.ticks_diff(time.ticks_ms(), start) < 0:
    epoche = epoche + 1
    start = time.ticks_ms() #reset start
    print('Period', epoche) #1x Epoche max. ~298h - derzeit unklar, muss getestet werden
    #convert ticks_ms -> hours
    #compare if hours increased by 48h -> freigabe giessen
    current = time.ticks_ms()/1000 #in seconds
  if current > autosetinterval:
    reset = reset +1
    if reset >= 7:
      reset = 0
      return(1)
  return(0)
def meassure_all_sensors(): #Measure all Sensors
  global bme, temp, hum, pres, volt
  temp = bme.temperature #bme sensor temp
  hum = bme.humidity #bme sensor humidity
  pres = bme.pressure #bme sensor air pressure
  volt = adc.read(0, 0) #read voltage level from soil-sensor via ADC
  print('Temperature: ', temp) #check
  print('Humidity: ', hum) #check
  print('Pressure: ', pres) #check
  sleep(0.5)

def water_storage(): #speichert den aktuellen Tankinhalt
  storageFull = 1.2 #max. 1,2 Liter
  storageCurrent = 0 #Startwert
  print(storageCurrent, storageFull)
  
def button_check(): #check for user input, button pressed y/n
  #button pressed = 0, not pressed = 1
  #button.value()
  sleep(1)
  print(button.value())

def pump_driver(): #run water pump
  #Pump Driver Pin A-IA ->D5/ESPin: 14 (Pumpe vorwaerts)
  #Pump Driver Pin A-IB ->D6/ESPin: 12 (Pumpe rueckwaerts) / nicht benoetigt
  #freqency must be between 1Hz and 1kHz and duty cycle 0 (all off ->0V) and 1023 (all on ->12V)
  print('Pumpe Ein')
  pumpe = PWM(Pin(14), freq=100, duty=300) #~30% Voltage to pump
  sleep(30) #pump runtime, adjust to pump speed, total volume 200ml per activation
  pumpe.deinit() #Pumpe aus
  print('Pumpe Aus')

def validate_sensor(): #activate pump if time and sensor value are true
  pass
  
def display_output(): #print to display
  display.fill(0)
  display.text('HOT: ' + str(temp), 0, 1)
  display.text('AIR: ' + str(hum), 0, 15)
  display.text('PRES: ' + str(pres), 0, 30)
  display.text('HUMI: ' + str(volt), 0, 45)
  display.show()

while True: #main body
  meassure_all_sensors() #calls function to meassure sensors
  epochetime()
  #button_check() #checks if button is pressed
  #water_storage() #checks if sufficient water is left in tank
  
  # if storageCurrent > 0.2 AND time
  # call pump_driver()
  
  display_output() #calls function to print data to display
  sleep(60)
  











