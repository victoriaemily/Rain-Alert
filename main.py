import requests
from twilio.rest import Client
from datetime import date
from twilio.http.http_client import TwilioHttpClient
import os

#constants
OWM_API_KEY = "os.environ.get("OWN_API_KEY")"
OWM_ENDPOINT = "https://api.openweathermap.org/data/2.5/forecast"
#cstat coords :)
MY_LON=-96.325500
MY_LAT=30.612910

ACCT_SID = "os.environ.get("ACCT_SID")"
AUTH_TOKEN = "os.environ.get("AUTH_TOKEN")"

today = str(date.today())
todays_date = today[8:]
will_rain = False

#wakeup hour can be changed to filter out rain times after wakeup
wakeup_hour = 6

OWM_PARAMS = {
    "lon": MY_LON,
    "lat": MY_LAT,
    "appid": OWM_API_KEY,
}

response = requests.get(OWM_ENDPOINT,OWM_PARAMS)
data = response.json()

forecasts = data['list']

for forecast in forecasts:
    weather = forecast['weather'][0]['id']
    time = forecast['dt_txt']
    hour_of_time = int(time[11:13])
    day = int(time[8:10])
    if weather < 700 and hour_of_time > wakeup_hour and day == int(todays_date):
        will_rain = True
if will_rain == True:
    proxy_client = TwilioHttpClient()
    proxy_client.session.proxies = {'https': os.environ['https_proxy']}

    client = Client(ACCT_SID, AUTH_TOKEN, http_client=proxy_client)
    message = client.messages \
        .create(
        body="It's raining today, bring an umbrella! ☔",
        from_='+19853797328',
        to='+18323404253'
    )
    print(message.status)