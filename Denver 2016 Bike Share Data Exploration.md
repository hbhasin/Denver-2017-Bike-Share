# Denver 2017 B-cycle Ridership Data Exploration and Predictive Analytics

![](https://github.com/hbhasin/Denver-2017-Bike-Share/blob/master/figures/Splash.PNG)

[Denver B-cycle](https://denver.bcycle.com/) is a non-profit public bike sharing organization operating an automated bike sharing system called Denver B-cycle. Its mission is to "serve as a catalyst to fundamentally transform public thinking and behavior by operating a bike sharing system in Denver to enhance mobility while promoting all aspects of sustainability: quality of life, equity, the environment, economic development, and public health".
![](https://github.com/hbhasin/Denver-2017-Bike-Share/blob/master/figures/Denver%20Bikes.PNG)

Denver B-cycle posts its trips data set on its website as soon as its annual report is released. Trips data have been available since 2010. The 2017 annual report and its associated dataset for this report were obtained from [Denver B-Cycle website](https://denver.bcycle.com/). 

![](https://github.com/hbhasin/Denver-2017-Bike-Share/blob/master/figures/Denver%202017%20Annual%20Report.PNG)

This study has two parts:
1.	Explore the Trips datasets and visualize the data to provide useful and interesting information.
2.	Deploy a variety of regression models to train and test the data followed by a prediction on 20 unseen samples.

# Part 1: Data Exploration

## Data Acquisition

Data for this study was downloaded from several sources and combined using the following steps:
1.	Downloaded B-cycle 2017 Trips and Kiosk data from [Denver B-Cycle website](https://www.denverbcycle.com/company). The columns names were changed to comply with Python code best practices.
2.	Created a list of the 7921 combinations of the 89 checkout/return kiosks. Used [Google Distance Matrix API](https://developers.google.com/maps/documentation/distance-matrix/) to provide the bicycling distance and time between each checkout and return kiosk. Adopted Tyler’s method of finding the average distance by taking the distance from each checkout-return pair’s distance separately then averaging it. As he pointed out in his study, this approach was taken “because of the large number of one-way streets in the Denver downtown area where the kiosks are highly clustered”. Google only supports a maximum of 2500 requests a day, it took four days to obtain this data.
3.	Obtained daily and hourly weather data via [Dark Sky API](https://darksky.net/dev/) for all of 2017. Dark Sky supports up to 1000 requests per day

### Basic Ridership Statistics 
#### Number of Rides 
The B-cycle data, as downloaded, contained 344,256 rows of trips data. This agrees with the 344,256 total trips reported in the [2017 Denver B-cycle annual report](http://denver.bcycle.com/docs/librariesprovider34/default-document-library/annual-reports/dbs_annualreport_2017_04.pdf). The breakdown was as follows:

Membership Type | Number of Trips
--------------- | -------------
Annual (And Annual Plus) | 167,644
Flex | 3,868
30 Day | 60,462
24 Hr Online | 8,159
24 Hr Kiosk | 103,471
24 Hr Rental | 652
**Total Trips** | **344, 256**

The Trips dataset reported the following breakdown:

Membership Type | Number of Trips
--------------- | -------------
24-hour Kiosk Only (Denver B-cycle) | 103,471
Annual Plus (Denver B-cycle) | 77,500
Annual (Denver B-cycle) | 76,601
Monthly (Denver B-cycle) | 60,462
Republic Rider (Annual) (Boulder B-cycle) | 7,229
24 HR (Denver B-cycle) | 5,873
Denver B-cycle Founder (Denver B-cycle) | 4,891
Flex Pass (Denver B-cycle) | 3,868
24 hour online (Denver B-cycle) | 2,250
24 HR Rental (Denver B-cycle) | 652
**Total Trips** | **344,256**

Over 1.16% of the Denver B-cycle rides (4,029 rides) had the same checkout station as return station with a trip duration of only 1 minute (Figure 1). It is very likely that the majority of these “rides” are likely people checking out a bike, and then deciding after a very short time that this particular bike doesn’t work for them.

![](https://github.com/hbhasin/Denver-2017-Bike-Share/blob/master/figures/Figure%201.PNG)

<p align="center">
FIGURE 1: TRIP DURATION WHEN CHECKOUT AND RETURN KIOSKS ARE THE SAME
</p>

There were 17,342 rows in the Trips dataset that had kiosk names not listed in the Kiosk Master List. These 17,342 rows were removed accordingly.

Removing the 4,029 rows with a trip duration of 1 minute and 17,342 rows with invalid kiosk names resulted in **322,082 Denver B-cycle rides in 2017**.

### Distance Traveled
To estimate the distance between checkout and return kiosks when they are the same, using the “average speed of all the other rides (nominal distance ridden divided by the duration), and then applying this average speed to the same-kiosk trip durations” was adopted. This resulted in **535,628 miles ridden in 2017**.

### Most Popular and Least Popular Checkout and Return Kiosks 
### Most Popular 
The following ten kiosks were the most popular checkout kiosks by number of total bike checkouts in 2017.

Checkout Kiosk | Number of Checkouts
-------------- | -------------------
16th & Wynkoop | 12,309
1350 Larimer | 7,724
13th & Speer | 7,722
1550 Glenarm | 7,643
16th & Platte | 7,258
18th & Arapahoe | 6,771
14th & Stout | 6,611
20th & Chestnut | 6,239
16th & Broadway | 6,227
16th & Little Raven | 6,025

The following ten kiosks were the most popular return kiosks by number of total bike returns in 2017.

Return Kiosk | Number of Returns
------------ | -------------------
16th & Wynkoop | 14,717
1350 Larimer | 9,502
1550 Glenarm | 8,412
16th & Platte | 7,881
13th & Speer | 7,411
16th & Broadway | 7,195
16th & Little Raven | 7,104
17th & Wewatta | 6,547
REI | 6,422
18th & Arapahoe | 6,370

### Least Popular 
The following ten kiosks were the least popular checkout kiosks by number of total bike checkouts in 2017.

Checkout Kiosk | Number of Checkouts
-------------- | -------------------
Colfax & Garfield | 1,566
33rd & Arapahoe | 1,488
14th & Elati | 1,455
Pepsi Center | 1,382
Colfax & Pearl | 1,327
4th & Walnut | 1,292
Colfax & Columbine | 1,154
39th & Fox | 304
29th & Brighton | 152
7th & Sherman | 93

The following ten kiosks were the least popular return kiosks by number of total bike returns in 2017.

Checkout Kiosk | Number of Returns
-------------- | -------------------
Colfax & Garfield | 1,446
14th & Elati | 1,403
32nd & Julian | 1,353
4th & Walnut | 1,286
Colfax & Pearl | 1,172
32nd & Clay | 999
Colfax & Columbine | 907
39th & Fox | 316
29th & Brighton | 204
7th & Sherman | 120

## Checkout Method
The 2017 dataset also includes information on the checkout method used by the rider.

Checkout_Method | Number of Checkouts
--------------- | -------------------
Rfid | 169,974
Kiosk Phone Lookup | 59,933
New Kiosk Purchase | 45,504
Kiosk Credit Card Lookup | 36,164
Mobile | 10,503
Virtual | 4

## Checkouts per Membership Type 
Denver B-cycle has a number of different membership passes. The following were the top ten by number of checkouts in 2017 (Figure 4).

Membership Type | Number of Checkouts
--------------- | -------------------
24-hour Kiosk Only (Denver B-cycle) | 96,857
Annual Plus (Denver B-cycle) | 72,715
Annual (Denver B-cycle) | 72,456
Monthly (Denver B-cycle) | 55,859
Republic Rider (Annual) (Boulder B-cycle) | 6,812
24 HR (Denver B-cycle) | 5,579
Denver B-cycle Founder (Denver B-cycle) | 4,075
Flex Pass (Denver B-cycle) | 3,657
24 hour online (Denver B-cycle) | 2,073
24 HR Rental (Denver B-cycle) | 617



![](https://github.com/hbhasin/Denver-2017-Bike-Share/blob/master/figures/Figure%204.PNG)


<p align="center">
FIGURE 4: NUMBER OF CHECKOUTS BY MEMBERSHIP TYPE IN 2017
</p>

## Map of Station Popularity
### Checkout Kiosks 

The use of Tableau aided in the creation of the following map showing the popularity of the various Checkout Kiosks (Figure 2). The size of the circle is proportional to the number of checkouts from that kiosk in 2017. 

![](https://github.com/hbhasin/Denver-2017-Bike-Share/blob/master/figures/Figure%202.PNG)

<p align="center">
FIGURE 2: CHECKOUT KIOSK LOCATIONS AND NUMBER OF CHECKOUTS IN 2017
</p>

### Return Kiosks 
Similarly, the use of Tableau aided in the creation of the following map showing the popularity of the various Return Kiosks (Figure 3). The size of the circle corresponds to the number of checkouts returned to that kiosk in 2017.

![](https://github.com/hbhasin/Denver-2017-Bike-Share/blob/master/figures/Figure%203.PNG)

<p align="center">
FIGURE 3: RETURN KIOSK LOCATIONS AND NUMBER OF RETURNS IN 2017
</p>

## Checkout Method
The 2017 dataset also includes information on the checkout method used by the rider.

Checkout_Method | Number of Checkouts
--------------- | -------------------
RFID | 169,974
Kiosk Phone Lookup | 59,933
New Kiosk Purchase | 45,504
Kiosk Credit Card Lookup | 36,164
Mobile | 10,503
Virtual | 4

## Checkouts per Membership Type 
Denver B-cycle has a number of different membership passes. The following were the top ten by number of checkouts in 2017 (Figure 4).

Membership Type | Number of Checkouts
--------------- | -------------------
24-hour Kiosk Only (Denver B-cycle) | 96,857
Annual Plus (Denver B-cycle) | 72,715
Annual (Denver B-cycle) | 72,456
Monthly (Denver B-cycle) | 55,859
Republic Rider (Annual) (Boulder B-cycle) | 6,812
24 HR (Denver B-cycle) | 5,579
Denver B-cycle Founder (Denver B-cycle) | 4,075
Flex Pass (Denver B-cycle) | 3,657
24 hour online (Denver B-cycle) | 2,073
24 HR Rental (Denver B-cycle) | 617



![](https://github.com/hbhasin/Denver-2017-Bike-Share/blob/master/figures/Figure%204.PNG)


<p align="center">
FIGURE 4: NUMBER OF CHECKOUTS BY MEMBERSHIP TYPE IN 2017
</p>

## Ridership by Calendar and Clock Variables 
### Ridership by Hour 
Bike checkout time is probably the most important attribute in the Trips dataset. Each checkout time was converted into its integer hour. For example, 7:02 AM or 7:59 AM would be converted to an integer of 7. In this way, total number of checkouts could be aggregated for the year and plotted against their hours of the day, as shown in Figure 5.

It appears that the highest number of checkouts occur between 4 PM and 5 PM with ridership increasing steadily from 10 AM onwards.

![](https://github.com/hbhasin/Denver-2017-Bike-Share/blob/master/figures/Figure%205.PNG)


<p align="center">
FIGURE 5: NUMBER OF CHECKOUTS BY HOUR IN 2017
</p>



Figure 6 shows the average distance ridden by the hour of the day in 2017. More distance is covered during the 10 AM to 2 PM period and declining steadily thereafter. There appears to be a sharp increase in distance ridden between 11 PM and midnight.

![](https://github.com/hbhasin/Denver-2017-Bike-Share/blob/master/figures/Figure%206.PNG)

<p align="center">
FIGURE 6: ESTIMATED AVERAGE MILES RIDDEN BY HOUR OF CHECKOUT IN 2017
</p>


## Ridership by Hour and Weekday 
Figure 7 shows that weekday ridership patterns are similar. On the other hand weekend ridership demonstrate a busy afternoon (between 12 PM and 3 PM)

![](https://github.com/hbhasin/Denver-2017-Bike-Share/blob/master/figures/Figure%207.PNG)

<p align="center">
FIGURE 7: CHECKOUTS BY HOUR OF DAY PER WEEKDAY IN 2017
</p>

## Ridership by Month 
Monthly checkouts, as shown in Figure 8, suggest high ridership during the summer months and low ridership during the winter months.

![](https://github.com/hbhasin/Denver-2017-Bike-Share/blob/master/figures/Figure%208.PNG)

<p align="center">
FIGURE 8: TOTAL CHECKOUTS BY MONTH IN 2017
</p>

## Merging with Weather 

It is highly likely that weather plays a very important role in bike ridership and bike checkout times. This was shown in the previous plots on total checkouts per hour of the day, by weekday, and by month. To verify this, weather data obtained from Dark Sky API was merged with the Trips dataset and several graphs plotted to visualize the relationships.

### Checkouts vs. Daily Temperature 

Figure 9 shows the total number of checkouts against maximum and minimum daily temperature. It clearly suggests that ridership increases as the temperature increases and vice-versa.

![](https://github.com/hbhasin/Denver-2017-Bike-Share/blob/master/figures/Figure%209.PNG)

<p align="center">
FIGURE 9: TOTAL CHECKOUTS BY DAILY TEMPERATURE IN 2017
</p>

Apparent temperature, as defined by Dark Sky, is “apparent (or “feels like”) temperature in degrees Fahrenheit”. It appears to have a subtle effect on bike ridership as shown in Figure 10.


![](https://github.com/hbhasin/Denver-2017-Bike-Share/blob/master/figures/Figure%2010.PNG)

<p align="center">
FIGURE 10: TOTAL CHECKOUTS BY DAILY APPARENT TEMPERATURE IN 2017
</p>


## Checkouts vs. Daily Cloud Cover 
Dark Sky defines Cloud Cover as “the percentage of sky occluded by clouds, between 0 and 1, inclusive”. Figures 11 shows the total number of checkouts against daily cloud cover. They clearly suggest that ridership is highest as the cloud cover stays at around 0.15.

![](https://github.com/hbhasin/Denver-2017-Bike-Share/blob/master/figures/Figure%2011.PNG)

<p align="center">
FIGURE 11: TOTAL CHECKOUTS BY DAILY CLOUD COVER IN 2017
</p>

## Checkouts vs. Daily Wind Speed 
Wind speed is reported in miles per hour. As shown in Figure 12, ridership does not seem to be somewhat impacted by higher wind speeds. 

![](https://github.com/hbhasin/Denver-2017-Bike-Share/blob/master/figures/Figure%2012.PNG)

<p align="center">
FIGURE 12: TOTAL CHECKOUTS BY DAILY WIND SPEED IN 2017
</p>

## Checkouts vs. Daily Humidity 
Humidity is defined by Dark Sky as “relative humidity, between 0 and 1. Figure 13 shows decreased ridership at higher humidity levels.

![](https://github.com/hbhasin/Denver-2017-Bike-Share/blob/master/figures/Figure%2013.PNG)

<p align="center">
FIGURE 13: TOTAL CHECKOUTS BY DAILY HUMIDITY IN 2017	
</p>

## Checkouts vs. Daily Visibility 
Visibility is measured in miles and capped at 10 miles, according to Dark Sky. As Figure 14 shows, ridership peaks when visibility is at 10 miles.

![](https://github.com/hbhasin/Denver-2017-Bike-Share/blob/master/figures/Figure%2014.PNG)

<p align="center">
FIGURE 14: TOTAL CHECKOUTS BY DAILY VISIBILITY IN 2017
</p>

## Days with Highest/Lowest Ridership
Another interesting data discovery was the fact that Saturdays and Sundays had the highest and lowest ridership depending upon the weather. This may be due to “‘weekend warriors’ who rent B-cycles for pleasure and are highly affected by the weather in their decision to ride”.


### Highest Ridership

Checkout Week Day | Date of Checkout | Max Temperature | Min Temperature | Number of Checkouts
----------------- | ------------------- | --------------- | --------------- | -------------------
Monday | 2017-07-03 | 84.630 | 56.460 | 1,633
Sunday | 2017-05-28 | 67.660 | 40.570 | 1,627
Friday | 2017-09-01 | 82.270 | 58.350 | 1,612
Friday | 2017-06-30 | 70.830 | 51.380 | 1,609
Saturday | 2017-06-03 | 72.020 | 48.460 | 1,593
Saturday | 2017-08-26 | 87.100 | 57.520 | 1,575
Friday | 2017-08-18 | 83.370 | 54.080 | 1,556
Saturday | 2017-08-12 | 78.570 | 55.480 | 1,552
Thursday | 2017-08-25 | 83.620 | 54.650 | 1,514
Thursday | 2017-07-07 | 81.740 | 60.810 | 1,503

### Lowest Ridership

Checkout Week Day | Date of Checkout | Max Temperature | Min Temperature | Number of Checkouts
----------------- | ------------------- | --------------- | --------------- | -------------------
Sunday | 2017-12-31 | 23.560 | 10.160 | 107
Tuedaay | 2017-12-26 | 13.700 | 8.630 | 84
Sunday | 2017-01-08 | 45.220 | 15.570 | 76
Friday | 2017-01-06 | 19.330 | -7.450 | 56
Monday | 2017-01-16 | 33.820 | 27.400 | 55
Saturday | 2017-04-29 | 30.440 | 27.190 | 52
Saturday | 2017-01-07 | 25.480 | 4.130 | 49
Monday | 2017-12-25 | 24.140 | 9.120 | 47
Sunday | 2017-12-24 | 25.330 | 2.460 | 35
Thursday | 2017-01-05 | 5.150 | 0.070 | 18

## Checkouts vs. Hourly Weather Variables
Hourly weather conditions provide better resolution than daily weather conditions. To investigate this, number of checkouts against hourly weather variables were also plotted and compared with the plots using daily weather variables.

### Checkouts vs. Hourly Temperature
The scatter plots in Figure 15 and 16 show that the relationship between the number of checkouts and the hourly temperatures are not linear.

![](https://github.com/hbhasin/Denver-2017-Bike-Share/blob/master/figures/Figure%2015.PNG)

<p align="center">
FIGURE 15: TOTAL CHECKOUTS BY HOURLY TEMPERATURE IN 2017
</p>

![](https://github.com/hbhasin/Denver-2017-Bike-Share/blob/master/figures/Figure%2017.PNG)

<p align="center">
FIGURE 16: TOTAL CHECKOUTS BY HOURLY APPARENT TEMPERATURE IN 2017
</p>

### Checkouts vs. Hourly Humidity
Figure 17 shows that humidity affects ridership significantly.

![](https://github.com/hbhasin/Denver-2017-Bike-Share/blob/master/figures/Figure%2017.PNG)

<p align="center">
FIGURE 17: TOTAL CHECKOUTS BY HOURLY HUMIDITY IN 2017	
</p>

### Checkouts vs. Hourly Cloud Cover
As shown in Figure 18 Cloud Cover certainly impacts ridership.

![](https://github.com/hbhasin/Denver-2017-Bike-Share/blob/master/figures/Figure%2018.PNG)

<p align="center">
FIGURE 18: TOTAL CHECKOUTS BY HOURLY CLOUD COVER IN 2017	
</p>

### Checkouts vs. Hourly Wind Speed
Data on wind speed indicates it is clustered heavily in 0 to 8 miles per hour range, as shown in Figure 19.

![](https://github.com/hbhasin/Denver-2017-Bike-Share/blob/master/figures/Figure%2019.PNG)

<p align="center">
FIGURE 19: TOTAL CHECKOUTS BY HOURLY WIND SPEED IN 2017	
</p>

### Checkouts vs. Hourly Visibility
As shown in Figure 20 visibility at 10 miles has the greatest impact on ridership.

![](https://github.com/hbhasin/Denver-2017-Bike-Share/blob/master/figures/Figure%2020.PNG)

<p align="center">
FIGURE 20: TOTAL CHECKOUTS BY HOURLY VISIBILITY IN 2017	
</p>
