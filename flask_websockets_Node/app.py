from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, join_room, leave_room, emit
from flask_session import Session
import requests
import json
import os
from flask import jsonify
from engineio.payload import Payload
from PIL import Image
import string
import random
import csv
from io import StringIO
from uploader import *
from websocket_functions import *
from GlobalData import *
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

#Payload.max_decode_packets = 50


app = Flask(__name__)
app.debug = False
app.config['SECRET_KEY'] = 'secret'
app.config['SESSION_TYPE'] = 'filesystem'



socketio = SocketIO(app, manage_session=False)

### HTML ROUTES ###

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')



@app.route('/upload', methods=['GET'])
def upload():
    prolist = listProjects()
    return render_template('upload.html', namespaces=prolist)

@app.route('/Examples/CustomElements1')
def CustomElements1R():
    return render_template('geneElement.html')

@app.route('/Examples/ServerSideVar')
def ServerSideVarR():
    return render_template('scroll.html', data = scb1Data)

@app.route('/Examples/CustomElements2')
def test3():
    return render_template('test.html')




### DATA ROUTES###

###RECEIVE INCOMING WEBSOCKET MSG FROM NODE.JS 
@app.route('/flask', methods=['GET', 'POST'])
def ws_receiver():
    wsreceiver(socketio)
    return 

@app.route('/uploadfiles', methods=['GET', 'POST'])
def uploadR():
    return upload_files(request)

@app.route('/load_all_projects', methods=['GET', 'POST'])
def loadAllProjectsR():
    return jsonify(projects=listProjects())

@app.route('/load_project/<name>', methods=['GET', 'POST'])
def loadProjectInfoR(name):
    return loadProjectInfo(name)

@app.route('/login/<usr>', methods=['GET', 'POST'])
def loginR(usr):
    if(request.method=='GET'):

        
        username = usr 
        room = 1
        #Store the data in session
        session['username'] = username
        session['room'] = room
        return render_template('geneElement.html', session = session)
    else:
        return "error"
    return render_template('main.html', usr = usr)

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if(request.method=='POST'):

        
        username = request.form['username'] 
        room = request.form['room']
        #Store the data in session
        session['username'] = username
        session['room'] = room
        return render_template('chat.html', session = session)
    else:
        if(session.get('username') is not None):
            session['username'] = 'reee'
            session['room'] = '2'
            return render_template('chat.html', session = session)
        else:
            return redirect(url_for('index'))


@app.route('/Test')
def test():
    if 'username' in session:
        username = session['username']
        return 'Logged in as ' + username + '<br>' + "<b><a href = '/logout'>click here to log out</a></b>"
    return "You are not logged in <br><a href = '/'>" + "click here to log in</a>"


###SocketIO ROUTES###


@socketio.on('join', namespace='/chat')
def join(message):
    room = session.get('room')
    join_room(room)
    #print(bcolors.WARNING + session.get('username') + ' has entered the room.' + bcolors.ENDC)
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
    #print(bcolors.WARNING + session.get('username') + "ex: " + json.dumps(message) + bcolors.ENDC)
    if message['fn'] == 'mkB':

        global scb1Data
        scb1Data.append({'id': message['id'], 'msg': message['msg'] })
        print('add to server' + message['msg'] + ' ' + message['id'] )
    
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

