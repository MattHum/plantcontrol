#ESP8266/Wemos D1 mini v3, Date:2020-12-28,v0.0.1
#Micropython v1.13, immer ESPins benutzen, project: plant care, owner: MHu

from machine import Pin, I2C, PWM
from time import sleep
import time
import BME280 #sensor t,c,hum lib
import sh1106 #display lib
import ads1x15 #Capacitive Soil Sensor/CSensor
  
class MyMachine:
 

  def __init__(self):
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
    time_start = time.ticks_ms() #start Wert des internen Zaehlers
    
    self.i2c = I2C(scl=Pin(5), sda=Pin(4), freq=400000) #i2c settings
    self.display = sh1106.SH1106_I2C(128, 64, i2c, Pin(16), 0x3c) #Load the driver and set it to "display"
    self.bme = BME280.BME280(i2c=i2c) #sensor function
    self.pump = PWM(Pin(14), freq=0, duty=0) #create PWM objekt and configure pump forward
    self.pump_reverse = PWM(Pin(12), freq=0, duty=0) #create PWM objekt and configure pump backwards
    self.button = Pin(0, Pin.IN, Pin.PULL_UP) #initialize button
    self.adc = ads1x15.ADS1115(i2c, addr, gain) #create analog-digtial converter object to read analog humidity sensor

    activateAndClearDisplay()

  def activateAndClearDisplay(self):
    display.sleep(False) #activate display
    display.fill(0) #clear display

  def readLatestSensorData(self):
    self.temp = bme.temperature #bme sensor temp
    self.hum = bme.humidity #bme sensor humidity
    self.pres = bme.pressure #bme sensor air pressure
    self.volt = adc.read(0, 0) #read voltage level from soil-sensor via ADC

  def displaySensorData(self): #print to display
    self.display.fill(0)
    self.display.text('HOT: ' + str(self.temp), 0, 1)
    self.display.text('AIR: ' + str(self.hum), 0, 15)
    self.display.text('PRES: ' + str(self.pres), 0, 30)
    self.display.text('HUMI: ' + str(self.volt), 0, 45)
    self.display.show()

  def runPump(self, duration):
    #Pump Driver Pin A-IA ->D5/ESPin: 14 (Pumpe vorwaerts)
    #Pump Driver Pin A-IB ->D6/ESPin: 12 (Pumpe rueckwaerts) / nicht benoetigt
    #freqency must be between 1Hz and 1kHz and duty cycle 0 (all off ->0V) and 1023 (all on ->12V)
    print('Pumpe Ein')
    self.pump = PWM(Pin(14), freq=100, duty=300) #~30% Voltage to pump
    sleep(duration) #pump runtime, adjust to pump speed, total volume 200ml per activation
    self.pumpe.deinit() #Pumpe aus
    print('Pumpe Aus')

  def buttonCheck(self):
    sleep(1)
    print(self.button.value())

  def checkTime(self):
    self.time_current = time.ticks_ms()
    time_diff = time.ticks_diff(self.time_current, self.time_start)
    if (time_diff < 0):
      self.epoche += 1
      print('Period', epoche) #1x Epoche max. ~298h - derzeit unklar, muss getestet werden
      #convert ticks_ms -> hours
      #compare if hours increased by 48h -> freigabe giessen

def validate_sensor(self): #activate pump if time and sensor value are true
  pass


m = MyMachine()

while True: #main loop
  m.checkTime()
  m.readLatestSensorData() #calls function to measure sensors
  m.displaySensorData()
  #button_check() #checks if button is pressed
  #water_storage() #checks if sufficient water is left in tank

  # if storageCurrent > 0.2 AND time
  # call pump_driver()

  sleep(60)



