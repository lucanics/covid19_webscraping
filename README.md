# Project description

Infections of Covid-19 are rapidly increasing worldwide. 
Data can help to better vizualize and understand the spread. 
This small project webscrapes the data from the dashboard: 
https://gisanddata.maps.arcgis.com/apps/opsdashboard/index.html#/bda7594740fd40299423467b48e9ecf6

This dashboard was developed by the Center for Systems Science and Engineering (CSSE) at Johns Hopkins University (JHU).
Cudos to the researchers at this University to visualize the current data. In my opinion, what was missing is to visualize
the trend over time as only the most recent data is shown.

Thus, this script collect the current data with its timestamp and saves it to a local csv file. The data can then be
processed to vizualize trends over time, which will also be a part of this project (ToDo!).


# run
* create virtualenv
* pip install requirements.txt
* python run.py
