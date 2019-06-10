from __future__ import division
import json

tokenize = lambda doc: doc.lower().split(" ")
def jaccard_similarity(query, document):
    intersection = set(query).intersection(set(document))
    union = set(query).union(set(document))
    return len(intersection) / len(union)


def get_advertisement(caption):
    file_path = "salenabot/recommendation_module/videos_infos.json"
    index=-1
    maxValue=0.0
    all_titles =[]
    all_links =[]
    all_documents=[]
    title=" "
    link=" "
    with open(file_path) as json_data:
        properties = json.load(json_data)
        for record in properties["Info"]:
          txt=record['description']
          all_titles+=[record['title']]
          all_links+=[record['url']]
          all_documents += [txt]
          tokenized_documents = [tokenize(d) for d in all_documents]  # tokenized docs
        caption_tokenized=tokenize(caption)
        for i in tokenized_documents:
            index+=1
            if(jaccard_similarity(i,caption_tokenized)>maxValue):
                print("here")
                maxValue=jaccard_similarity(i,caption_tokenized)
                title = all_titles[index]
                link =all_links[index]
        if maxValue == 0.0:
            title = "default advertisement"
            link = "https://www.youtube.com/watch?v=PZguUhAB_hI"

    return title, link



#title,link=get_advertisement("skin")
#print(title)
#print(link)

