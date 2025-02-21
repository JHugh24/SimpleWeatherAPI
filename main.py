import requests
from configobj import ConfigObj
from dotenv import load_dotenv
from os import getenv

# Sets the file name for the config and creates the initial config variable
config_file_name = 'weather.ini'
config = ConfigObj()
# If the config file has been created it sets the config variable to that file, otherwise it sets the filename variable for the initial config variable
try:
    config = ConfigObj(config_file_name)
except Exception as e:
    config.filename = config_file_name

# Initializes the city name, state code, and country code variables (csc vars) as empty strings
city_name = ''
state_code = ''
country_code = ''

# Sets the initialized csc vars to the values stored in the config file if available, otherwise sends message requesting location input
try:
    city_name = config['city_name']
    state_code = config['state_code']
    country_code = config['country_code']
except Exception as e:
    if e.args[0] == 'city_name':
        print("No location saved, please enter your location information as follows:")
    else: print(f'Error encountered: {e}')

# Checks for empty strings in csc vars and requests input for any missing data, sets values in config file as well
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

# Writes to the config file and creates it if it doesn't already exist 
config.write()

# Sets limit which indicates number of responses from call, sets unit type for returned values such as temperature
limit = 1
unit_type = 'imperial'

# Loads dotenv to read .env file and gets api key from it
load_dotenv()
api_key = getenv('API_KEY')

# Creates URL for geocoding API GET request 
geocoding_endpoint_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name},{state_code},{country_code}&limit={limit}&appid={api_key}"

# Sends get request to created geocoding URL and sets it to response variable, parses response into JSON data for easier access
geo_response = requests.get(url=geocoding_endpoint_url)
geo_response = geo_response.json()

# Gets latitude and longitude data for given csc vars
lat = geo_response[0]["lat"]
lon = geo_response[0]["lon"]

# Uses lat and lon data to create URL for weather API GET request
weather_endpoint_url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&appid={api_key}&units={unit_type}"

# Sends get request to created weather URL and sets it to response variable, parses response into JSON data for easier access
weather_response = requests.get(url=weather_endpoint_url)
weather_response = weather_response.json()

# Prints city name and current temperature 
print(f"The current temperature in {city_name} is {weather_response['current']['temp']}")