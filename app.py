from flask import Flask,request
import joblib
from sklearn import model_selection
from sklearn.linear_model import LogisticRegression
import pickle
app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
  return 'Hello World!'

@app.route('/weather/predict', methods=['GET'])
def predict_weather():
  inparray = [request.json["precipitation"],request.json["temp_max"],request.json["temp_min"],request.json["wind"]]
  filename = 'finalized_model.sav'
  loaded_model = joblib.load(filename)
  result = loaded_model.predict([inparray])
  print(result)
  if(result == 1):
    weather = "rain"
  else:
    weather = "sunny"
  return {"weather":weather}

@app.route('/weather/accuracy', methods=['GET'])
def weather_accuracy():
  return {"accuracy":.8464163822525598}

@app.route('/music/predict', methods=['GET'])
def predict_music():
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
      0:'pop',
      1:'rap',
      2:'rock',
      3:'latin',
      4:'r&b',
      5:'edm'
    }
    music = replace_dict[0]
    return {"music genre":music}

@app.route('/music/accuracy', methods=['GET'])
def music_accuracy():
  return {"accuracy":.5509365006852444}




if __name__ == '__main__':
  app.run()
