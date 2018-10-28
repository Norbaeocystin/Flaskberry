# Flaskberry
Flask application to control Raspberry Pi 3 B+ sensors

App is using [Flask](http://flask.pocoo.org/) library and as database engine [MongoDB](https://www.mongodb.com/).

App can be run locally or remotely

To use Flaskberry:
 you need also:
   * install [MongoDB](https://docs.mongodb.com/manual/installation/) locally or on server
   * install [Controlberry](https://github.com/Norbaeocystin/Controlberry)
 
 For web app part main.py in Flaskberry and for control of raspberry pi run control.py in Controlberry
 
 For remote control it is possible to use free tier [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) ( you cant use free tier [mlab](https://mlab.com/) because it doesn't support .watch()).
 
 ## Notes:
   * if you want Flask app deploy change in main.py app.run(debug=True) to app.run()
   * [how to install mongodb](https://docs.mongodb.com/manual/installation/)
   * also it is good to install [TTL index](https://docs.mongodb.com/manual/core/index-ttl/) on Timestamp field in documents in Temperature collection
   * How to install and run:
``` 
sudo apt-get update
sudo apt-get install screen
sudo pip3 install git+git://github.com/Norbaeocystin/Flaskberry.git
#or if you have windows
python -m pip install https://github.com/Norbaeocystin/Flaskberry/archive/master.zip
#write connection MongoDB URI and Database to config.json
flaskberry
```
 
 ## To do list
 - [ ] users dashboard
 - [x] settings dashboard, but still needs improvement
 - [ ] compiled versions
 - [ ] better design
 - [ ] add more sensors
 - [ ] add timing options
 - [ ] notifications (SMS, email, facebook, alerts)
