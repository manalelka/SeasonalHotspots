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
    tags_count=get_top_tags(df)
    st.title('Seasonal hotspots')
    #Tags
    st.subheader("Top 1000 Tags used in Helsinki ")
    wordcloud = plotWordCloud(tags_count)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    st.pyplot(plt)

    # overall time series trend and weekday decomposition on daily aggregated helsinki posting data
    st.subheader("Overall posting activity within provided timeline")
    ts1 = to_ts(df)
    ts1 = agg_ts(ts1, '24H') # add radio buttons for aggregation in the final step (hourly, daily, weekly...)
    m1, fcst1 = fcast(ts1, 1, 'D') # in a similar manner add a forecasting frequency that matches the data aggregation
    forecast1 = m1.plot(fcst1)
    axes11 = forecast1.get_axes()
    axes11[0].set_xlabel('Date')
    axes11[0].set_ylabel('Count')
    components1 = m1.plot_components(fcst1)
    axes12 = components1.get_axes()
    axes12[0].set_xlabel('Date')
    axes12[0].set_ylabel('Count')
    axes12[1].set_ylabel('Count')
    
    st.pyplot(forecast1)
    if st.checkbox('Decompose'):
        st.subheader("Overall posting activity by trend and weekday components")
        st.pyplot(components1)
    
    st.subheader("Seasonaly centers of interest ")
    selected = st.text_input("", "Search...")
    if (selected != "Search..."):
        plotTagHist(df,selected)
        nb, freq =nbPosts_freq(selected)
        rank = getRankTag(selected,tags_count)
        st.markdown("<div class='container-div'> <div> Number of posts: "+nb+"</div> <div> Posting frequency: "+freq+"</div><div> Tag Rank : "+rank+"</div></div>", unsafe_allow_html=True)
    
    # st.subheader("Good Tag")
    # gt = findGoodTag(df['tags'])
    # st.write(gt)

    
    if (selected != "Search..."):
        st.subheader("Tag time series")
        df2 = df
        df2[selected] = df2["tags"].apply(lambda x: 1 if selected in x else 0)
        ts2 = to_ts(df2)
        ts2 = agg_ts(ts2, '24H', selected)
        m2, fcst2 = fcast(ts2, 7, 'D')
        forecast2 = m2.plot(fcst2)
        axes21 = forecast2.get_axes()
        axes21[0].set_xlabel('Date')
        axes21[0].set_ylabel('Count')

        components2 = m2.plot_components(fcst2)
        axes22 = components2.get_axes()
        axes22[0].set_xlabel('Date')
        axes22[0].set_ylabel('Count')
        axes22[1].set_ylabel('Count')
        st.pyplot(forecast2)
        st.pyplot(components2)


if __name__ == "__main__":
    main()





