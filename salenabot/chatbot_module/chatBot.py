import re
from salenabot.captioning_module.scene_model import get_scene_caption
from salenabot.recommendation_module.recommendation import get_advertisement

# build dictionary holds all categories
category = {"child": [
    "your baby is so cute , Would you like to try something like this {} for him? I think it will make him happy"],
    "woman": [
        "you look very pretty, I think you will be prettier if you tried this {},Would you like to see it?"],
    "man": ["you look so smart, I think {} will suits you, Would you like to see it"],
    "old woman": [
        "Wow, How can you look so young, i think you might find this {} very useful to you, Would you like to see it ?"],
    "old man": ["you look so handsome, i think you might find this {} very useful to you, Would you like to see it ?"],
    "person": ["i think you might find this {} very useful to you, Would you like to see it ?"]
}
varity_words = {"woman": ["lady", "girl", "woman"], "man": ["youth", "man"], "old woman": ["old woman"],
                "old man": ["old woman"],
                "child": ["child", "baby", "boy"]}


def get_key(caption):
    key = ""
    flag = False
    for k, v in varity_words.items():
        i = 0
        while i < len(v):
            if re.search(v[i], caption) is not None:
                flag = True
                key = k
                break
            else:
                i += 1
        if flag:
            break
    return key


def get_calling_caption(image):
    caption = get_scene_caption(image)
    print(caption)
    # caption = "a girl walk a dog"
    if caption is not None:
        pattern = "with .*"
        match = re.search(pattern, caption)
        if match is not None:
            match = match.group(0)
            calling_user_caption = "hey what's up , you who are " + match + "come and talk with me."
        else:
            verb_match = re.search(r"\b(\w+ing)\b", caption)
            if verb_match is None:
                calling_user_caption = "hey {} ,come and talk with me."
                key = get_key(caption)
                calling_user_caption = calling_user_caption.format(key)
                calling_user_caption=re.sub("his","your",calling_user_caption)
                calling_user_caption = re.sub("her", "your", calling_user_caption)
                calling_user_caption = re.sub("mirror", "camera", calling_user_caption)
                return calling_user_caption
            verb = verb_match.group(0)
            pattern = str(verb) + ".*"
            verb_calling = re.search(pattern, caption)
            verb_calling = verb_calling.group(0)
            calling_user_caption = "hey what's up , you who are " + verb_calling + "come and talk with me."
            calling_user_caption = re.sub("his", "your", calling_user_caption)
            calling_user_caption = re.sub("her", "your", calling_user_caption)
            calling_user_caption = re.sub("mirror", "camera", calling_user_caption)
        return calling_user_caption
    else:
        return "none"


def get_recommendation_data(img_path):
    caption = get_scene_caption(img_path)
    if caption is not None:
        tag, link,duration = get_advertisement(caption)
        key = get_key(caption)
        if key == "":
            key = "person"
        recommendation_caption = category[key]
        recommendation_caption = recommendation_caption.__getitem__(0)
        recommendation_caption = recommendation_caption.format(tag)
        return recommendation_caption, link,tag,duration
    else:
        return None, None, None,None

# image = "COCO_test2014_000000000063.jpg"  # TODO: get image using API
# tag,BOT,link = get_recommendation_data(image)
# # take input[yes or NO] for seeing add
# input = str(input())
# # input="yes"
# check_input(input, tag,link)
