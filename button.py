from machine import Pin
from time import sleep
#import d1_mini
button = Pin(0, Pin.IN, Pin.PULL_UP)
button.irq(trigger=Pin.IRQ_FALLING, handler=handle_interrupt)

def handle_interrupt(pin):
  print('pressed')
# Hold the button down and then run that line again

while True:
  #button.value()
  sleep(1)
  print(button.value())
