
import logging
from pymongo import MongoClient
import RPi.GPIO as GPIO
import time
from threading import Thread

from distance import distance
from led import light

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

#change URI to your need
client = MongoClient('mongodb//localhost')
db = client.Raspberry
Commands = db.Commands


def no_arg(func, instances = 1):

    '''
    no_arg will start function func which is function without arguments on threads where number of threads equals instances
    '''

    for i in range(instances):
        t = Thread(target=func)
        t.start()

def watch_collection():
    '''
    checking collection if there will be inserted document which have LED in it it will light up,
    '''
    logger.info('Starting watching Commands collection')
    watcher = Commands.watch()
    for item in watcher:
        doc = item.get('fullDocument')
        if doc:
            _id = item['fullDocument'].get('_id')
            if doc.get('Command') == 'LED':
                logger.info('Led command received')
                light(item['fullDocument'].get('Duration',1))
            if doc.get('Command') == 'DISTANCE':
                logger.info('Distance command received')
                dist = distance()
                logger.info('Distance: {} for _id:{}'.format(dist, _id))
                Commands.update({'_id':_id},{'$set':{'DISTANCE':dist}})

if __name__ == '__main__':
    no_arg(watch_collection)
