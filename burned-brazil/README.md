# EDA about the Fire events in Brazil and timeseries forecasting project

Within this notebook I aimed on having a better understanding the brazilian situation regarding
the number of fire events along the years, especially in Pantanal and Amazonia biomes. For those
which are not aware, this topic is so relevant that big countries (economically-wise) like Germany
and US have several remarks about how severe the punishments are to those which are practicing
these enviromental crimes. All the data was obtained directly from INPE's website (National Institute
for Spatial Research - Brazil).

## Files description:
- burned-brazil.ipynb: notebook containing the exploratory data analysis part
- dataset-creation.ipynb: notebook containing the functions which create smaller datasets to be used in the
[webapp](https://share.streamlit.io/viniciushenning/projects/burned-brazil-app/burned-brazil/webapp/webapp.py)
- predictive-model.ipynb: first draft on the timeseries forecasting of fire events in Brazil and some thoughts to better understand it.
- tidied-up-pm.ipynb: tidied up and elongated version of the timeseries forecasting part
- webapp folder: folder containing the [web application](https://share.streamlit.io/viniciushenning/projects/burned-brazil-app/burned-brazil/webapp/webapp.py) about the fire events in Brazil)
- anomaly_app folder: folder containing the [web application about anomaly](https://share.streamlit.io/viniciushenning/projects/working-branch/burned-brazil/anomaly_app/anomaly_app.py) in timeseries

## Part 1 - Exploratory Data Analysis (EDA)
In this part is made an in-depth EDA to better understand the situation for specific years and along
the years for each biome. I was able to investigate the correlation between the mean precipitation
and the number fire events along the year for several years. Also, due to a similar pattern of fire
events along the years for two sharing border biomes, I was able to investigate if the fire events
was occurring on the borders rather than distributed in the bulk of it. Last but not least,
I was able to understand the catastrophic and sad Pantanal situation and why some important environmental
organizations are talking so much about that [here](https://github.com/ViniciusHenning/projects/blob/master/burned-brazil/burned-brazil.ipynb) and a shortenversion can be found [here](https://github.com/ViniciusHenning/projects/blob/master/burned-brazil/final-notebook.ipynb).

## Part 2 - Timeseries forecasting for the fire events
In this part I wanted to work on the forecasting for the timeseries associated to the fire events.
Since I was rather new to timeseries forecasting at this point, I worked on a notebook with **a lot**
of information and strategies that was coming to my mind to attack the problem, [here](https://github.com/ViniciusHenning/projects/blob/master/burned-brazil/predictive-model.ipynb).
When getting more mature about the topic, I wrote a more clean version [here](https://github.com/ViniciusHenning/projects/blob/master/burned-brazil/tidied-up-pm.ipynb).
One can clearly see the relevance of anomalies in timeseries and how properly handling them increases the model's performance
by a huge factor (in this case one obtains an improvement of roughly 280\%). Afterwards we adapt the timeseries to use
XGBoost to forecast the result it is obtained an even better result. To see how further one can go, some feature engineering
is performed in an attempt to improve it even further, however, the latter makes the model worse.

## Part 3a - Web application for correcting the anomalies in timeseries
A part which really interested me was anomalies in timeseries and ways to handle it. I really like
working on making nice visualization plots to highlight something that one wants to show. In this part
it wasn't different: I found a great course called "timeseries talks" on [ritvikmath](https://www.youtube.com/channel/UCUcpVoi5KkJmnE3bvEhHR0Q)
where he shows a really nice way of highlighting the anomaly events in timeseries. I made some changes in it and deployed
a web application where the user uploads a timeseries and the app spots the anomalies in it
based on a careful residual analysis. If the user wishes,the web app returns a new dataset where the anomalies are corrected
and a new prediction can be made, you can find my web application [here](https://share.streamlit.io/viniciushenning/projects/working-branch/burned-brazil/anomaly_app/anomaly_app.py).

**How to:** the way to use this web application is pretty simple:

1st: you upload a timeseries to be analyzed by the web application;
2nd: you chose the datetime column to be used. Generally it is the first column, however, someone can interchange it
and put it as the second column. So the app provides the chance to change it so it can perform the analysis.
3rd: you choose the data acquisition of your data: if it is a daily/biweekly/semimonthly, monthly, etc... If it is not
(if it is a random data acquisition), you can use the [resample function](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.resample.html)
from pandas to handle it properly. 
4th: enjoy the app!
It provides several features of the timeseries that you can check:
- Seasonal-trend-residuals decomposition; decomposes the timeseries in its seasonal, trend and residual part.
- Timeseries after removing the residuals: if the timeseries is not written after a exponential transformation, for instance
(where the season, trend and residuals composem themselves as a multiplication) the timeseries = seasonal+trend+residuals. 
The residuals encompass the anomalies and they are used to spot it. This options allows the user to have a better feeling
about which points in his timeseries are anomalies by comparing how it would be **without the residuals**.
- Residual analysis: it analyses the residuals and it calculates its standard deviation and mean. The user then chooses
how many std wants to be considered (generally it is $3\sigma$), defining a range for what is going to be  considered
as anomaly anomaly (beyond this threshold) or not (below this threshold). All that can be clearly seen graphically.
- Anomaly points in the timeseries: based on the number of standard deviations chosen, it spots as red diamonds in the
ordinary timeseries the anomalies, so the user can see what points have to be treated.
- The corrected timeseries after the handling the anomalies: I provide a straightforward way where the app analyses
the other points for the same period of other years and correct the anomaly by the mean value.

The user has the option to download the corrected timeseries and use for making forecastings. As an example
one could download the files "prec.csv" and "fire.csv" from my [github folder](https://github.com/ViniciusHenning/projects/tree/master/burned-brazil/anomaly_app)
and usem to see how the app works. The data acquisition is semimonthly. For better understand the role
of anomaly in timeseries you can follow along my [jupyter notebook](https://github.com/ViniciusHenning/projects/blob/master/burned-brazil/tidied-up-pm.ipynb)
 and see that after implementing the anomaly correction there is a **huge** gain in the forecasting.

## Part 3b - Web application about the fire distribution in Brazil

[This web applicatiion](https://share.streamlit.io/viniciushenning/projects/burned-brazil-app/burned-brazil/webapp/webapp.py)
access the INPE's dataset and make live plots about content ask by the reader like:
1) The fire distribution of fire events in Brazil shown in the Brazil map;
2) Given a specific year, the user can choose an specific biome and the app finds the corresponding biome,
plot the fire distribution of that biome in the map of Brazil, highlight the percentage of the fire
distribution of that biome in a pie chart for the rest of the biomes and shows the timeseries
of fire events for the chosen biome and year along with its mean precipitation.
Note. 1: since it access the dataset itself rather than ready images, it take few seconds to load everything.
I believe that it is nicer than the images themselves, since it is easy to be used if we have access to other
datasets (from future years, for instance).
Note. 2: Since the dataset is quite big and there is a limitation of the cloud that I was using, I rework
a bit the dataset from INPE to make it a bit smaller.

