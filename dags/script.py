from dotenv import load_dotenv

import pandas as pd
import requests
import datetime
import os

load_dotenv(verbose=True)


API_KEY = os.getenv('API_KEY')

print(API_KEY)

location = "42.3453,-71.0514"

fields = ["temperature", "humidity"]

timesteps = ["1h"]

start_time = "nowMinus30d"

end_time = "nowMinus15d"

url = f"https://api.tomorrow.io/v4/historical?apikey={API_KEY}"

payload = {
    "location": location,
    "fields": fields,
    "timesteps": timesteps,
    "startTime": start_time,
    "endTime": end_time,
}
headers = {
    "accept": "application/json",
    "Accept-Encoding": "gzip",
    "content-type": "application/json"
}


url = f'https://api.tomorrow.io/v4/timelines?apikey={API_KEY}'

p = {'location': [53.9, 27.5], \
          'fields' : [ \
            "precipitationIntensity", \
            "precipitationType", \
            "windSpeed", \
            "windGust", \
            "windDirection", \
            "temperature", \
            "temperatureApparent", \
            "cloudCover", \
            "cloudBase", \
            "cloudCeiling", \
            "weatherCode", \
                    ], \
          'timesteps' : '1h', \
          'units' : 'metric', \
     }
    
response = requests.get(url, params=p)

print(response.json())

