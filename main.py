import requests

def get_weather(city: str):
    headers = {'User-Agent': 'Mozilla/5.0'}

    # 1. Get City Coordinates
    photon_url = f"https://photon.komoot.io/api/?q={city}&limit=1"
    
    try:
        response = requests.get(photon_url, headers=headers)
        response.raise_for_status()
        location_data = response.json()
    except requests.exceptions.RequestException:
        print("Error: Could not connect to the city search service.")
        return

    descriptions = {
        0: "Sunny",
        1: "Mainly Clear",
        2: "Partly Cloudy",
        3: "Overcast"
    }

    # 2. Check if city exists
    if location_data['features']:
        coords = location_data['features'][0]['geometry']['coordinates']
        url = f"https://api.open-meteo.com/v1/forecast?latitude={coords[1]}&longitude={coords[0]}&current_weather=true"    

        # 3. Get Weather
        try:
            weather_response = requests.get(url)
            weather_response.raise_for_status()
            data = weather_response.json()

            temperature = data['current_weather']['temperature']
            weathercode = data['current_weather']['weathercode']
            status = descriptions.get(weathercode, "Unknown")

            # --- THE TERMINAL OUTPUT ---
            print("\n" + "="*30)
            print(f"🌍 Weather for: {city.upper()}")
            print(f"🌡️  Temperature: {temperature}°C")
            print(f"☁️  Status:      {status}")
            print("="*30 + "\n")

        except requests.exceptions.RequestException:
            print("Error: Could not fetch weather data.")
            
    else:
        print(f"Error: City '{city}' not found.")

# --- This is the new "Engine Starter" ---
if __name__ == "__main__":
    print("Tempo")
    while True:
        user_city = input("Enter a city name (or type 'quit' to exit): ")
        
        if user_city.lower() == 'quit':
            print("Goodbye!")
            break
            
        get_weather(user_city)