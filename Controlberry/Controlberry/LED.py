'''
For control of LEDs, LED stripes
'''

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

running = None

def get_light(pin, brightness):
  '''
  pin number of GPIO pin, brightness = from 0 to 100
  '''
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(pin, GPIO.OUT)
  p = GPIO.PWN(pin,124)
  running = p
  t = Thread(target = p.start, args = brightness)
  t.start()
  
def stop():
  if running:
    running.stop()
