import pandas as pd
import numpy as np
import json
import re
import time
import datetime as dt
import matplotlib.pyplot as plt
import ast
import operator
from sklearn import linear_model, model_selection, feature_selection
from selenium import webdriver
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import streamlit as st
from wordcloud import WordCloud

def get_features(row):
    """ access the wanted fields from one row of data """
    try:
        location_id = row["location"]["id"]
    except:
        location_id = None
    try:
        location_name = row["location"]["name"]
    except:
        location_name = None
    try:
        tags = row["tags"]
    except:
        tags = []
    timestamp = dt.datetime.fromtimestamp(row["taken_at_timestamp"])
    try:
        address_str = json.loads(row["location"]["address_json"])
        address = address_str["street_address"]
        zip_code = address_str["zip_code"]
        city_name = address_str["city_name"]
        region_name = address_str["region_name"]
    except:
        address_str = []
        address = []
        zip_code = []
        city_name = []
        region_name = []
    return [location_id, location_name, address, zip_code, city_name, region_name, tags, timestamp]

@st.cache
def loadData():
    filepath = '../DataScraping/20k.json'
    with open(filepath, encoding ='utf8') as f:
        data = json.load(f)
    data = data["GraphImages"]
    df = pd.DataFrame(list(map(get_features, data)),
        columns = ["location_id", "location_name", "address", "zip_code", "city_name", "region_name", "tags", "timestamp"])
    return df