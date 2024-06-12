from flask import Flask, request
import json

app = Flask(__name__)

@app.route('/activate_pump', methods=['POST'])
def activate_pump():
    print('Received request to activate pump' + json.dumps(request.get_json()))
    return json.dumps({'message': 'Pump activated'})

if __name__ == '__main__':
    app.run()