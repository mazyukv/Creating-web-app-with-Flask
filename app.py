from flask import Flask, jsonify
app = Flask(__name__)

@app.route('/<name>')
def index(name):
    return '<h1>Hello {}!</h1>'.format(name)

@app.route('/home', methods=['GET', 'POST'], defaults={'name': 'Pupsikin'})

@app.route('/home/<string:name>', methods=['POST', 'GET']) #methods to allow different http requests. GET is by default. Can choose strig ot int etc for the variable 
def home(name):
    return '<h1>Hello {}, you are on the home page <3</h1>'.format(name)

@app.route('/json')
def json():
    return jsonify({'key': 'value1', 'key2': [1,2,3]})

if __name__ == '__main__':
    app.run(debug=True) #debug true is to automatically resartapp running after you make a small change