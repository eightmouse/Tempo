#--- Modules ---#
import fastapi
from fastapi import Query
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import requests

app = fastapi.FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost", "http://127.0.0.1"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

@app.get("/")

def home(city: str = Query(default="London", max_length=50)):

    headers = {'User-Agent': 'Mozilla/5.0'}

    photon_url = f"https://photon.komoot.io/api/?q={city}&limit=1"
    response = requests.get(photon_url, headers=headers)
    location_data = response.json()

    descriptions = {
        0: "Sunny",
        1: "Mainly Clear",
        2: "Partly Clody",
        3: "Overcast"
    }

    if location_data['features']:

        coords = location_data['features'][0]['geometry']['coordinates']
        url = f"https://api.open-meteo.com/v1/forecast?latitude={coords[1]}&longitude={coords[0]}&current_weather=true"    

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            print(f"DEBUG DATA: {data}")

            temperature = data['current_weather']['temperature']
            weathercode = data['current_weather']['weathercode']

            status = descriptions.get(weathercode, "Unknown")

            print(f'API request successful.')

            return {
                "City": city,
                "Temperature": temperature,
                "Description": status,
                    }
        
        except requests.exceptions.RequestException as e:
            print(f'API request failed: {e}')
            return {"error": "Could not fetch weather"}
        
    else:
        return {"error": "City not found"}
