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
    return jsonify({
        "message": data,
        "status": "success"})
    # data = request.get_json()
    # pump = data.get("pump", None)
    # action = data.get("action", None)
    
    # if pump is None or action is None:
    #     return jsonify({"status": "error", "message": "Missing pump or action"})
    
    # if pump not in pump_pins:
    #     return jsonify({"status": "error", "message": "Invalid pump"})
    
    # if action == "on":
    #     GPIO.output(pump_pins[pump], GPIO.HIGH)
    # elif action == "off":
    #     GPIO.output(pump_pins[pump], GPIO.LOW)
    # else:
    #     return jsonify({"status": "error", "message": "Invalid action"})
    
    # return jsonify({"status": "success", "pump": pump, "action": action})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
