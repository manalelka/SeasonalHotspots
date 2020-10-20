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
from educatedTag import *
from fbprophet import Prophet

def main():
    local_css ('style.css')

    Title_html = """
        <style>
            .title {
                background-image: url("https://live.staticflickr.com/4441/36144860233_be0fbab4de_b.jpg");
                background-repeat: cover;
                border-radius: 1rem;

            }
            .title h1{
              user-select: none;
              font-size: 7rem;

            }
        </style>
        <div>
            <div class="title">
                <h1>Insights of Helsinki</h1>
            </div>
             <h3>Top 1000 Tags In The Area<h3>
        </div>
        """
    st.markdown(Title_html, unsafe_allow_html=True)

    ##Loading the data:
    df=loadData()
    tags_count=get_top_tags(df)
    tag_clusters = find_clusters(df['tags'])
    #Tags
    #wordcloud = plotWordCloud(tags_count)
    wordcloud = WordCloud(height=300, width=300, margin=1, random_state=1, background_color='white', colormap='rainbow', collocations=False).generate(tags_count)
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
        freq , nb =freq_nbPosts(df,selected)
        rank = getRankTag(selected,tags_count)
        st.markdown("<div class='card'> <div class='container'><div> <b>Number of posts:</b> </div><div>"+str(nb)+"</div></div></div><div class='card'> <div class='container'><div><b> Posting frequency:</b></div><div>"+str(int(freq))+" minutes </div></div></div><div class='card'><div class='container'><div><b> Tag Rank: </b></div><div>"+rank+"</div></div></div>", unsafe_allow_html=True)
    
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

    st.subheader('Tag clusters')
    st.text('Cluster groups below are built automatically using machine learning. You probably notice\nsome common theme inside the clusters. If you find relevant theme for you business, try\nusing combination of three tags in that cluster in you next social media post! Good luck!')

    i = 0
    for cluster in tag_clusters:
        st.markdown(f"CLUSTER {i + 1}.")
        st.write(pd.DataFrame({
            'Tag': tag_clusters[i][0],
            'Popular': tag_clusters[i][1],
            'Frequency': tag_clusters[i][2],
        }))
        i += 1


if __name__ == "__main__":
    main()





