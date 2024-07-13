import keyring
import requests
from datetime import date


todays_date = date.today().strftime("%Y-%m-%d")

nasa_api = keyring.get_password('nasa', 'api')

nasa_url = "https://api.nasa.gov/neo/rest/v1/feed?start_date=" + todays_date +"&end_date="+ todays_date + "&api_key="+nasa_api

response = requests.get(nasa_url)

res_json = response.json()



def closest_asteroid(near_earth_objects):
    asteroid = []
    for i in range(0, len(near_earth_objects)):
        asteroid.insert(i, near_earth_objects[i]['close_approach_data'][0]['miss_distance']['kilometers'])
    return asteroid.index(min(asteroid))


def detector():
    if "near_earth_objects" in res_json:
        near_asteroids = res_json['near_earth_objects'][todays_date]
        closest_asteroid_index = closest_asteroid(near_asteroids)


    name = near_asteroids[closest_asteroid_index]['name']
    how_close = near_asteroids[closest_asteroid_index]['close_approach_data'][0]['miss_distance']['kilometers']
    diameter = near_asteroids[closest_asteroid_index]['estimated_diameter']['meters']['estimated_diameter_max']

    how_close_str = str(round(float(how_close)))
    diameter_str = str(round(diameter))

    alert = "Ближайший астероид сегодня - " + name + ". Он находится в " + how_close_str + " км от Земли. Его диаметр составляет " + diameter_str + " метров."

    return alert

