from flask import Flask, request

app = Flask(__name__)

@app.route('/activate_pumps', methods=['GET', 'POST'])
def print_request():
    print('Headers: ', request.headers)
    print('Body: ', request.get_data())
    return 'Request printed in console'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)