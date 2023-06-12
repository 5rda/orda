import requests

def get_weather(lat, lon, api_key):
    url = f"http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}&units=metric&lang=en"
    
    response = requests.get(url)
    return response.json()