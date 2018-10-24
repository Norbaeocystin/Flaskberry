'''
For control of LEDs, LED stripes
'''
from threading import Thread
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

running = {}

def get_light(name, pin, brightness):
  '''
  pin number of GPIO pin, brightness = from 0 to 100
  '''
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(pin, GPIO.OUT)
  p = GPIO.PWN(pin,124)
  running.update({name:p})
  t = Thread(target = p.start, args = brightness)
  t.start()
  
def stop(name):
  if running.get(name):
    running.get(name).stop()
