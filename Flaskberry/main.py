import json
import time
from flask import Flask, render_template, request, Response, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
import numpy as np

from pymongo import MongoClient
from pymongo import DESCENDING

# define folder for templates delete when deploying on pythonanywhere 
app = Flask(__name__, template_folder='Templates')
app.config['SECRET_KEY'] = 'you-will-never-guess'

#loads config file
json_data= open('config.json').read()
DATABASE = json.loads(json_data)
URI = DATABASE.get('URI')
DB = DATABASE.get('Database')

#setup mongodb
CONNECTION = MongoClient(URI, connect = False)
db = CONNECTION.get_database(DB)
Temperature = db.Temperature
Commands = db.Commands

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
def get_distance():
    '''
    return distance from ultrasound sensor
    '''
    _id = Commands.insert({"Command":'DISTANCE'})
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
    this renders webpages which is parsing streaming data from
    sse
    '''
    return render_template('index.html')


@app.route('/distance', methods=['GET', 'POST'])
def get_distance_():
    '''
    this renders webpages which is parsing streaming data from
    sse
    '''
    form = DistanceForm()
    if request.method == 'POST':
        distance = get_distance()
        print(distance)
        return render_template('distance.html', form = form, distance = distance)
    return render_template('distance.html', form = form, distance = '')

@app.route('/temp')
def get_temperature():
    '''
    this renders webpages which is parsing streaming data from
    sse
    '''
    temp = get_last_temperature()
    return str(temp).replace("'",'"'), 200

@app.route('/temperature')
def get_temp():
    '''
    this renders webpages which is parsing streaming data from
    sse
    '''
    temp = get_last_temperature()
    keys = list(temp.keys())
    return render_template('temperature.html', TemperatureKeys = keys)

@app.route('/logout')
def get_logout():
    
    '''
    this function is important to be able to
    logout 
    '''
    
    return "Logout", 401

if __name__ == "__main__":
    app.run(debug = True) #threaded=True)
