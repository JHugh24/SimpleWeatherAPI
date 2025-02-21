import requests
from configobj import ConfigObj
from dotenv import load_dotenv
import os


config_file_name = 'weather.ini'
config = ConfigObj()

try:
    config = ConfigObj(config_file_name)
except Exception as e:
    config.filename = config_file_name


city_name = ''
state_code = ''
country_code = ''


try:
    city_name = config['city_name']
    state_code = config['state_code']
    country_code = config['country_code']
except Exception as e:
    if e.args[0] == 'city_name':
        print("No location saved, please enter your location information as follows:")
    else: print(f'Error encountered: {e}')


if city_name == '':
    print('Enter your city:')
    city_name = input()
    config['city_name'] = city_name

if state_code == '':
     print('Enter your 2 digit state code:')
     state_code = input()
     config['state_code'] = state_code

if country_code == '':
     print('Enter your 2 digit country code:')
     country_code = input()
     config['country_code'] = country_code


config.write()

limit = 1
unit_type = 'imperial'

load_dotenv()
api_key = os.getenv('API_KEY')

geocoding_endpoint_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name},{state_code},{country_code}&limit={limit}&appid={api_key}"

geo_response = requests.get(url=geocoding_endpoint_url)
geo_response = geo_response.json()

lat = geo_response[0]["lat"]
lon = geo_response[0]["lon"]

weather_endpoint_url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&appid={api_key}&units={unit_type}"
response = requests.get(url=weather_endpoint_url)
response = response.json()

print(f"The current temp in {city_name} is {response['current']['temp']}")