import os
import requests
from flask import Flask, render_template
from PIL import Image

app = Flask(__name__)

# Bursa'nın koordinat bilgileri
LATITUDE = 40.1885
LONGITUDE = 29.0610

# Resim klasörü ve hava durumu API URL'si
IMAGE_FOLDER = 'static/images'  # Resim klasörünün yolunu belirtin
WEATHER_API_URL = f"https://api.open-meteo.com/v1/forecast?latitude={LATITUDE}&longitude={LONGITUDE}&current_weather=true"

@app.route("/")
def index():
    # Resimleri klasörden yükleme
    image_files = [f"images/{file}" for file in os.listdir(IMAGE_FOLDER) if file.endswith(('.png', '.jpg', '.jpeg'))]
    
    # Hava durumu verisini çekme
    weather_data = {}
    try:
        response = requests.get(WEATHER_API_URL)
        data = response.json()
        if 'current_weather' in data:
            weather_data = {
                "temperature": data['current_weather']['temperature'],
                "description": data['current_weather']['weathercode']
            }
    except Exception as e:
        print("Hava durumu verisi alınamadı:", e)
    
    return render_template("index.html", images=image_files, weather=weather_data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
