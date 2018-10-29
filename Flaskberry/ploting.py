'''
functions to plot stored temperature and humidity data
'''
import base64
import io
import json
import logging
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.lines as mlines
from pymongo import DESCENDING, MongoClient
import pandas 
import time
import pkg_resources

logging.basicConfig(level=logging.DEBUG,  format = '%(asctime)s %(name)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

Config = pkg_resources.resource_filename('Flaskberry', 'Config/config.json')
#loads config file
json_data= open(Config).read()
DATABASE = json.loads(json_data)
URI = DATABASE.get('URI')
DB = DATABASE.get('Database')
CONNECTION = MongoClient(URI, connect = False)
db = CONNECTION.get_database(DB)
Adafruit = db.Adafruit
Settings = db.Settings

visualization = Settings.find_one().get('Visualization')

utc_zone = time.timezone/-(60*60)
now = datetime.datetime.now() - datetime.timedelta(hours = utc_zone)
delta = now - datetime.timedelta(hours = 24) - datetime.timedelta(hours = utc_zone)

def get_last_adafruit():
    '''
    returns last temperature from collection
    '''
    return Adafruit.find().limit(1).sort([('_id', DESCENDING)]).next().get('Temperature')

keys = list(get_last_adafruit().keys())
settings = Settings.find_one()

def transform_adafruit_dict(json, keys = keys, settings = settings):
    result = {}
    result['Timestamp'] = json['Timestamp']
    for item in keys:
        result[settings.get(item, item) + ' Humidity'] = json['Temperature'][item]['Humidity']
        result[settings.get(item, item) + ' Temperature'] = json['Temperature'][item]['Temperature']
    return result

temperatures = list(Adafruit.find({'Timestamp':{'$gt':delta}},{'_id':0}))
first = (temperatures[-1].get('Timestamp') - now).seconds//3600
tmp  = [transform_adafruit_dict(item) for item in temperatures]
df = pandas.DataFrame(tmp)

def get_image_as_string(df = df, humidity = 'Room Humidity', temperature = 'Room Temperature', 
                        targets_t = (30,20), targets_h = (60,40), day_start = 10, day_end = 20, 
                        h = first, humidity_interval = (0, 100), temperature_interval = (0,40)):
    #dividing night and day
    print(targets_t)
    print(targets_h)
    target_humidity_day,target_humidity_night  = targets_h
    target_temperature_day, target_temperature_night = targets_t
    order_hours = list(range(h + 1,-1, -1))
    d = datetime.datetime.now()
    hours = [(d - datetime.timedelta(hours = item)).hour for item in order_hours]
    time = df['Timestamp'] + datetime.timedelta(hours = utc_zone)
    temperature = df[temperature]
    humidity = df[humidity]
    hours_ = mdates.HourLocator(interval = 1)
    h_fmt = mdates.DateFormatter('%H:%M')
    fig, ax = plt.subplots(2, figsize = (5,5))
    plt.subplots_adjust(hspace = 0.35)
    #fig.autofmt_xdate()
    # Call plot() method on the appropriate object
    ax[0].plot(time, humidity)
    ax[0].set_title('Humidity')
    ax[0].set_ylim(humidity_interval)
    #ax[0].set_yticks([30,40,50,60,70,80])
    '''ax[0].xaxis.set_major_locator(hours_)
    ax[0].xaxis.set_major_formatter(h_fmt)
    ax[0].xaxis.set_major_locator(plt.MaxNLocator(10))'''
    ax[1].set_title('Temperature')
    ax[1].plot(time, temperature)
    ax[1].xaxis.set_major_locator(hours_)
    ax[1].set_ylim(temperature_interval)
    ax[1].xaxis.set_major_formatter(h_fmt)
    ax[1].xaxis.set_major_locator(plt.MaxNLocator(10))
    ax[0].xaxis.set_major_locator(hours_)
    ax[0].xaxis.set_major_formatter(h_fmt)
    ax[0].xaxis.set_major_locator(plt.MaxNLocator(10))
    def add_line(ax, x1,x2,y1,y2, color ,label):
        '''
        adding line to subplot ax
        '''
        line = mlines.Line2D(xdata = (x1, x2), ydata = (y1,y2), color = color, ) #label = label)# change ydata
        ax.add_line(line)
        return line
    for item in  [[ax[0],target_humidity_day, target_humidity_night],
                  [ax[1], target_temperature_day, target_temperature_night]]:
        min_, max_ = item[0].get_xlim()
        line_1 = add_line(item[0],min_,max_,item[1],item[1],'red',label='Day Target')
        line_2 = add_line(item[0],min_,max_,item[2],item[2],'green',label='Night Target')
        item[0].legend(handles =[line_1, line_2],labels = ['Day Target', 'Night Target'], loc='lower right', frameon=False)
        '''
        #case where day start is in hours limit
        if day_start in hours and day_end not in hours:
            logger.debug('case 1')
            start = (((max_ - min_)/24)*hours.index(day_start) +2 )+ min_
            #add lines
            add_line(item[0], start, max_,item[1], item[1], 'red')
            add_line(item[0], start, start,item[1], item[2], 'red')
            add_line(item[0], min_, start,item[2], item[2], 'red')
        #next case  
        if day_start not in hours and day_end in hours:
            logger.debug('case 2')
            start = (((max_ - min_)/24)*hours.index(day_end)  + 2)+ min_
            #add lines
            add_line(item[0], start, max_, item[1], item[1], 'red')
            add_line(item[0], start, start,item[1], item[2], 'red')
            add_line(item[0], min_, start,item[2], item[2], 'red')
        #next two cases
        if day_start in hours and day_end in hours:
            day_start_index = hours.index(day_start)
            day_end_index = hours.index(day_end)
            #first one
            if day_end_index > day_start_index:
                logger.debug('case 3')
                start = (((max_ - min_)/24)*(day_start_index+1))+ min_
                end = (((max_ - min_)/24)*(day_end_index +2))+ min_
                add_line(item[0], min_, start,item[2], item[2], 'red')
                add_line(item[0], start, start,item[1], item[2], 'red')
                add_line(item[0], start, end, item[1], item[1], 'red')
                add_line(item[0], end, end,item[1], item[2], 'red')
                add_line(item[0], end, max_, item[2], item[2], 'red')
            #second one
            if day_end_index < day_start_index:
                logger.debug('case 4')
                start = (((max_ - min_)/24)*(day_start_index+1))+ min_
                end = (((max_ - min_)/24)*(day_end_index+2))+ min_
                add_line(item[0], start, max_, item[1], item[1], 'red')
                add_line(item[0], start, start,item[1], item[2], 'red')
                add_line(item[0], end, start, item[2], item[2], 'red')
                add_line(item[0], end, end,item[1], item[2], 'red')
                add_line(item[0], min_, end,item[1], item[1], 'red')
        '''
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    stream = buf.read()
    string = base64.b64encode(stream)
    return string.decode()

def get_key_document(key):
    vis_data = Settings.find_one().get('Visualization')
    result = {}
    result['humidity'] = key + ' Humidity'
    result['temperature'] = key + ' Temperature'
    result['targets_t'] = float(vis_data.get('{}_Temperature_day'.format(key),0)),float(vis_data.get('{}_Temperature_night'.format(key),0))
    result['targets_h'] = float(vis_data.get('{}_Humidity_day'.format(key),0)),float(vis_data.get('{}_Humidity_night'.format(key),0))
    result['day_start'] = int(vis_data.get('{}_day'.format(key),0))
    result['day_end'] = int(vis_data.get('{}_night'.format(key),0))
    return result

def get_keys():
    vis_data = Settings.find_one().get('Visualization')
    if vis_data:
        keys = list({item.replace('__Temperature_day','') for item in vis_data.keys()})
        return keys

def get_image_as_string_from_key(key):
    if key not in get_keys():
        return ''
    else:
        doc = get_key_document(key)
        print(doc)
        return get_image_as_string(humidity = doc['humidity'], temperature = doc['temperature'], 
                            targets_t = doc['targets_t'], targets_h = doc['targets_h'],
                            day_start = doc['day_start'], day_end = doc['day_end'])
    