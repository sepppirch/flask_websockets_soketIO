from flask import Flask, jsonify, request,g, render_template
from flask import Flask, flash, request, redirect, url_for
from flask import Flask, session
import json

import sendRequest as sreq

idata = {'mes': 'dfhdfhfh', 'usr': 'NaS7QA89nxLg9nKQAAAn', 'tag': 'flask'}

app = Flask(__name__)


###RECEIVE INCOMING WEBSOCKET MSG FROM NODE.JS 
@app.route('/flask', methods=['GET', 'POST'])
def wsreceiver():
    if request.method == 'POST':
        #data = request.form
        data =request.get_json()
    else:
        data = request.args

    global idata
    idata = data
    #print(idata)


    #data["tag"] = "flask"
    #astring = data["usr"]
    #print(data)

    sreq.send('http://127.0.0.1:3000/in', data)


    return 
    
@app.route('/')
def index():
    
    return render_template("index.html", data=idata)


if __name__ == "__main__":
    app.run(port=5000, debug=True)


