from forecastiopy import *
import csv
import os
import pandas as pd
import datetime
import time

apikey = 'Your Key'
 
Denver = [39.742043, -104.991531, 1480575600]
Denver_Time = 1451606400
 
fio = ForecastIO.ForecastIO(apikey,
                            latitude=Denver[0],
                            longitude=Denver[1],
                            time=str(Denver[2])) 
print 'Latitude', fio.latitude, 'Longitude', fio.longitude
print 'Timezone', fio.timezone
print fio.get_url() # You might want to see the request url
print

req_list = {}
b_mth = '12/'
for b_day in range(1,32):
    dt = datetime.datetime(2017, 12, b_day, 0, 0)
    req_list[b_mth + str(b_day) + '/2017'] = int((time.mktime(dt.timetuple())))

sortedReqList = sorted(req_list.items())

    
columns = ['Date', 'Hour', 'apparentTemperature', 'cloudCover', 'humidity', 'temperature', 'time', 'visibility', 'windSpeed']
index = ['Row']
dF = pd.DataFrame(columns = columns, index = index)
dF1= pd.DataFrame(columns = columns, index = index)
csv_file = "Denver_Jan_Hourly_2017_Forecast.csv"

for req_day in sortedReqList:
    Denver_Time = req_day[1]
    fio = ForecastIO.ForecastIO(apikey,
                            latitude=Denver[0],
                            longitude=Denver[1],
                            time=str(Denver_Time))

    if fio.has_hourly() is True:
        hourly = FIOHourly.FIOHourly(fio)

        for hour in xrange(0, hourly.hours()):
            print 'Hour', hour+1
            for item in hourly.get_hour(hour).keys():
                print item + ' : ' + str(hourly.get_hour(hour)[item])
                dF['Date'] = req_day[0]
                dF['Hour'] = int(hour)
                if item == 'time':
                    dF[str(item)] = hourly.get_hour(hour)[item]
                if item == 'cloudCover':
                    dF[str(item)] = hourly.get_hour(hour)[item]
                if item == 'temperature':
                    dF[str(item)] = hourly.get_hour(hour)[item]
                if item == 'apparentTemperature':
                    dF[str(item)] = hourly.get_hour(hour)[item]
                if item == 'windSpeed':
                    dF[str(item)] = hourly.get_hour(hour)[item]
                if item == 'humidity':
                    dF[str(item)] = hourly.get_hour(hour)[item]
                if item == 'visibility':
                    dF[str(item)] = hourly.get_hour(hour)[item]
            dF1 = dF1.append(dF)   
    else:
        print 'No Hourly data'

#csv_file = "C:\Temp\Jan2017.csv"
dF1.to_csv(csv_file, sep=',')

new_dF = pd.read_csv(csv_file,index_col=0)
print new_dF
