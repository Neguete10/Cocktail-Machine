from flask import Flask, request, jsonify
import RPi.GPIO as GPIO
import time
import atexit

app = Flask(__name__)

# Define GPIO pins for the pumps
pump_pins = {
    "pump1": 17,
    "pump2": 18,
    "pump3": 27,
    "pump4": 22
}

# Set up the GPIO pins
GPIO.setmode(GPIO.BCM)
for pin in pump_pins.values():
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

def cleanup_gpio():
    GPIO.cleanup()

atexit.register(cleanup_gpio)

@app.route('/activate_pumps', methods=['POST'])
def activate_pumps():
    data = request.get_json()
    durations = {
        "pump1": data.get("pump1", 0),
        "pump2": data.get("pump2", 0),
        "pump3": data.get("pump3", 0),
        "pump4": data.get("pump4", 0)
    }
    
    for pump, duration in durations.items():
        if duration > 0:
            GPIO.output(pump_pins[pump], GPIO.HIGH)
            time.sleep(duration)
            GPIO.output(pump_pins[pump], GPIO.LOW)
    
    return jsonify({"status": "success", "durations": durations})

@app.route('/pump_control', methods=['POST'])
def pump_control():
    data = request.get_json()
    
    pumpId = data.get("pumpId", 0)
    pumpStatus = data.get("status", 0)

    if pumpStatus == "on":
        GPIO.output(pump_pins[pumpId], GPIO.HIGH)
    else:
        GPIO.output(pump_pins[pumpId], GPIO.LOW)
    
    return jsonify({
        "message": pumpId + " is turned " + pumpStatus + "!",
        "status": "success"})
    
@app.route('/clean', methods=['POST'])
def clean():
    data = request.get_json()
    pumpId = data.get("pumpId", 0)
    if pumpId == "clean":
        for pump in pump_pins.values():
            GPIO.output(pump, GPIO.HIGH)
        
        time.sleep(10)
        
        for pump in pump_pins.values():
            GPIO.output(pump, GPIO.LOW)
        
    print(pumpId)
    
    return jsonify({
        "message": "All cleaned up nicely now!",
        "status": "success"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
