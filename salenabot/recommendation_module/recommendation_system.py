import json
from difflib import SequenceMatcher


def get_advertisement(caption):
    file_path = "../recommendation_module/videos_infos.json"
    new_ration = 0
    old_ratio = 0
    title = " "
    link = " "
    with open(file_path) as json_data:
        properties = json.load(json_data)
        for record in properties["Info"]:
            tags = record['tags']
            new_ration = SequenceMatcher(None, caption, tags).ratio()
            if new_ration > old_ratio:
                old_ratio = new_ration
                title = record['title']
                link = record['url']
        if new_ration == 0:
            title = "default advertisement"
            link = "https://www.youtube.com/watch?v=PZguUhAB_hI"

    return title, link


