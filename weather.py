import keyring
import requests


def get_weather():
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    city = 'Almaty'
    params = {
        'q': city,
        'appid': keyring.get_password('weather', 'api'),
        'units': 'metric',
        'lang': 'ru'
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        print(data)
        weather = data['weather'][0]['description']
        temperature = data['main']['temp']
        return f"Погода в {city}: {weather} Температура: {temperature}°C"
    else:
         return f"Не удалось получить данные о погоде для города {city}."





