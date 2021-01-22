import time #ESP8266/Wemos D1 mini v3, Date:2020-12-28,v0.0.1
from machine import Pin, I2C, PWM #Micropython v1.13, immer ESPins benutzen, project: plant care, owner: MHu
import BME280 #sensor t,c,hum lib
import sh1106 #display lib
import ads1x15 #Capacitive Soil Sensor/CSensor

class MyMachine:
  addr = 0x48
  gain = 1
  adc = None
  
  def __init__(self):
    self.i2c = I2C(scl=Pin(5), sda=Pin(4), freq=400000) #i2c settings
    self.display = sh1106.SH1106_I2C(128, 64, self.i2c, Pin(16), 0x3c) #Load the driver and set it to "display"
    self.bme = BME280.BME280(i2c=self.i2c) #sensor function
    self.pump = PWM(Pin(14), freq=0, duty=0) #create PWM objekt and configure pump forward
    #self.pump_reverse = PWM(Pin(12), freq=0, duty=0) #create PWM objekt and configure pump backwards
    #self.button = Pin(0, Pin.IN, Pin.PULL_UP) #initialize button
    self.adc = ads1x15.ADS1115(self.i2c, self.addr, self.gain) #create analog-digtial converter object to read analog humidity sensor
    self.time_start = time.ticks_ms()/1000 #Sekunden
    self.autosetinterval = time.ticks_ms()/1000 + 25200 #counter
    self.time_current = 0
    self.time_start = 0
    self.reset = 0
    self.epoche = 0
    self.water_storage = 1.2
    self.water_use = 0
    self.water_status = True
    self.button = Pin(0, Pin.IN, Pin.PULL_UP)
    self.button.irq(trigger=Pin.IRQ_FALLING, handler=self.handle_interrupt)
    self.soil_dry = 20000 #CSensor >20000 /Annahme Test offen
    self.soil_ok = 15000 #CSensor 15000 bis 10000 /Annahme Test offen
    self.soil_humid = 10000 #CSensor 250 - bis 10000 /Annahme Test offen
    #self.soil_humidity = None
    self.activateAndClearDisplay()
    
  def activateAndClearDisplay(self):
    self.display.sleep(False) #activate display
    self.display.fill(0) #clear display

  def readLatestSensorData(self):
    self.temp = self.bme.temperature #bme sensor temp
    self.hum = self.bme.humidity #bme sensor humidity
    self.pres = self.bme.pressure #bme sensor air pressure
    self.volt = self.adc.read(0, 0) #read voltage level from soil-sensor via ADC

  def validate_sensor(self): #activate pump if time and sensor value are true
    if self.volt >= self.soil_dry:
      self.soil_humidity="dry  "
      return(True)
    elif self.volt <= self.soil_dry and self.volt >= self.soil_ok:
      self.soil_humidity="okey "
      return(False)
    elif self.volt <= self.soil_dry and self.volt >= self.soil_humid:
      self.soil_humidity="humid"
      return(False)
    
  def displaySensorData(self): #print to display
    self.display.rotate(flag=1) #rotate display 180°
    self.display.fill(0)
    self.display.text('HOT: ' + str(self.temp), 0, 1)
    self.display.text('AIR: ' + str(self.hum), 0, 12)
    self.display.text('PRES: ' + str(self.pres), 0, 24)
    self.display.text('HUMI: ' + str(self.volt), 0, 36)
    self.display.text('Time: ' + str(self.time_current/60/60), 0, 48)
    self.display.show()

  def runPump(self):
    #Pump Driver Pin A-IA ->D5/ESPin: 14 (Pumpe vorwaerts)
    #Pump Driver Pin A-IB ->D6/ESPin: 12 (Pumpe rueckwaerts) / nicht benoetigt
    #freqency must be between 1Hz and 1kHz and duty cycle 0 (all off ->0V) and 1023 (all on ->12V)
    print('Pumpe Ein')
    self.pump = PWM(Pin(14), freq=100, duty=300) #~30% Voltage to pump
    time.sleep(25) #pump runtime, adjust to pump speed, total volume 200ml per activation
    self.pump.deinit() #Pumpe aus
    print('Pumpe Aus')
    return()

  def checkTime(self):
    self.time_current = time.ticks_ms()/1000 #Sekunden
    time_diff = time.ticks_diff(self.time_current, self.time_start)
    if time_diff < 0:
        self.epoche += 1
        print('Period', self.epoche) #1x Epoche max. ~298h - derzeit unklar, muss getestet werden
        self.time_start = time.ticks_ms()/1000 #reset start
        self.autosetinterval = 25200 #reset autointerval
    if self.time_current > self.autosetinterval:
        self.reset += 1
        self.autosetinterval += 25200 #incraese intervall
        if self.reset >= 7:
            self.reset = 0
            return(True)
        return(False)

  def water(self):
    if self.water_storage - 0.2 < 0:
      print('tank is empty')
      # call function to ask user for new water
      self.water_status = False
      return(self.water_status)
    self.water_storage = self.water_storage - 0.2
    print('water ok')
    self.water_status = True
    return(self.water_status)

  def handle_interrupt(self, pin): #if button is pressed, function is called
    self.pump.deinit() #Pumpe aus
    print('button pressed')
    time.sleep(2)
    return()

m = MyMachine()

while True: #main loop
  m.readLatestSensorData() #calls function to measure sensors
  cT = m.checkTime() #True=timewindow for water, False=wait
  vs = m.validate_sensor() #Prüft Sensorwerte 
  w = m.water() #checks tank for water status
  
  if cT == True and vs == True and w == True:
    print('Water plant')
    m.runPump() #start pump
  
  m.displaySensorData() #show data on display

  if m.checkTime() is True:
    print('True')
  else:
    print('False, time: ' + str(m.time_current/60/60) + ' ' + str(m.reset) + ' ' + str(m.autosetinterval/60/60)) #Stunden
    time.sleep(2)
  time.sleep(2)

