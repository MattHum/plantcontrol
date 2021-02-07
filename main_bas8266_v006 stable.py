from time import sleep, ticks_ms, ticks_diff#ESP8266/Wemos D1 mini v3, Date:2020-12-28,v0.0.1
from machine import Pin, I2C, PWM #Micropython v1.13, immer ESPins benutzen, project: plant care, owner: MHu
from BME280 import BME280 #sensor t,c,hum lib
#from sh1106 import SH1106, SH1106_I2C #display lib
import sh1106
from ads1x15 import ADS1115 #Capacitive Soil Sensor/CSensor
import gc
gc.collect()

class MyMachine:
  addr = 0x48
  gain = 1
  adc = None
  def __init__(self):
    self.i2c = I2C(scl=Pin(5), sda=Pin(4), freq=400000) #i2c settings
    self.display = sh1106.SH1106_I2C(128, 64, self.i2c, Pin(16), 0x3c) #Load the driver and set it to "display"
    self.bme = BME280(i2c=self.i2c) #sensor function
    self.pump = PWM(Pin(14), freq=0, duty=0) #create PWM objekt and configure pump forward
    #self.pump_reverse = PWM(Pin(12), freq=0, duty=0) #create PWM objekt and configure pump backwards
    self.adc = ADS1115(self.i2c, self.addr, self.gain) #create analog-digtial converter object to read analog humidity sensor
    self.time_start = ticks_ms()/1000 #Sekunden
    self.autosetinterval = ticks_ms()/1000 + 3 #counter
    self.time_current = 0
    self.reset = 0
    self.epoche = 0
    self.water_storage = 1.2
    self.water_status = True
    self.button = Pin(0, Pin.IN, Pin.PULL_UP) #initialize button
    #self.button.irq(trigger=Pin.IRQ_FALLING, handler=self.handle_interrupt)
    self.soil_dry = 20000 #CSensor >20000 /Annahme Test offen
    self.soil_ok = 15000 #CSensor 15000 bis 10000 /Annahme Test offen
    self.soil_humid = 10000 #CSensor 250 - bis 10000 /Annahme Test offen
    self.soil_humidity = None
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
    #self.display.text('HOT: ' + str(self.temp), 0, 1)
    #self.display.text('AIR: ' + str(self.hum), 0, 12)
    #self.display.text('PRES: ' + str(self.pres), 0, 24)
    #self.display.text('HUMI: ' + str(self.volt), 0, 36)
    self.display.text('Time: ' + str(self.time_current/60/60), 0, 48)
    #self.display.text('Test', 0, 48)
    self.display.show()
    gc.collect()

  def runPump(self):
    #Pump Driver Pin A-IA ->D5/ESPin: 14 (Pumpe vorwaerts)
    #Pump Driver Pin A-IB ->D6/ESPin: 12 (Pumpe rueckwaerts) / nicht benoetigt
    #freqency must be between 1Hz and 1kHz and duty cycle 0 (all off ->0V) and 1023 (all on ->12V)
    print('Pumpe Ein')
    self.pump = PWM(Pin(14), freq=100, duty=300) #~30% Voltage to pump
    sleep(20) #pump runtime, adjust to pump speed, total volume 200ml per activation
    self.pump.deinit() #Pumpe aus
    gc.collect()
    print('Pumpe Aus')
    
  def checkTime(self):
    self.time_current = ticks_ms()/1000 #Sekunden
    time_diff = ticks_diff(self.time_current, self.time_start)
    if time_diff < 0:
        self.epoche += 1
        print('Period', self.epoche) #1x Epoche max. ~298h - derzeit unklar, muss getestet werden
        self.time_start = ticks_ms()/1000 #reset start
        self.autosetinterval = 3 #reset autointerval = 7h
    if self.time_current > self.autosetinterval:
        self.reset += 1 #alle 7h reset+1
        print(self.reset)
        self.autosetinterval += 3 #incraese intervall +7h
        if self.reset > 5: #alle 6x7=42h
            self.reset = 0
            return(True)
        return(False)
  
  def water(self):
    if self.water_storage - 0.2 < 0:
      print('tank is empty')
      # call function to ask user for new water
      self.water_status = False
      return(False)
    self.water_storage = self.water_storage - 0.2
    print('water ok')
    self.water_status = True
    return(True)

  def handle_interrupt(self, pin): #if button is pressed, function is called
    self.pump.deinit() #Pumpe aus
    print('button pressed')
    sleep(2)
    return()

m = MyMachine()

while True: #main loop
  m.readLatestSensorData() #calls function to measure sensors
  if (m.checkTime() == True and m.validate_sensor() == True and m.water() == True):
    print('Water plant')
    m.runPump() #start pump
  m.displaySensorData() #show data on display
    
  gc.collect()
  print(gc.mem_free())
  sleep(5)
