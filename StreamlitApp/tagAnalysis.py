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
from selenium.webdriver.chrome.options import Options
import streamlit as st
from wordcloud import WordCloud
from loadingData import *
from datetime import *
import datetime

@st.cache
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
    tag_counts = map(lambda row: row[0], tag_counts)
    return ' '.join(list(tag_counts))

def getRankTag(tag,tagsList):
    rank = str(tagsList.index(tag)+1) + " out of " + str(len(tagsList)) + " tags"
    return rank

@st.cache
def plotWordCloud(tag_counts):
    wordcloud = WordCloud().generate(str(tag_counts[0:100])) #We only get the first 100 tags 
    return wordcloud

def findMonthsForTag(df,tag):
    times_df  = pd.DataFrame(columns = ['Tag', 'Timestamps'])
    for ind in df.index: 
        if(df['tags'][ind]):
            if(tag in str(df.iloc[ind][6])):
                temp=pd.DataFrame([[tag,df.iloc[ind][7].strftime('%m')]], columns= ['Tag', 'Timestamps'])
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
        title=' Use of the tag "'+interestingTag+ '" along the summertime. '
        plt.title(title)
        plt.show()
        st.pyplot(plt)
    else:
        st.text("Tag not used.")


def plotTagHist(df,selected):
    tagTimestamps(df,selected)

def freq_nbPosts(df,tag):
    freq=0
    nbPosts=0
    minT = date.today()
    maxT =datetime.date(2019, 5, 17)
    for ind in df.index: 
        if(df['tags'][ind]):
            if(tag in str(df.iloc[ind][6])):
                nbPosts=nbPosts+1
                if(df.iloc[ind][7]<minT):
                    minT=df.iloc[ind][7]
                if(df.iloc[ind][7]>maxT):
                    maxT=df.iloc[ind][7]
    freq = abs(maxT - minT).total_seconds()/(nbPosts*60)
    return freq,nbPosts
