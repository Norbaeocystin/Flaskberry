'''
For control of LEDs, LED stripes
'''

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

def get_light(pin, brightness):
  '''
  pin number of GPIO pin, brightness = from 0 to 100
  '''
  GPIO.setup(pin, GPIO.OUT)
  GPIO.PWN(pin,124).start(brightness)
