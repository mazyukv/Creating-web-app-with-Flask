from flask import Flask, jsonify, request, url_for, redirect, session
app = Flask(__name__)
#configurations
app.config['DEBUG'] = True # true when debugging, false when goes live
app.config['SECRET_KEY'] = 'secret'

@app.route('/<name>')
def index(name):
    session.pop('name', None)
    return '<h1>Hello {}!</h1>'.format(name)

@app.route('/home', methods=['GET', 'POST'], defaults={'name': 'Pupsikin'})

@app.route('/home/<string:name>', methods=['POST', 'GET']) #methods to allow different http requests. GET is by default. Can choose strig ot int etc for the variable 
def home(name):
    session['name'] = name #all other routes will have access to this name 
    return '<h1>Hello {}, you are on the home page <3</h1>'.format(name)

@app.route('/json')
def json():
    if 'name' in session:
        name = session['name']
    else:
        name = 'NotinSession!'
    return jsonify({'key': 'value1', 'key2': [1,2,3], 'name': name})

@app.route('/query')
def query():
    name = request.args.get('name') #fetching values from url
    location = request.args.get('location')
    return '<h1>Hi {}. You are from {}. You are on the query page</h1>'.format(name, location)

@app.route('/theform', methods=['POST', 'GET'])
def theform():

    if request.method == 'GET':
        return '''<form method="POST" action="/theform">
                    <input type="text" name="name">
                    <input type="text" name="location">
                    <input type="submit" value="Submit">
                    </form>'''
    else:
        name = request.form['name'] #fetching values from data
        location = request.form['location']
        # return '<h1>Hello {}! You are from {}. You have submitted the form successfully!</h1>'.format(name, location)
        return redirect(url_for('home', name=name, location=location)) #appends it to the url 
# @app.route('/process', methods=['POST'])
# def process():
#     name = request.form['name'] #fetching values from data
#     location = request.form['location']

#     return '<h1>Hello {}! You are from {}. You have submitted the form successfully!</h1>'.format(name, location)


@app.route('/processjson', methods=['POST', 'GET'])
def processjson():
    data = request.get_json()
    name = data['name']
    location = data['location']
    randomlist = data['randomlist']

    return jsonify({'result': 'Success!', 'name': name, 'location': location, 'randomkeyinlist': randomlist[1]})

if __name__ == '__main__':
    app.run() #debug true is to automatically resartapp running after you make a small change. If you save mistake with it, app will crash