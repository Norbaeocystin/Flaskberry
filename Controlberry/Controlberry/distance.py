'''
date: Oktober 2018
code to control ultrasound sensor HC-SR04
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

def get_pins(name):
    '''
    UltraSoundName_0_ returns UltraSoundEcho_0_ and UltraSoundTrigger_0_ 
    '''
    Echo = name.replace('Name', 'Echo')
    Trigger = name.replace('Name', 'Trigger')
    return {'Echo':Settings.get(Echo),'Trigger':Settings.get(Trigger)}

def distance(name):
    #GPIO Mode (BOARD / BCM)
    GPIO.setmode(GPIO.BCM)
    SENSORS = get_pins(name)
    GPIO_TRIGGER = int(SENSORS.get('Trigger'))#18
    GPIO_ECHO = int(SENSORS.get('Echo'))#24
    GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
    GPIO.setup(GPIO_ECHO, GPIO.IN)
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)

    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    StartTime = time.time()
    StopTime = time.time()

    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()

    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()

    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
    GPIO.cleanup()
    return distance
