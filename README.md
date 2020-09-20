# SympTrack
Symptom Tracker HackMIT Project

## Introduction

### Requirements
To install dependencies, run ```$ pip3 install -r requirements.txt```.

### Running the app
Run ```$ python3 app.py``` and navigate to `http://127.0.0.1:5000/` in your browser.

### Misc.
By default there is one user in the database, with username `test` and password `test`. If you ever need to rebuild the database, simply delete `symptrack.db` and run ```$ python3 src/db.py```. Note that this will delete the default user, and you will need to register new users for testing.