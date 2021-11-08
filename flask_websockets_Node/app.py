from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, join_room, leave_room, emit
from flask_session import Session
import requests
import json
import string
import random

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def sendUE4(adress, data):
    # The POST request to our node server
    res = requests.post('http://127.0.0.1:3000/in', json=data)
    #return
    # Convert response data to json
    #returned_data = res.json() 
    #print(returned_data)

idata = {'mes': 'dfhdfhfh', 'usr': 'NaS7QA89nxLg9nKQAAAn', 'tag': 'flask'}
pairs = [("a", "1"), ("b", "2"), ("c", "3")]
sliders = [("ddfd", "1"), ("bfsd", "2"), ("cdfsdf", "3")]

app = Flask(__name__)
app.debug = False
app.config['SECRET_KEY'] = 'secret'
app.config['SESSION_TYPE'] = 'filesystem'

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

Session(app)


socketio = SocketIO(app, manage_session=False)



###RECEIVE INCOMING WEBSOCKET MSG FROM NODE.JS 
@app.route('/flask', methods=['GET', 'POST'])
def wsreceiver():
    if request.method == 'POST':
        data =request.get_json()
    else:
        data = request.args

    global idata

    idata = data
    print(bcolors.WARNING + data['usr']  + "says: " + data['mes'] + bcolors.ENDC)

    outstr = data['usr'] +' : ' + data['mes']
### Multicast to connected web clients (not UE4!)
    socketio.emit('message', {'msg': outstr}, namespace = '/chat' , room='1')

### Send it back to node wich multicasts it to ue4 clients
    sendUE4('http://127.0.0.1:3000/in', data)

    return





@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if(request.method=='POST'):

        string.ascii_uppercase
        username = request.form['username'] 
        room = request.form['room']
        #Store the data in session
        session['username'] = username
        session['room'] = room
        return render_template('chat.html', session = session)
    else:
        if(session.get('username') is not None):
            return render_template('chat.html', session = session)
        else:
            return redirect(url_for('index'))


@app.route('/Test')
def test():
    if 'username' in session:
        username = session['username']
        return 'Logged in as ' + username + '<br>' + "<b><a href = '/logout'>click here to log out</a></b>"
    return "You are not logged in <br><a href = '/'>" + "click here to log in</a>"

@app.route('/Test1')
def test1():
    
    return render_template('test.html', data = idata, pairs = pairs, sliders = sliders)


@app.route('/Test2')
def test2():
    
    return render_template('scroll.html', data = idata, pairs = pairs, sliders = sliders)

@socketio.on('join', namespace='/chat')
def join(message):
    room = session.get('room')
    join_room(room)
    print(bcolors.WARNING + session.get('username') + ' has entered the room.' + bcolors.ENDC)
    emit('status', {'msg':  session.get('username') + ' has entered the room.'}, room=room)


@socketio.on('text', namespace='/chat')
def text(message):
    room = session.get('room')
    print(bcolors.WARNING + session.get('username') + "says: " + message['msg'] + bcolors.ENDC)
    emit('message', {'msg': session.get('username') + ' : ' + message['msg']}, room=room)
    sendUE4('http://127.0.0.1:3000/in',  {'msg': session.get('username') + ' : ' + message['msg']})

@socketio.on('ex', namespace='/chat')
def ex(message):
    room = session.get('room')
    print(bcolors.WARNING + session.get('username') + "ex: " + json.dumps(message) + bcolors.ENDC)
    emit('ex', message, room=room)
    #sendUE4('http://127.0.0.1:3000/in',  {'msg': session.get('username') + ' : ' + message['msg']})

@socketio.on('test', namespace='/chat')
def test(message):
    #room = session.get('room')
    print(bcolors.WARNING + session.get('username') + "says: " + message['msg'] + bcolors.ENDC)
    #emit('message', {'msg': session.get('username') + ' : ' + message['msg']}, room=room)
    #sendUE4('http://127.0.0.1:3000/in',  {'msg': session.get('username') + ' : ' + message['msg']})

@socketio.on('sl1', namespace='/chat')
def test(message):
    room = session.get('room')
    #print(bcolors.WARNING + session.get('username') + "says: " + message['msg'] + bcolors.ENDC)
    emit('sl1', message , room=room)

@socketio.on('left', namespace='/chat')
def left(message):
    room = session.get('room')
    username = session.get('username')
    leave_room(room)
    session.clear()
    emit('status', {'msg': username + ' has left the room.'}, room=room)


if __name__ == '__main__':
    socketio.run(app)

