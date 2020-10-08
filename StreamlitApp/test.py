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

st.title('Seasonal hotspots')

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

def loadData():
    filepath = '../DataScraping/100k.json'
    with open(filepath, encoding = 'utf8') as f:
        data = json.load(f)
    data = data["GraphImages"]
    df = pd.DataFrame(list(map(get_features, data)),
        columns = ["location_id", "location_name", "address", "zip_code", "city_name", "region_name", "tags", "timestamp"])
    end = time.time()
    return df

df=loadData()

def get_top_tags(df):
    tag_counts = {}
    for tags in df.tags.values:
        if(tags):
            for tag in ast.literal_eval(str(tags)):
                if tag in tag_counts:
                    tag_counts[tag] += 1
                else:
                    tag_counts[tag] = 1
    tag_counts = sorted(tag_counts.items(), key=operator.itemgetter(1), reverse=True)
    top_tags = map(lambda row: row[0], tag_counts[0:1000])
    return list(top_tags)
top_tags=get_top_tags(df)

# Create and generate a word cloud image:
wordcloud = WordCloud().generate(str(top_tags))
# Display the generated image:
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
#plt.show()
st.pyplot(plt)

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def remote_css(url):
    st.markdown(f'<link href="{url}" rel="stylesheet">', unsafe_allow_html=True)    

selected = st.text_input("", "Search...")
print(selected)
button_clicked = st.button("OK")