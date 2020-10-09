from sklearn.feature_extraction.text import TfidfVectorizer

#https://github.com/smyachenkov/k-means_tags_demo/blob/master/kmeans_tags.py

def findGoodTag(tagSeries):
    cleanSeries = filter(None, list(tagSeries))
    numberOfUniqueTags = 100
    vectorizer = TfidfVectorizer()
    posts_coordinates = vectorizer.fit_transform(cleanSeries)

    return type(tagSeries)
