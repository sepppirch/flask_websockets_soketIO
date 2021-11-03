from flask import Flask
from flask.wrappers import Request

app = Flask(__name__)

@app.route('/flask', methods=['GET'])
def index():
    print(Request)
    return "Flask server"

if __name__ == "__main__":
    app.run(port=5000, debug=True)