import time

autosetinterval = 25200
reset = 0
# 1h = 3 600 s
# 7h = 25 200 s, reset after 7h45
# 48 h = 7 resets
while True:
  current = time.ticks_ms()/1000 #in seconds
  print(current)
  time.sleep(1)
  if current > autosetinterval:
    reset = reset +1
    if reset >= 7:
      reset = 0
      print('7h')

