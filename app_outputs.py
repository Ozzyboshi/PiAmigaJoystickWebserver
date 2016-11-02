'''

Adapted excerpt from Getting Started with Raspberry Pi by Matt Richardson

Modified by Rui Santos
Complete project details: http://randomnerdtutorials.com

'''

import RPi.GPIO as GPIO
from flask import Flask, render_template, request, Response
import json

app = Flask(__name__)

GPIO.setmode(GPIO.BCM)

# Create a dictionary called pins to store the pin number, name, and pin state:
pins = {
   4 : {'name' : 'Pin 7', 'state' : GPIO.LOW},
   17 : {'name' : 'Pin 11', 'state' : GPIO.LOW},
   18 : {'name' : 'Pin 12', 'state' : GPIO.LOW},
   21 : {'name' : 'Pin 40', 'state' : GPIO.LOW},
   27 : {'name' : 'Pin 13', 'state' : GPIO.LOW},
   22 : {'name' : 'Pin 15', 'state' : GPIO.LOW},
   23 : {'name' : 'Pin 16', 'state' : GPIO.LOW},
   24 : {'name' : 'Pin 18', 'state' : GPIO.LOW},
   25 : {'name' : 'Pin 22', 'state' : GPIO.LOW},
   5 : {'name' : 'Pin 29', 'state' : GPIO.LOW},
   6 : {'name' : 'Pin 31', 'state' : GPIO.LOW},
   12 : {'name' : 'Pin 32', 'state' : GPIO.LOW},
   13 : {'name' : 'Pin 33', 'state' : GPIO.LOW},
   19 : {'name' : 'Pin 35', 'state' : GPIO.LOW},
   16 : {'name' : 'Pin 36', 'state' : GPIO.LOW},
   26 : {'name' : 'Pin 37', 'state' : GPIO.LOW},
   20 : {'name' : 'Pin 38', 'state' : GPIO.LOW},
   21 : {'name' : 'Pin 40', 'state' : GPIO.LOW}
}

# Set each pin as an output and make it low:
for pin in pins:
   GPIO.setup(pin, GPIO.OUT)
   GPIO.output(pin, GPIO.LOW)


@app.route("/listPins")
def listPins():
   #return Response(response=json.dumps(pins),status=200,mimetype="application/json")
   return "jsonCallback("+json.dumps(pins)+");"
   
@app.route("/")
def main():
   # For each pin, read the pin state and store it in the pins dictionary:
   for pin in pins:
      pins[pin]['state'] = GPIO.input(pin)
   # Put the pin dictionary into the template data dictionary:
   templateData = {
      'pins' : pins
      }
   # Pass the template data into the template main.html and return it to the user
   return render_template('main.html', **templateData)

# The function below is executed when someone requests a URL with the pin number and action in it:
@app.route("/<changePin>/<action>")
def action(changePin, action):
   # Convert the pin from the URL into an integer:
   changePin = int(changePin)
   # Get the device name for the pin being changed:
   deviceName = pins[changePin]['name']
   # If the action part of the URL is "on," execute the code indented below:
   if action == "on":
      # Set the pin high:
      GPIO.output(changePin, GPIO.HIGH)
      # Save the status message to be passed into the template:
      message = "Turned " + deviceName + " on."
   if action == "off":
      GPIO.output(changePin, GPIO.LOW)
      message = "Turned " + deviceName + " off."

   # For each pin, read the pin state and store it in the pins dictionary:
   for pin in pins:
      pins[pin]['state'] = GPIO.input(pin)

   # Along with the pin dictionary, put the message into the template data dictionary:
   templateData = {
      'pins' : pins
   }

   return render_template('main.html', **templateData)

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=80, debug=True)
