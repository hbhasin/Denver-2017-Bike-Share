from forecastiopy import *
import csv
import os
import pandas as pd
import datetime 
import time

# Get API key from Dark Sky
apikey = 'Your Key'
 
Denver = [39.742043, -104.991531, 1451631600]
Denver_Time = 1451631600
 
fio = ForecastIO.ForecastIO(apikey,
                            latitude=Denver[0],
                            longitude=Denver[1],
                            time=str(Denver[2])) 
print 'Latitude', fio.latitude, 'Longitude', fio.longitude
print 'Timezone', fio.timezone
print fio.get_url() # You might want to see the request url
print

req_list = {}
# Change b_mth from 1 to 12 to indicate month
b_mth = '12/'
# Change second variable in range() to 32 for Jan, Mar, May, Jul, Aug, Oct, and Dec months
# Change second variable in range() to 31 for Apr, Jun, Sep and Nov months.
# Change second variable in range() to 30 for Feb.
for b_day in range(1,32):
    dt = datetime.datetime(2017, 12, b_day, 0, 0)
    req_list[b_mth + str(b_day) + '/2017'] = int((time.mktime(dt.timetuple())))
#print(req_list)
sortedReqList = sorted(req_list.items())
#for i in sortedReqList:
#    print(i)
    
columns = ['Date', 'cloudCover', 'apparentTemperatureMax', 'apparentTemperatureMin', 'temperatureMax', 'temperatureMin', 'windSpeed', 'humidity', 'visibility', 'time']
index = ['Row']
dF = pd.DataFrame(columns = columns, index = index)
dF1= pd.DataFrame(columns = columns, index = index)
# Change filename to reflect month
csv_file = "Denver_Jan_2017_Daily_Weather_Forecast.csv"

for req_day in sortedReqList:
    Denver_Time = req_day[1]
    fio = ForecastIO.ForecastIO(apikey,
                            latitude=Denver[0],
                            longitude=Denver[1],
                            time=str(Denver_Time))

    if fio.has_daily() is True:
        daily = FIODaily.FIODaily(fio)

        for day in xrange(0, daily.days()):
            #print 'Day', day+1
            for item in daily.get_day(day).keys():
                print item + ' : ' + unicode(daily.get_day(day)[item])
                #dF['Row'] = day
                dF['Date'] = req_day[0]
                if item == 'time':
                    dF[str(item)] = daily.get_day(day)[item]
                if item == 'cloudCover':
                    dF[str(item)] = daily.get_day(day)[item]
                if item == 'apparentTemperatureMax':
                    dF[str(item)] = daily.get_day(day)[item]
                if item == 'apparentTemperatureMin':
                    dF[str(item)] = daily.get_day(day)[item]
                if item == 'temperatureMax':
                    dF[str(item)] = daily.get_day(day)[item]
                if item == 'temperatureMin':
                    dF[str(item)] = daily.get_day(day)[item]
                if item == 'windSpeed':
                    dF[str(item)] = daily.get_day(day)[item]
                if item == 'humidity':
                    dF[str(item)] = daily.get_day(day)[item]
                if item == 'visibility':
                    dF[str(item)] = daily.get_day(day)[item]
            dF1 = dF1.append(dF)    
            #print
        #print
    else:
        print 'No Daily data'


#save to csv_file
dF1.to_csv(csv_file, sep=',')

new_dF = pd.read_csv(csv_file,index_col=0)
print new_dF
