# EDA about the Fire events in Brazil and timeseries forecasting project

Within this notebook I aimed on having a better understanding the brazilian situation regarding
the number of fire events along the years, especially in Pantanal and Amazonia biomes. For those
which are not aware, this topic is so relevant that big countries (economically-wise) like Germany
and US have several remarks about how severe the punishments are to those which are practicing
these enviromental crimes. All the data was obtained direct from INPE's website (National Institute
for Spatial Research - Brazil).

## Part 1 - Exploratory Data Analysis (EDA)
In this part I made an in-depth EDA to better understand the situation for specific years and along
the years for each biome. I was able to investigate the correlation between the mean precipitation
and the number fire events along the year for several years. Also, due to a similar pattern of fire
events along the years for two sharing border biomes, I was able to investigate if the fire events
was occurring on the borders rather than distributed in the bulk of it. Last but not least,
I was able to understand the catastrophic and sad Pantanal situation and why some important environmental
organizations are talking so much about that. The first version of can be found [here](#https://github.com/ViniciusHenning/projects/blob/master/burned-brazil/burned-brazil.ipynb) and a shortenversion can be found [here](#https://github.com/ViniciusHenning/projects/blob/master/burned-brazil/final-notebook.ipynb).

## Part 2 - Timeseries forecasting for the fire events
In this part I wanted to work on the forecasting for the timeseries associated to the fire events.
Since I was rather new to timeseries forecasting at this point, I worked on a notebook with **a lot**
of information and strategies that was coming to my mind to attack the problem, [here](#https://github.com/ViniciusHenning/projects/blob/master/burned-brazil/predictive-model.ipynb). To make it easier to follow a created a shorter version of it,
containing only the relevant parts [here](#https://github.com/ViniciusHenning/projects/blob/master/burned-brazil/tidied-up-pm.ipynb).

## Part 3 - Web application for correcting the anomalies in timeseries
A part which really interested me was the anomaly in timeseries and ways to handle it. I really like
working on making nice visualization plots to highlight something that you want to show. In this part
it wasn't different: I found a great course called "timeseries talks" on [ritvikmath](#https://www.youtube.com/channel/UCUcpVoi5KkJmnE3bvEhHR0Q)
where he shows a really nice way of highlighting the anomaly events in timeseries. I made some changes in it and deployed
a web application where the user uploads a timeseries and the app spots the anomalies in the timeseries,
the user choses how many standard deviation he wantes to take into account in the residual analysis
and the application and the app, if the user wishes, return a new dataset where the anomalies are corrected
and a new prediction can be made, you can find my web application [here](#https://share.streamlit.io/viniciushenning/projects/burned-brazil/anomaly_app/anomaly_app.py).
