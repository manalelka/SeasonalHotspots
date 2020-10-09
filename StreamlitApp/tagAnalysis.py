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
from loadingData import *

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
    
@st.cache
def plotWordCloud(top_tags):
    wordcloud = WordCloud().generate(str(top_tags))
    return wordcloud

def findMonthsForTag(df,tag):
    times_df  = pd.DataFrame(columns = ['Tag', 'Timestamps'])
    for ind in df.index: 
        if(df['tags'][ind]):
            if(tag in str(df.iloc[ind][6])):
                temp=pd.DataFrame([[tag,df.iloc[ind][7].strftime('%#m')]], columns= ['Tag', 'Timestamps'])
                times_df=times_df.append(temp,ignore_index = True)
    times_df=(times_df.groupby('Tag')['Timestamps']
       .apply(lambda x: ','.join(map(str, x)))
       .reset_index())
    return times_df

def tagTimestamps(df,interestingTag):
    res=findMonthsForTag(df,interestingTag)
    if(res.empty==False):
        months = list(map(int, (res['Timestamps'].values)[0].split(",")))
        fig, ax = plt.subplots()
        bins = np.arange(1,14)
        ax.hist(months, bins = bins, edgecolor="k", align='left')
        ax.set_xticks(bins[:-1])
        ax.set_xticklabels([dt.date(1900,i,1).strftime('%b') for i in bins[:-1]] )
        title='Use of the tag "'+interestingTag+ '" along the summertime.'
        plt.title(title)
        plt.show()
        st.pyplot(plt)
    else:
        st.text("Tag not used.")


def plotTagHist(df):
    selected = st.text_input("", "Search...")
    if (selected != "Search..."):
        tagTimestamps(df,selected)