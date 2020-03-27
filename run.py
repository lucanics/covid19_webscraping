#!/usr/bin/env python
# coding: utf-8

import os
import unicodedata
import pandas as pd
import plotly.express as px
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

baseurl = "https://gisanddata.maps.arcgis.com/apps/opsdashboard/index.html#/bda7594740fd40299423467b48e9ecf6"

def get_dashboard_html():
    '''get html from dashboard after the relevant data it done loading'''
    options = webdriver.ChromeOptions()
    options.add_argument('headless')

    driver = webdriver.Chrome(options=options)
    driver.get(baseurl)

    try:
        '''wait until the text "Austria" can be 
        found within the container with the 
        ID "ember34" (maximum of 60 seconds)'''
        wait = WebDriverWait(driver, 60).until(
            EC.text_to_be_present_in_element((By.ID, "ember34"), "Austria")
        ) 
        elem = driver.find_element_by_id("ember34")
        elem_inner = elem.get_attribute('innerHTML')
        soup_data = BeautifulSoup(elem_inner, features="html.parser")
        timestamp = driver.find_element_by_id("ember55")  # get timestamp for most recent data-upload
        soup_timestamp = BeautifulSoup(timestamp.get_attribute('innerHTML'), features="html.parser")
    finally:
        driver.quit()
        return soup_data, soup_timestamp

def extract_data_from_html():
    '''extracts data and converts it to a pandas dataframe'''
    data = []
    soup_data, soup_timestamp = get_dashboard_html()
    timestamp = soup_timestamp.find_all("svg")[-1].text.replace('\n','')
    nodes = soup_data.find("nav", class_="feature-list")
    h5_nodes = nodes.findChildren("h5")

    for node in h5_nodes:
        value = unicodedata.normalize("NFKD", node.text)
        data.append(value)

    data_split = [row.split(None, 1) for row in data]
    df = pd.DataFrame(data_split, columns=["Confirmed Cases", "Country"])
    df["timestamp"] = timestamp
    return df

df = extract_data_from_html()
filename = 'Covid-19_confirmed_cases.csv'

# if file does not exist write header 
if not os.path.isfile(filename):
   df.to_csv(filename, header='column_names', index=False)
   print(f"File {filename} successfully created")
else: # else it exists so append without writing the header
   df.to_csv(filename, mode='a', header=False, index=False)
   print(f"Successfully appended to file {filename}")