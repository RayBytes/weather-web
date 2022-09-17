from flask import Flask as fl, render_template, request
import requests
import json

app = fl(__name__)

with open("config.json") as file:
    data = json.load(file)

def getWeather(place):
    req = requests.get(f"http://api.weatherapi.com/v1/current.json?key={data['apikey']}&q={place}&aqi=no"); response = json.loads(req.text)
    if 'error' in req.text:
        return f"{response['error']['message']}"
    
    return response

@app.route('/')
def form():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def index():
    text = request.form['Input a place']
    if text == "":
        return render_template("error.html", error="Nothing has been inputed")
        
    data = getWeather(text)
    if " " in data:
        return render_template("error.html", error=data)
    return render_template("weather.html", imgsrc = data['current']['condition']['icon'], feelslike=data['current']['feelslike_c'], temperature= data['current']['temp_c'], country= data['location']['country'], region=data['location']['region'])



if __name__ == "__main__":
  app.run()