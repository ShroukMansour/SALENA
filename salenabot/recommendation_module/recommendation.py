import json
from sklearn.feature_extraction.text import TfidfVectorizer
import math

tokenize = lambda doc: doc.lower().split(" ")
def cosine_similarity(v1,v2):
    "compute cosine similarity of v1 to v2: (v1 dot v2)/{||v1||*||v2||)"
    sumxx, sumxy, sumyy = 0, 0, 0
    for i in range(len(v1)):
        x = v1[i]
        y = v2[i]
        sumxx += x*x
        sumyy += y*y
        sumxy += x*y
    return sumxy/math.sqrt(sumxx*sumyy)
# in Scikit-Learn
def get_advertisement(caption):
    file_path = "E:/FCI/GP/recommendation_system/videos_infos.json"
    index = -1
    maxValue = 0.0
    all_durations= []
    all_titles= []
    all_links= []
    all_videos_discriptions = []
    with open(file_path) as json_data:
        properties = json.load(json_data)
        for record in properties["Info"]:
            all_durations+= [record['duration']]
            all_titles += [record['title']]
            all_links += [record['url']]
            all_videos_discriptions += [record['description']]

    all_videos_discriptions+=[caption]
    sklearn_tfidf = TfidfVectorizer(min_df=0, use_idf=True, smooth_idf=False, sublinear_tf=True,tokenizer=tokenize)
    sklearn_representation = sklearn_tfidf.fit_transform(all_videos_discriptions)
    captionIndex=len(sklearn_representation.toarray())-1
    for i in range(len(sklearn_representation.toarray())-1):
        index+=1
        similarity = cosine_similarity(sklearn_representation.toarray()[i],sklearn_representation.toarray()[captionIndex])
        if(similarity>maxValue):
            print("here")
            maxValue=similarity
            title = all_titles[index]
            link =all_links[index]
            duration=all_durations[index]
    if maxValue == 0.0:
        title = "default advertisement"
        link = "https://www.youtube.com/watch?v=PZguUhAB_hI"
        duration="2:09"

    return title, link,duration
