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
