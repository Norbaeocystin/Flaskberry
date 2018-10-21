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
 
 For remote control it is possible to use free tier databases from [mlab](https://mlab.com/) or [MongoDB Atlas](https://www.mongodb.com/cloud/atlas).
 
 ## Notes:
   *in mlab free tier you have only one database my_database
   *if you want deploy change in main.py app.run(debug=True) to app.run()
