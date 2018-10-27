import json
import time
from flask import Flask, render_template, request, Response, json, flash, make_response
from flask_wtf import FlaskForm
import pandas
import io
import csv

from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired

from pymongo import MongoClient
from pymongo import DESCENDING
from pymongo.errors import OperationFailure

import pkg_resources

Config = pkg_resources.resource_filename('Flaskberry', 'Config/config.json')

# define folder for templates delete when deploying on pythonanywhere 
app = Flask(__name__, template_folder='Templates')
app.config['SECRET_KEY'] = 'you-will-never-guess'

#loads config file
json_data= open(Config).read()
DATABASE = json.loads(json_data)
URI = DATABASE.get('URI')
DB = DATABASE.get('Database')

#if URI doesnt exits it will write data to config.json
if not URI:
    URI = input("Please write your connection MongoDB URI and press Enter: \n")
    DB = input("Please write name of your Database: \n")
    with open(Config, 'w') as outfile:
        json.dump({'URI':URI,'Database':DB}, outfile)

json_data= open(Config).read()
DATABASE = json.loads(json_data)
URI = DATABASE.get('URI')
DB = DATABASE.get('Database')
CONNECTION = MongoClient(URI, connect = False)
db = CONNECTION.get_database(DB)
Temperature = db.Temperature
Commands = db.Commands
Settings = db.Settings
Adafruit = db.Adafruit

#will capp collections to prevent from collecting to much data
for item in ['Commands','Temperature', 'Adafruit']:
    try:
        if not db.command('collstats',item).get('capped', False):
            print('Not capped')
            db.command({"convertToCapped": item, "size": 10000000});
            print('{} changed to capped collection'.format(item))
    except OperationFailure:
        pass

class SettingsForm(FlaskForm):
    '''
    Form for searching in database
    '''
    submit = SubmitField('Submit')

#functions for temperature
'''
def get_temperatures():
    list1 = [item.get('Temperature') for item in list(Temperature.find().limit(36000).sort([('_id', DESCENDING)]))]
    return list(np.mean(np.array(list1).reshape(-1, 1200), axis=1))[::-1]'''

def get_last_temperature():
    '''
    returns last temperature from collection
    '''
    return Temperature.find().limit(1).sort([('_id', DESCENDING)]).next().get('Temperature')

def get_last_adafruit():
    '''
    returns last temperature from collection
    '''
    return Adafruit.find().limit(1).sort([('_id', DESCENDING)]).next().get('Temperature')

   

#functions for distance
def get_distance(name):
    '''
    return distance from ultrasound sensor
    '''
    _id = Commands.insert({"Command":'DISTANCE', 'Name':name})
    time.sleep(0.1)
    for i in range(10):
        distance = Commands.find_one({"_id":_id}).get('DISTANCE')
        if distance:
            return str(round(distance,2))
        else:
            time.sleep(0.1)

class DistanceForm(FlaskForm):
    submit = SubmitField('Distance')

@app.route('/')
def get_main():
    '''
    home
    '''
    return render_template('index.html')

@app.route('/api/sensor/settings', methods=['GET', "POST"])
def get_sensor_settings():
    if request.method == 'POST':
        Settings.update({'_id':0},request.json,True)
        return 'Success'

@app.route('/settings', methods=['GET', 'POST'])
def get_settings():
    '''
    settings
    '''
    form = SettingsForm()
    try:
        keys = list(Temperature.find().sort([('_id', -1)]).limit(1).next().get('Temperature').keys())
    except StopIteration:
        keys = []
    settingsData = json.dumps(Settings.find_one({"_id":0},{'_id':0}))
    if request.method == 'POST':
        return render_template('settings.html', form = form, keys = keys)
    return render_template('settings.html', form = form, keys = keys, settingsData = settingsData)

@app.route('/led', methods=['GET', 'POST'])
def get_led():
    '''
    led control
    '''
    settings = Settings.find_one({"_id":0},{'_id':0})
    ledKeys = [(k,v) for k,v in settings.items() if 'LedName' in k]
    return render_template('led.html', LedKeys = ledKeys)

@app.route('/api/led', methods=['GET', "POST"])
def get_led_api():
    if request.method == 'POST':
        data = request.json
        if data.get('Brightness'):
            data['Brightness'] = int((int(data['Brightness'])/255)*100)
        data['Command'] = 'LED'
        Commands.insert(data)
        return 'Success'

@app.route('/help')
def get_help():
    '''
    help
    '''
    return render_template('help.html')


@app.route('/distance', methods=['GET', 'POST'])
def get_distance_():
    '''
    distance
    '''
    form = DistanceForm()
    settings = Settings.find_one({"_id":0},{'_id':0})
    ultraSoundKeys = [(k,v) for k,v in settings.items() if 'UltraSoundName' in k]
    if request.method == 'POST':
        name = list(request.form)[0]
        distance = get_distance(name)
        return render_template('distance.html', form = form, ultraSoundKeys = ultraSoundKeys, name = str(name), distance = distance)
    return render_template('distance.html', form = form, ultraSoundKeys = ultraSoundKeys, name = 0, distance = 0)

@app.route('/temp')
def get_temperature():
    '''
    temperature api
    '''
    try:
        temp = get_last_temperature()
    except:
        temp = ''
    return str(temp).replace("'",'"'), 200

@app.route('/temperature', methods=['GET', 'POST'])
def get_temp():
    '''
    temperature
    '''
    settings = json.dumps(Settings.find_one({"_id":0},{'_id':0}))
    try:
        temp = get_last_adafruit()
        keys = list(temp.keys())
    except:
        keys = []
    if request.method == 'POST':
        flash ('Loading data ... ')
        temperatures = list(Temperature.find({},{'_id':0}))
        tmp  = [dict(item.get('Temperature').items()|{'Timestamp':item.get('Timestamp')}.items()) for item in temperatures]
        df = pandas.DataFrame(tmp)
        string = df.to_string(index=False)
        strings = string.split('\n')
        data = "\n".join([','.join(item.split()) for item in strings])
        flash ('Processing data ... ')
        si = io.StringIO()
        cw = csv.writer(si)
        cw.writerows(data)
        output = make_response(si.getvalue())
        #output = excel.make_response_from_array(data, 'csv')
        output.headers["Content-Disposition"] = "attachment; filename=TemperaturesDS18B20.csv"
        output.headers["Content-type"] = "text/csv"
        flash ('Saving data ... ')
        return output
    return render_template('adafruit.html', TemperatureKeys = keys, settings = settings)

app.route('/adafruit', methods=['GET', 'POST'])
def get_adafruit():
    '''
    temperature
    '''
    settings = json.dumps(Settings.find_one({"_id":0},{'_id':0}))
    try:
        temp = get_last_temperature()
        keys = list(temp.keys())
    except:
        keys = []
    if request.method == 'POST':
        flash ('Loading data ... ')
        temperatures = list(Temperature.find({},{'_id':0}))
        tmp  = [dict(item.get('Temperature').items()|{'Timestamp':item.get('Timestamp')}.items()) for item in temperatures]
        df = pandas.DataFrame(tmp)
        string = df.to_string(index=False)
        strings = string.split('\n')
        data = "\n".join([','.join(item.split()) for item in strings])
        flash ('Processing data ... ')
        si = io.StringIO()
        cw = csv.writer(si)
        cw.writerows(data)
        output = make_response(si.getvalue())
        #output = excel.make_response_from_array(data, 'csv')
        output.headers["Content-Disposition"] = "attachment; filename=TemperaturesHumidity.csv"
        output.headers["Content-type"] = "text/csv"
        flash ('Saving data ... ')
        return output
    return render_template('temperature.html', TemperatureKeys = keys, settings = settings)

@app.route('/logout')
def get_logout():
    
    '''
    http logout
    '''
    
    return "Logout", 401

def run():
    app.run(debug = True)

if __name__ == "__main__":
    app.run(debug = True) #threaded=True)
