from flask import Flask, jsonify, request, url_for, redirect, session, render_template, g
import sqlite3
app = Flask(__name__)
#configurations
app.config['DEBUG'] = True # true when debugging, false when goes live
app.config['SECRET_KEY'] = 'secret'

def connect_db():
    sql = sqlite3.connect('C:/Users/Варвара/OneDrive/Рабочий стол/Creating-web-app-with-Flask/data.db')
    sql.row_factory = sqlite3.Row
    return sql

def get_db():
    if not hasattr(g, 'sqlite3'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

@app.route('/<name>')
def index(name):
    session.pop('name', None)
    return '<h1>Hello {}!</h1>'.format(name)

@app.route('/home', methods=['GET', 'POST'], defaults={'name': 'Pupsikin'})
@app.route('/home/<string:name>', methods=['POST', 'GET']) #methods to allow different http requests. GET is by default. Can choose strig ot int etc for the variable 
def home(name):
    session['name'] = name #all other routes will have access to this name 
    db = get_db()
    cur = db.execute('select id, name, location from users')
    results = cur.fetchall()
    return render_template('home.html', name=name, display=False, mylist=['one', 'two', 'three', 'four'], listofdictionaries = [{'name': 'Stepan'}, {'name': 'Irina'}], results=results)

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
        return render_template('form.html')
    else:
        name = request.form['name'] #fetching values from data
        location = request.form['location']
        # return '<h1>Hello {}! You are from {}. You have submitted the form successfully!</h1>'.format(name, location)
        
        db = get_db()
        db.execute('insert into users (name, location) values (?, ?)', [name, location])
        db.commit()

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

@app.route('/viewresults')
def viewresults():
    db = get_db()
    cur = db.execute('select id, name, location from users')
    results = cur.fetchall()
    return '<h1>The ID is {}. The name is {}. The location is {}.</h1>'.format(results[2]['id'], results[2]['name'], results[2]['location'])

if __name__ == '__main__':
    app.run() #debug true is to automatically resartapp running after you make a small change. If you save mistake with it, app will crash