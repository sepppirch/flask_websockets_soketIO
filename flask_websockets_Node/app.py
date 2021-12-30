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
import random
import csv

from io import StringIO
Payload.max_decode_packets = 50

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

scb1Data = [
  {"msg": "TMP", "id": '#button1'},
  {"msg": "MMU", "id": '#button2'},
  {"msg": "PAM", "id": '#button3'},
  {"msg": "CHR", "id": '#button3'},
  {"msg": "OMG", "id": '#button3'},
  {"msg": "WTF", "id": '#button3'},
  {"msg": "HH2H", "id": '#button3'},
  {"msg": "ASS1", "id": '#button3'}
]
pairs = [("a", "1"), ("b", "2"), ("c", "3")]
sliders = [("ddfd", "1"), ("bfsd", "2"), ("cdfsdf", "3")]

app = Flask(__name__)
app.debug = False
app.config['SECRET_KEY'] = 'secret'
app.config['SESSION_TYPE'] = 'filesystem'

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

#Session(app)

def makeProjectFolders(name):
    path = "static/projects/" + name
    try:
        os.mkdir(path)
        os.mkdir(path + '/layouts')
        os.mkdir(path + '/layoutsRGB')
        os.mkdir(path + '/links')
        os.mkdir(path + '/linksRGB')
    except OSError:
        print ("Creation of the directory %s failed" % path)
    else:
        print ("Successfully created the directory %s " % path)




def listProjects():
    folder = 'static/projects'
    sub_folders = [name for name in os.listdir(folder) if os.path.isdir(os.path.join(folder, name))]
    print(sub_folders)
    return sub_folders


def makeNodeTex(project, name, file):

    f = StringIO(file)
    csvreader = csv.reader(f, delimiter=',')
    path = 'static/projects/' + project 
    
    
    texh = [(0,0,0)] * 16384
    texl = [(0,0,0)] * 16384
    texc = [(0,0,0,0)] * 16384

    new_imgh = Image.new('RGB', (128, 128))
    new_imgl = Image.new('RGB', (128, 128))
    new_imgc = Image.new('RGBA', (128, 128))

    TexXYZ = Image.new('RGB', (128, 256))
    
    i = 0
    attrlist = {}
    attrlist['names'] = []

    try:
        for row in csvreader:
            #print(row[7])
            my_list = row[7].split(";")
            attrlist['names'].append(my_list)
            
            x = int(float(row[0])*65280)
            y = int(float(row[1])*65280)
            z = int(float(row[2])*65280)
            r = int(row[3])
            g = int(row[4])
            b = int(row[5])
            a = int(row[6])
            xh = int(x / 255)
            yh = int(y / 255)
            zh = int(z / 255)
            xl = x % 255
            yl = y % 255
            zl = z % 255
            pixelh = (xh,yh,zh)
            pixell = (xl,yl,zl)
            pixelc = (r,g,b,a)
            texh[i] = pixelh
            texl[i] = pixell
            texc[i] = pixelc
            i += 1

    except (IndexError, ValueError):
        return '<a style="color:red;">ERROR </a>' + name + " nodefile malformated?" 
    
    with open(path + '/names.json', 'w') as outfile:
        json.dump(attrlist, outfile)

    new_imgh.putdata(texh)
    new_imgl.putdata(texl)
    new_imgc.putdata(texc)
        
    TexXYZ.paste(new_imgh, (0, 0))
    TexXYZ.paste(new_imgl, (0, 128))
        
    pathXYZ = path + '/layouts/' +  name + 'XYZ.bmp'
    pathRGB = path + '/layoutsRGB/' +  name +  'RGB.png'

    if os.path.exists(pathXYZ):
        return '<a style="color:red;">ERROR </a>' +  name + " Nodelist already in project"
    else:
        TexXYZ.save(pathXYZ)
        new_imgc.save(pathRGB, "PNG")
        return '<a style="color:green;">SUCCESS </a>' + name + " Node Textures Created"
    
    
    
def makeLinkTex(project, name, file):
    
    f = StringIO(file)
    csvreader = csv.reader(f, delimiter=',')
    path = 'static/projects/' + project 

    with open('static/csv/'+ name +'.csv', newline='') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
 
        texl = [(0,0,0)] * 1024 * 512
        texc = [(0,0,0,0)] * 512 * 512
        new_imgl = Image.new('RGB', (1024, 512))
        new_imgc = Image.new('RGBA', (512, 512))
        i = 0
        try:
            for row in csvreader:

                sl = int(row[0]) % 128
                s = int(int (row[0]) / 128)

                el = int(row[1]) % 128
                e = int(int (row[1]) / 128)

                r = int(row[2])
                g = int(row[3])
                b = int(row[4])
                a = int(row[5])

                pixell1 = (s,sl,0)
                pixell2 = (e,el,0)
                pixelc = (r,g,b,a)

                if i < 262144:

                    texl[i*2] = pixell1
                    texl[i*2+1] = pixell2
                    texc[i] = pixelc

                i += 1

        except (IndexError, ValueError):
            return '<a style="color:red;">ERROR </a>'  +  name + " Linkfile malformated?" 

        new_imgl.putdata(texl)
        new_imgc.putdata(texc)
        pathl = path + '/links/' +  name + 'XYZ.bmp'
        pathRGB = path + '/linksRGB/' +  name +  'RGB.png'

        if os.path.exists(pathl):
            return '<a style="color:red;">ERROR </a>' +  name  + " linklist already in project"
        else:
            new_imgl.save(pathl, "PNG")
            new_imgc.save(pathRGB, "PNG")
            return '<a style="color:green;">SUCCESS </a>' +  name +  " Link Textures Created"
    
    
    

    

    
    
    
    

    
    
    

    
    
    


    
    
    

    
    
    


    


    
    

    
    
    
    
    
    

    
    

    
    

    return "successfully created node textures and names file"














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

    return "creatde image"



@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/upload', methods=['GET'])
def upload():
    prolist = listProjects()
    return render_template('upload.html', namespaces=prolist)

@app.route('/uploadfiles', methods=['GET', 'POST'])
def upload_file():
    #print("namespace", request.args.get("namespace"))
    form = request.form.to_dict()
    #print(request.files)
    #print(form)
    prolist = listProjects()
    namespace = ''
    if form["namespace"] == "New":
        namespace = form["new_name"]
        
    else:
        namespace = form["existing_namespace"]
    if not namespace:
        return "namespace fail"
    
    # GET LAYOUT
    
    if namespace in prolist:
        print('project exists')
    else:
        # Make Folders
        makeProjectFolders(namespace)





    state = ''
    layout_files = request.files.getlist("layouts")

    if len(layout_files) > 0 and len(layout_files[0].filename) > 0:
        print("loading layouts", len(layout_files))
        print(layout_files[0])
        for file in layout_files:
            # TODO: fix the below line to account for dots in filenames
            name = file.filename.split(".")[0]
            contents = file.read().decode('utf-8')
            state = state + ' <br>'+  makeNodeTex(namespace, name, contents)
            

            
            # print(contents)
            #x = validate_layout(contents.split("\n"))
            #print("layout errors are", x)
            #if x[1] == 0:
            
        #Upload.upload_layouts(namespace, layout_files)


    # GET EDGES
    edge_files = request.files.getlist("links")
    if len(edge_files) > 0 and len(edge_files[0].filename) > 0:
        print("loading links", len(edge_files))
        #Upload.upload_edges(namespace, edge_files)
        for file in edge_files:
            name = file.filename.split(".")[0]
            contents = file.read().decode('utf-8')
            state = state + ' <br>'+ makeLinkTex(namespace, name, contents)
            
    #print(state)

    return state

#@app.route('/projects', methods=['GET', 'POST'])


@app.route('/load_project', methods=['GET', 'POST'])
def loadProject():
    folder = 'static/projects/erika/'
    layoutfolder = folder + "layouts"
    layoutRGBfolder = folder + "layoutsRGB"
    linksRGBfolder = folder + "linksRGB"
    linkfolder = folder + "links"
    layouts = [name for name in os.listdir(layoutfolder)]
    layoutsRGB = [name for name in os.listdir(layoutRGBfolder)]
    links = [name for name in os.listdir(linkfolder)]
    linksRGB = [name for name in os.listdir(linksRGBfolder)]
    return jsonify(
        layouts=layouts,
        layoutsRGB=layoutsRGB,
        links = links,
        linksRGB = linksRGB 
    )

#@app.route('/nodeTex', methods=['GET', 'POST'])


       # return redirect("http://127.0.0.1:5000/" + pathXYZ, code=302)







@app.route('/image', methods=['GET', 'POST'])
def write_image():
    new_im = Image.new('RGB', (128, 128))
    i = 0
    k = random.randrange(10,255)
    l = random.randrange(10,255)
    m = random.randrange(10,255)
    for y in range (128):
        for x in range (128):
            r = (i % k)
            h = (i % l)
            q = (i % m)
            #new_im.putpixel((x, y), ((128 - x)*2, x*2, y*2))\
            new_im.putpixel((x, y), (r, h, q))

            i+=1
    #print(h)
    url = 'static/img/test.bmp'
    new_im.save(url)
    return redirect("http://127.0.0.1:5000/" + url, code=302)


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


@app.route('/Test1')
def test1():
    
    return render_template('gene-element.html')


@app.route('/Test2')
def test2():
    
    return render_template('scroll.html', data = scb1Data)

@app.route('/Test3')
def test3():
    
    return render_template('test.html')

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

