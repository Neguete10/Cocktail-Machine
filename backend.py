from flask import Flask, request, jsonify
import os
import platform
import RPi.GPIO as GPIO
import time
import atexit
from flask_cors import CORS
from threading import Thread

app = Flask(__name__)
CORS(app)

app = Flask(__name__)

#TOP VIEW FROM BACK
# M4 -- M3
# M1 -- M2

# Define GPIO pins for the pumps
pump_pins = {
    "pump1": 22,
    "pump2": 23,
    "pump3": 27,
    "pump4": 17
}

# Set up the GPIO pins
GPIO.setmode(GPIO.BCM)
for pin in pump_pins.values():
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)

def cleanup_gpio():
    GPIO.cleanup()

atexit.register(cleanup_gpio)

@app.route('/activate_pumps', methods=['POST'])
def activate_pumps():
    data = request.get_json()
    durations = {
        "pump1": float(data.get("pump1", 0)),
        "pump2": float(data.get("pump2", 0)),
        "pump3": float(data.get("pump3", 0)),
        "pump4": float(data.get("pump4", 0))
    }
    seconds_per_ounce = 14 #off-set calibrated for 1 oz of liquid
    
    threads = []
    for pump, duration in durations.items():
        thread = Thread(target=activate_pumps, args=(pump, duration, seconds_per_ounce))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
        
    # for pump, duration in durations.items():
    #     if duration > 0:
    #         GPIO.output(pump_pins[pump], GPIO.LOW)
    #         time.sleep(duration*seconds_per_ounce)
    #         GPIO.output(pump_pins[pump], GPIO.HIGH)
    
    return jsonify({"status": "success", "durations": durations})

@app.route('/pump_control', methods=['POST'])
def pump_control():
    data = request.get_json()
    
    pumpId = data.get("pumpId", 0)
    pumpStatus = data.get("status", 0)

    if pumpStatus == "on":
        GPIO.output(pump_pins[pumpId], GPIO.LOW)
    else:
        GPIO.output(pump_pins[pumpId], GPIO.HIGH)
    
    return jsonify({
        "message": pumpId + " is turned " + pumpStatus + "!",
        "status": "success"})
    
@app.route('/clean', methods=['POST'])
def clean():
    data = request.get_json()
    pumpId = data.get("pumpId", 0)
    pumpStatus = data.get("status", 0)
    if pumpStatus == "on":
        for pump in pump_pins.values():
            GPIO.output(pump, GPIO.LOW)
    else:
        for pump in pump_pins.values():
            GPIO.output(pump, GPIO.HIGH)
        
    print(pumpId)
    
    return jsonify({
        "message": "All cleaned up nicely now!",
        "status": "success"
    })
    
@app.route('/shutdown', methods=['POST'])
def shutdown():
    system_platform = platform.system()
    try:
        if system_platform == "Windows":
            os.system('shutdown /s /t 1')
        elif system_platform == "Linux":
            os.system('sudo shutdown -h now')
        else:
            return jsonify({"error": "Unsupported platform"}), 500
        return jsonify({"message": "System is shutting down..."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/reboot', methods=['POST'])
def reboot():
    system_platform = platform.system()
    try:
        if system_platform == "Windows":
            os.system('shutdown /r /t 1')
        elif system_platform == "Linux":
            os.system('sudo reboot')
        else:
            return jsonify({"error": "Unsupported platform"}), 500
        return jsonify({"message": "System is rebooting..."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
