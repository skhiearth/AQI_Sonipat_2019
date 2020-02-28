import pandas as pd
import requests
from datetime import datetime
import os

# Dark Sky Secret Key
secret_key = '46d8abf841357ef2fe310170ad26ce87'

# Sonipat Coordinates
SON_LAT = '28.9287'
SON_LONG = '77.0912'

# Reading in the AQI data
df = pd.read_excel("AQI_Sonipat_2019/Sonipat_AQI.xlsx")

# Copying data frame to new frame to extract dates
df_date_weather = df.copy()['Date']
frame = {'date': df_date_weather} 
df_date_weather = pd.DataFrame(frame) 

# Weather API
minTemp = []
maxTemp = []
precipIntensity = []
pressure = []
humidity = []
windSpeed = []
windBearing = []
cloudCover = []

count = 1

for date in df_date_weather['date'].dt.date:
    if(count%10 == 0):
        print(count)
    date_time = str(date) + "T11:00:00"
    link = "https://api.darksky.net/forecast/{}/{},{},{}".format(secret_key, SON_LAT, SON_LONG, date_time)
    
    # Sending GET request and saving the response as a response object
    r = requests.get(url = link)
    
    # Unpacking data in JSON Format
    data = r.json() 

    toAdd = data['daily']['data']

    for val in toAdd:
        minTemp.append(round(((val['temperatureMin'] - 32) * 5/9), 2))
        maxTemp.append(round(((val['temperatureMax'] - 32) * 5/9), 2))
        precipIntensity.append(val['precipIntensity'])
        pressure.append(val['pressure'])
        humidity.append(val['humidity'])
        windSpeed.append(val['windSpeed'])
        windBearing.append(val['windBearing'])
        cloudCover.append(val['cloudCover'])

    count = count + 1


# Adding the result to the dataframe
df_date_weather['Min_Temp'] = minTemp
df_date_weather['Max_Temp'] = maxTemp
df_date_weather['Precip_Intensity'] = precipIntensity
df_date_weather['Pressure'] = pressure
df_date_weather['Humidity'] = humidity
df_date_weather['Wind_Speed'] = windSpeed
df_date_weather['Wind_Bearing'] = windBearing
df_date_weather['Cloud_Cover'] = cloudCover

horizontal_stack = pd.concat([df, df_date_weather], axis=1)
horizontal_stack = horizontal_stack.drop(['date'], axis = 1) 

horizontal_stack.to_csv("AQI_Sonipat_2019/Sonipat_AQI_Weather.csv")