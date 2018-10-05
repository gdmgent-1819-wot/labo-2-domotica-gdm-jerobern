import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from sense_hat import SenseHat
from time import time, sleep
import os
import sys

# Update with firebase info
serviceAccountKey = '../serviceAccountKey.json'
databaseURL = 'https://wot-1819-jerobern.firebaseio.com/'

try:
    # Fetch the service account key JSON file contents
    firebase_cred = credentials.Certificate(serviceAccountKey)

    # Initalize the app with a service account; granting admin privileges
    firebase_admin.initialize_app(firebase_cred, {
    'databaseURL': databaseURL
    })

    # As an admin, the app has access to read and write all data
    firebase_ref_active_room = db.reference('active_room')
except:
    print('Unable to initialize Firebase: {}'.format(sys.exc_info()[0]))
    sys.exit(1)

try:
    # SenseHat
    sense = SenseHat()
    sense.set_imu_config(False, False, False)
except:
    print('Unable to initialize the Sense Hat library: {}'.format(sys.exc_info()[0]))
    sys.exit(1)

def room_changed_handler(args):
    active_room = firebase_ref_active_room.get()
    if active_room and 'lights' in active_room:
        lights = active_room['lights']
        for light in lights: 
            position = light['position']
            color = (255, 255, 0) if light['is_on'] else (51, 51, 0)
            sense.set_pixel(int(position['x']), int(position['y']), color)
    if active_room and 'outlets' in active_room:
        outlets = active_room['outlets']
        for outlet in outlets: 
            position = outlet['position']
            color = (0,191,255) if outlet['is_on'] else (0, 0, 139)
            sense.set_pixel(int(position['x']), int(position['y']), color)
    if active_room and 'doors' in active_room:
        doors = active_room['doors']
        for door in doors: 
            position = door['position']
            color = (0, 255, 0) if door['is_open'] else (255, 0, 0)
            sense.set_pixel(int(position['x']), int(position['y']) - 1, color)
            sense.set_pixel(int(position['x']), int(position['y']), color)
            sense.set_pixel(int(position['x']), int(position['y']) + 1, color)

def main():
  firebase_ref_active_room.listen(room_changed_handler)
  while True:
    sleep(0.1)
        
if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, SystemExit):
        print('Interrupt received! Stopping the application...')
    finally:
        print('Cleaning up the mess...')
        sense.clear()
        sys.exit(0)