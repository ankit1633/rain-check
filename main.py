from flask import Flask, render_template, request, jsonify
import requests
import vonage

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/check_rain', methods=['POST'])
def check_rain():
    api_key = "31fb0963fbbfa9191b9426f24a5ae567"
    lat = "19.025290"
    lon = "72.853409"
    nexmo_api_key = "45eee021"
    nexmo_api_secret = "Myoc7bzzIT7XyQHw"
    phone_number = request.form['phone_number']

    parameters = {
        "lat": lat,
        "lon": lon,
        "appid": api_key,
        "cnt": 4
    }

    response = requests.get(url="https://api.openweathermap.org/data/2.5/forecast", params=parameters)
    response.raise_for_status()
    weather_data = response.json()

    code_list = [weather_data["list"][i]["weather"][0]["id"] for i in range(4)]
    will_rain = any(code <= 600 for code in code_list)

    client = vonage.Client(key=nexmo_api_key, secret=nexmo_api_secret)
    sms = vonage.Sms(client)

    if will_rain:
        response = sms.send_message({
            "from": "WeatherAlert",
            "to": phone_number,
            "text": "It's going to rain today",
        })
        if response["messages"][0]["status"] == "0":
            return jsonify({"message": "SMS sent"})
        else:
            return jsonify({"message": f"Error: {response['messages'][0]['error-text']}"})
    else:
        return jsonify({"message": "No rain expected."})

if __name__ == '__main__':
    app.run(debug=True)
