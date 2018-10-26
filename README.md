# Flaskberry
Flask application to control Raspberry Pi 3 B+ sensors

App is using [Flask](http://flask.pocoo.org/) library and as database engine [MongoDB](https://www.mongodb.com/).

App can be run locally or remotely

For fully functional this code is divided in two parts: 
  * Flask server
  * Raspberry controls
  
 To download zip to your raspberry https://codeload.github.com/Norbaeocystin/Flaskberry/zip/master
 and unzip master
 
 For web app part main.py in Flaskberry and for control of raspberry pi run control.py in Controlberry
 
 For remote control it is possible to use free tier [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) ( you cant use free tier [mlab](https://mlab.com/) because it doesn't support .watch()).
 
 ## Notes:
   * if you want Flask app deploy change in main.py app.run(debug=True) to app.run()
   * [how to install mongodb](https://docs.mongodb.com/manual/installation/)
   * also it is good to install [TTL index](https://docs.mongodb.com/manual/core/index-ttl/) on Timestamp field in documents in Temperature collection
   * Example how to set up Controlberry (via raspberry terminal), do it in your preferred folder:
     * sudo apt-get update
     * sudo apt-get install screen
     * pip3 install pymongo
     * sudo pip3 install git+git://github.com/Norbaeocystin/Flaskberry.git
     * write connection MongoDB URI and Database to config.json
     * run in terminal: flaskberry
 
 ## To do list
 - [ ] users dashboard
 - [x] settings dashboard, but still needs improvement
 - [ ] compiled versions
 - [ ] better design
 - [ ] add more sensors
 - [ ] add timing options
 - [ ] notifications (SMS, email, facebook, alerts)
