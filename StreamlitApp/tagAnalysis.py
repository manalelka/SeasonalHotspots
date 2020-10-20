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


def nbPosts_freq(tag):
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--headless')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
    tag_df  = pd.DataFrame(columns = ['Hashtag', 'Number of Posts', 'Posting Freq (mins)'])
    driver.get('https://www.instagram.com/explore/tags/'+str(tag))
    soup = BeautifulSoup(driver.page_source,"lxml")
    # Extract current hashtag name
    tagname = tag
    # Extract total number of posts in this hashtag
    # NOTE: Class name may change in the website code
    # Get the latest class name by inspecting web code
    #nposts = "0"
    #pfreq = "no-time"
    if(soup.find('span', {'class': 'g47SY'})):
        nposts = soup.find('span', {'class': 'g47SY'}).text
        # Extract all post links from 'explore tags' page
        # Needed to extract post frequency of recent posts
        myli = []
        for a in soup.find_all('a', href=True):
            myli.append(a['href'])
        # Keep link of only 1st and 9th most recent post
        newmyli = [x for x in myli if x.startswith('/p/')]
        newmyli =[newmyli[-1], newmyli[0]]
        timediff = []
        # Extract the posting time of 1st and 9th most recent post for a tag
        for j in range(len(newmyli)):
            driver.get('https://www.instagram.com'+str(newmyli[j]))
            soup = BeautifulSoup(driver.page_source,"lxml")
            for i in soup.findAll('time'):
                if i.has_attr('datetime'):
                    timediff.append(i['datetime'])
                    #print(i['datetime'])

        # Calculate time difference between posts
        # For obtaining posting frequency
        datetimeFormat = '%Y-%m-%dT%H:%M:%S.%fZ'
        diff = dt.datetime.strptime(timediff[0], datetimeFormat)- dt.datetime.strptime(timediff[1], datetimeFormat)
        #print(dt.datetime.strptime(timediff[0], datetimeFormat),dt.datetime.strptime(timediff[1], datetimeFormat))
        pfreq= int(diff.total_seconds()/(9*60))
        if(pfreq==0):
            pfreq="Very high (less than 1 min)"
        print(pfreq)
        # Add hashtag info to dataframe
        tag_df.loc[len(tag_df)] = [tagname, nposts, pfreq]
    driver.quit()
    time.sleep(3)
    return  nposts, pfreq
