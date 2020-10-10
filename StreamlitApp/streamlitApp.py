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
from tagAnalysis import *
from timeseries import *
from perfectTag import findGoodTag
from fbprophet import Prophet

def main():
    local_css ('style.css')
    ##Loading the data:
    df=loadData()
    top_tags=get_top_tags(df)
    st.title('Seasonal hotspots')
    #Tags
    st.subheader("Top 1000 Tags used in Helsinki ")
    wordcloud = plotWordCloud(top_tags)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    st.pyplot(plt)

    # overall time series trend and weekday decomposition on daily aggregated helsinki posting data
    ts = to_ts(df)
    ts = agg_ts(ts, '24H') # add radio buttons for aggregation in the final step (hourly, daily, weekly...)
    forecast, components = fcast(ts, 7, 'D') # in a similar manner add a forecasting frequency that matches the data aggregation

    st.pyplot(forecast)
    if st.checkbox('Decompose'):
        st.pyplot(components)
    
    st.subheader("Seasonaly centers of interest ")
    selected = st.text_input("", "Search...")
    if (selected != "Search..."):
        plotTagHist(df,selected)
        # nb, freq =nbPosts_freq(selected)
        # st.markdown("<div class='container-div'> <div> Number of posts: "+nb+"</div> <div> Posting frequency: "+freq+"</div></div>", unsafe_allow_html=True)
    # st.subheader("Trends")
    # st.subheader("Locations")
    # st.subheader("Good Tag")
    # gt = findGoodTag(df['tags'])
    # st.write(gt)

    st.subheader("Tag prediction")
    if (selected != "Search..."):
        df[selected] = df["tags"].apply(lambda x: 1 if selected in x else 0)
        ts = to_ts(df)
        ts = agg_ts(ts, '24H', selected)
        forecast, components = fcast(ts, 7, 'D')
        st.pyplot(forecast)
        if st.checkbox('Decompose tag'):
            st.pyplot(components)


if __name__ == "__main__":
    main()





