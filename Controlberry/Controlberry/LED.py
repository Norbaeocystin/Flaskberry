'''
For control of LEDs, LED stripes

{'Command':'LED',
'Brightness':100,
'Name':<string>,
'State':<boolean>
}
'''
import json
from pymongo import MongoClient
import RPi.GPIO as GPIO
import time

#loads config file
json_data= open('config.json').read()
DATABASE = json.loads(json_data)
URI = DATABASE.get('URI')
DB = DATABASE.get('Database')

#setup mongodb
CONNECTION = MongoClient(URI, connect = False)
db = CONNECTION.get_database(DB)
Settings = db.Settings.find_one({"_id":0},{'_id':0})

#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

running = {}


def get_pin(name):
    '''
    LedName_0_ returns pin
    '''
    pin = name.replace('Name', 'Pin')
    return Settings.get(int(pin))


def get_light(name, brightness):
  '''
  pin number of GPIO pin, brightness = from 0 to 100
  '''
  pin = get_pin(name)
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(pin, GPIO.OUT)
  p = GPIO.PWN(pin,124)
  running.update({name:p})
  t = Thread(target = p.start, args = [brightness])
  t.start()
  
def get_stop(name):
  if running.get(name):
    running.get(name).stop()
