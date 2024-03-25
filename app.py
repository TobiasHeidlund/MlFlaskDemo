from flask import Flask, request, jsonify
import joblib

import jwt
from datetime import timezone
from datetime import datetime
from datetime import timedelta
from jwt.exceptions import InvalidSignatureError
from sklearn import model_selection
from sklearn.linear_model import LogisticRegression
import pickle

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/weather/predict', methods=['GET'])
def predict_weather():
    if verifyToken(request.headers) == False:
        return "Invalid token", 403
    inparray = [request.json["precipitation"], request.json["temp_max"], request.json["temp_min"], request.json["wind"]]
    filename = 'finalized_model.sav'
    loaded_model = joblib.load(filename)
    result = loaded_model.predict([inparray])
    print(result)
    if (result == 1):
        weather = "rain"
    else:
        weather = "sunny"
    return {"weather": weather}


@app.route('/weather/accuracy', methods=['GET'])
def weather_accuracy():
    if verifyToken(request.headers) == False:
        return "Invalid token", 403
    return {"accuracy": .8464163822525598}


@app.route('/music/predict', methods=['GET'])
def predict_music():
    if verifyToken(request.headers) == False:
        return "Invalid token", 403

    inparray = [request.json["danceability"],
                request.json["key"],
                request.json["loudness"],
                request.json["mode"],
                request.json["speechiness"],
                request.json["acousticness"],
                request.json["instrumentalness"],
                request.json["liveness"],
                request.json["valence"],
                request.json["tempo"],
                request.json["duration_ms"]]
    filename = 'finalized_music.pbz2'
    loaded_model = joblib.load(filename)
    result = loaded_model.predict([inparray])
    print(result)
    replace_dict = {
        0: 'pop',
        1: 'rap',
        2: 'rock',
        3: 'latin',
        4: 'r&b',
        5: 'edm'
    }
    music = replace_dict[0]
    return {"music genre": music}


@app.route('/music/accuracy', methods=['GET'])
def music_accuracy():
    if verifyToken(request.headers) == False:
        return "Invalid token", 403
    return {"accuracy": .5509365006852444}




secret = "BYT UT MOT NÅGOT HÄMLIGT"
def verifyToken(headers):
    token = headers.get('Authorization')[7:]
    print(token)
    try:
        encoded = jwt.decode(token, secret, algorithms=['HS256'], verify=True)
        return encoded
    except Exception:
        return False


@app.route('/login', methods=['POST'])
def login_user():
    username = request.json['username']
    password = request.json['password']
    encoded = jwt.encode({'username': username,
                          "exp": datetime.now(tz=timezone.utc) + timedelta(days=30),
                          "iat": datetime.now(tz=timezone.utc)
                          }, secret, algorithm='HS256')
    return {"token": encoded}


if __name__ == '__main__':
    app.run()
