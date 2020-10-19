from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from collections import Counter
import streamlit as st

@st.cache
def find_clusters(tag_series):
    #Hyperparameters
    clusters = 10
    top_limit = 10
    max_iter = 100
    n_init = 5

    #Series to list
    posts = []
    for index, tag_list in tag_series.items():
        if len(tag_list) > 0:
            posts.append(" ".join(tag_list))

    #Most common
    most_common = Counter(" ".join(posts).split()).most_common(100)
    dict_common = dict(most_common)

    #Vectorizing
    vectorizer = TfidfVectorizer()
    posts_matrix = vectorizer.fit_transform(posts)

    #Build a model
    model = KMeans(
        n_clusters=clusters,
        init='k-means++',
        max_iter=max_iter,
        n_init=n_init,
    )

    #Find clusters
    post_clusters = model.fit_predict(posts_matrix)
    #Sorting
    ordered_centers = model.cluster_centers_.argsort()[:, ::-1]
    tags = vectorizer.get_feature_names()

    #Building result
    result_clusters = []
    for idx, cluster in enumerate(ordered_centers):
        tags_list = []
        top100_list = []
        freq_list = []
        for tag_in_cluster in cluster[:top_limit]:
            tg = tags[tag_in_cluster]
            if tags[tag_in_cluster] in dict_common.keys():
                tags_list.append(tags[tag_in_cluster])
                top100_list.append('Yes')
                freq_list.append(dict_common[tags[tag_in_cluster]])
            else:
                tags_list.append(tags[tag_in_cluster])
                top100_list.append('No')
                freq_list.append('Low')
        result_clusters.append([tags_list, top100_list, freq_list])

    return result_clusters
