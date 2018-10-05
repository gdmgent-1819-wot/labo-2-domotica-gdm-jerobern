import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from sense_hat import SenseHat
import pygame
from time import time, sleep
import os
import sys

try:
    pygame.init()
    alarm_sound = pygame.mixer.Sound('../assets/sounds/alarm.wav')
except:
    print('Unable to load alarm sound')
    sys.exit(1)

# Update with firebase info
serviceAccountKey = '../serviceAccountKey.json'
databaseURL = 'https://wot-1819-jerobern.firebaseio.com/'

lights = dict();
outlets = dict();
doors = dict();

try:
    # Fetch the service account key JSON file contents
    firebase_cred = credentials.Certificate(serviceAccountKey)

    # Initalize the app with a service account; granting admin privileges
    firebase_admin.initialize_app(firebase_cred, {
    'databaseURL': databaseURL
    })

    # As an admin, the app has access to read and write all data
    firebase_ref_active_room = db.reference('active_room')
    firebase_ref_alarm = db.reference('active_room/alarm')
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
    # render all lights on senseHat
    if active_room and 'lights' in active_room:
        global lights
        lights = active_room['lights']
        for light in lights: 
            position = light['position']
            color = (255, 255, 0) if light['is_on'] else (51, 51, 0)
            sense.set_pixel(int(position['x']), int(position['y']), color)
    # render all outlets on senseHat
    if active_room and 'outlets' in active_room:
        global outlets
        outlets = active_room['outlets']
        for outlet in outlets: 
            position = outlet['position']
            color = (0,191,255) if outlet['is_on'] else (0, 0, 139)
            sense.set_pixel(int(position['x']), int(position['y']), color)
     # render all doors on senseHat
    if active_room and 'doors' in active_room:
        global doors
        doors = active_room['doors']
        for door in doors: 
            position = door['position']
            color = (0, 255, 0) if door['is_open'] else (255, 0, 0)
            sense.set_pixel(int(position['x']), int(position['y']) - 1, color)
            sense.set_pixel(int(position['x']), int(position['y']), color)
            sense.set_pixel(int(position['x']), int(position['y']) + 1, color)

def alarm_changed_handler(args):
    alarm_is_on = firebase_ref_alarm.get();
    while alarm_is_on:
        for light in lights: 
            position = light['position']
            color = (255, 255, 0)
            sense.set_pixel(int(position['x']), int(position['y']), (255, 255, 0))
            sleep(0.15)
            sense.set_pixel(int(position['x']), int(position['y']), (51, 51, 0))
        for door in doors: 
            position = door['position']
            sense.set_pixel(int(position['x']), int(position['y']) - 1, (0, 255, 0))
            sense.set_pixel(int(position['x']), int(position['y']), (0, 255, 0))
            sense.set_pixel(int(position['x']), int(position['y']) + 1, (0, 255, 0))
            sleep(0.15)
            sense.set_pixel(int(position['x']), int(position['y']) - 1, (255, 0, 0))
            sense.set_pixel(int(position['x']), int(position['y']), (255, 0, 0))
            sense.set_pixel(int(position['x']), int(position['y']) + 1, (255, 0, 0))
        alarm_sound.play()
        alarm_is_on = firebase_ref_alarm.get();

def main():
    firebase_ref_active_room.listen(room_changed_handler)
    firebase_ref_alarm.listen(alarm_changed_handler)
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