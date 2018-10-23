'''
date: Oktober 2018
Short code to light up LED for defined time
'''
import RPi.GPIO as GPIO
import time
from pymongo import MongoClient

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
#set GPIO Pin
LED = SENSORS.get('Led') #21

def light(interval = 10):
    '''
    will light LED for 10 seconds rr for defined time 
    '''
    try:
    	interval = float(interval)
    except ValueError:
    	interval = 10
    GPIO.setup(LED, GPIO.OUT)
    GPIO.output(LED,True)
    time.sleep(interval)
    GPIO.output(LED,False)
