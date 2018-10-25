import json
import time
from flask import Flask, render_template, request, Response, json
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired
import numpy as np

from pymongo import MongoClient
from pymongo import DESCENDING

# define folder for templates delete when deploying on pythonanywhere 
app = Flask(__name__, template_folder='Templates')
app.config['SECRET_KEY'] = 'you-will-never-guess'

#loads config file
try:
    json_data= open('config.json').read()
    DATABASE = json.loads(json_data)
    URI = DATABASE.get('URI')
    DB = DATABASE.get('Database')
except FileNotFoundError:
    URI = input("Please write your MongoDB URI: ")
    DB = input("Please write name of your Database")
    json_data = {'URI':URI, 'DB':DB}
    with open('config.json', 'w') as f:
        json.dump(json_data, f)

#setup mongodb
CONNECTION = MongoClient(URI, connect = False)
db = CONNECTION.get_database(DB)
Temperature = db.Temperature
Commands = db.Commands
Settings = db.Settings

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

@app.route('/temperature')
def get_temp():
    '''
    temperature
    '''
    settings = json.dumps(Settings.find_one({"_id":0},{'_id':0}))
    try:
        temp = get_last_temperature()
        keys = list(temp.keys())
    except:
        keys = []
    return render_template('temperature.html', TemperatureKeys = keys, settings = settings)

@app.route('/logout')
def get_logout():
    
    '''
    http logout
    '''
    
    return "Logout", 401

if __name__ == "__main__":
    app.run(debug = True) #threaded=True)
