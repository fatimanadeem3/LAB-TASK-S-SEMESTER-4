from flask import Flask, render_template, request
import requests
from datetime import datetime

app = Flask(__name__)

API_KEY = "https://api.openweathermap.org/data/2.5/weather?lat=44.34&lon=10.99&appid=df8cb2fcea3e3dead8bc9faf6855c9ee&units=metric"

@app.route("/", methods=["GET", "POST"])
def index():
    Weather_Data = None
    if request.method == "POST":
        city = request.form.get("city")
        if city:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid=df8cb2fcea3e3dead8bc9faf6855c9ee&units=metric"
            response = requests.get(url)
            Data = response.json()
            
            if Data["cod"] == 200:
                Weather_Data = {
                    "city": Data["name"],
                    "temperature": Data["main"]["temp"],
                    "humidity": Data["main"]["humidity"],
                    "wind_speed": Data["wind"]["speed"],
                    "weather": Data["weather"][0]["description"],
                    "icon": Data["weather"][0]["icon"],
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "day": datetime.now().strftime("%A")
                }
            else:
                Weather_Data = {"error": "City not found!"}

    return render_template("index.html", weather=Weather_Data)

if __name__ == "__main__":
    app.run(debug=True)
