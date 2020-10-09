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
       
def main():
    local_css ('style.css')
    df=loadData()
    # top_tags=get_top_tags(df)
    # st.title('Seasonal hotspots')
    # st.subheader("Top 1000 Tags used in Helsinki ")
    # wordcloud = plotWordCloud(top_tags)
    # plt.imshow(wordcloud, interpolation='bilinear')
    # plt.axis("off")
    # st.pyplot(plt)
    # st.subheader("Seasonaly centers of interest ")
    # plotTagHist(df)
    # st.subheader("Trends")
    # st.subheader("Locations")
    
    st.subheader("Time series")
    ts = to_ts(df)
    ts2 = agg_ts(ts)
    st.text(ts2.columns)
    fig = fcast(ts2)
    st.pyplot(fig)

if __name__ == "__main__":
    main()





