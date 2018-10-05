# labo-2-domotica-gdm-jerobern

## Setup
* add Google Firebase privésleutel in root serviceAccountKey.json
* update Google Firebase config in firebaseConfig.js
* run python file in pi/app_domotica.py on a Raspberry Pi with SenseHat connected (and connected to internet)
* open index.html in browser

## Opdracht
Maak een SmartHome-applicatie waarmee een geauthenticeerde bezoeker (client) devices kan sturen en/of uitlezen. De client draait op GitHub pages en maak gebruikt van Google Firebase (Koppelingen naar een externe site.)Koppelingen naar een externe site.. Op de Raspberry Pi draait een programma die kan anticiperen op wijzigingen binnen Google Firebase Firestore (Koppelingen naar een externe site.)

Op senseHat van Raspberry Pi worden lampen, stopcontacten en deuren nagebootst met behulp van leds.

* stuur alle lichtpunten;
* stuur alle stopcontacten;
* stuur de voor-en achterdeur;
* lees de temperatuur en humidity uit;
* alert knop (bijvoorbeeld inbraak): laat alle lichtpunten flikkeren, open alle deuren, speel een alarmgeluid af.