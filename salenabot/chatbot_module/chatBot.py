import re
import builtins
import cv2
# from salenabot.chatbot_module.predictor import Predictor
# from salenabot.chatbot_module.predict_beam import get_best_caption
from SALENA.salenabot.recommendation_module.recommendation_system import get_advertisement
from colour import Color
import json
import numpy as np

def is_color(color):
    try:
        Color(color)
        return True
    except:
        return False
def calling_user(image):

    #image = "COCO_test2014_000000000063.jpg"  # TODO: get image using API
    model_weights_path = "modified logs2/nep031-acc0.681-val_acc0.650.h5"
    # predictor = Predictor(model_weights_path, beam_size=3)  # TODO: call the model
    # caption = get_best_caption(predictor, image)
    caption = "a girl is wearing a sky blue skirt wow"
    words = caption.split(' ')
    for word in words:

        value = is_color(word)
        if value == True:
            combo = words[words.index(word) - 1] + " " + word
            value = is_color(combo.replace(" ", ""))
            if value == True:
                wearing = str(combo) + " " + words[words.index(word) + 1]
            else:
               wearing=word+ " " + words[words.index(word) + 1]

        else:
            continue
    text = "hey what's up , you who are wearing " + wearing + " come and have fun with me. Hi my name is Salena \n How are you?"
    print(text)
    file = {"calling_caption":text}
    json_file=json.dumps(file)
    return json_file


# build dictionary holds all categories
category = {"child": [
    "your baby is so cute , Would you like to try something like this {} for him? I think it will make him happy"],
    "woman": [
        "you look very pretty, I think you will be prettier if you tried this {},Would you like to see it?"],
    "man": ["you look so smart, I think {} will suits you, Would you like to see it"],
    "old woman": ["Wow, How can you look so young, i think you might find this {} very useful to you, Would you like to see it ?"],
    "old man": [""]
}
varity_words = {"woman":["lady", "girl","woman"], "man":["youth","man"],"old woman":["old woman"],"old man":["old woman"],
                "child":["child","baby","boy"]}


def chat_bot(image):
    #image = "COCO_test2014_000000000063.jpg"  # TODO: get image using API
    model_weights_path = "modified logs2/nep031-acc0.681-val_acc0.650.h5"
    # predictor = Predictor(model_weights_path, beam_size=3)  # TODO: call the model
    # caption = get_best_caption(predictor, image)
    caption = "a girl is wearing a sky blue skirt wow"
    tag, link = get_advertisement(caption)
    flag = False
    key = ""
    for k, v in varity_words.items():
        i = 0
        while i < len(v):
            if (re.search(v[i], caption) != None):
                # print(v[i])
                flag = True
                key = k
                break
            else:
                i += 1
        if (flag == True):
            break
    #cat_child = re.search("child", caption)
    #cat_woman = re.search("woman", caption)
    #cat_man = re.search("man", caption)
    #cat_old_woman = re.search("old woman", caption)
    #cat_old_men = re.search("old man", caption)
    #key = ""

    #if cat_child is not None:
     #   key = "child"
    #elif cat_woman is not None:
    #    key = "woman"
    #elif cat_man is not None:
    #    key = "man"
    #elif cat_old_woman is not None:
    #    key = "old woman"
    #elif cat_old_men is not None:
    #    key = "old man"
    description = calling_user(caption)
    BOT = category[key]
    BOT = BOT.__getitem__(0)
    BOT = BOT.format(tag)

    #print(description)
    fine = builtins.input()
    print(BOT)
    file2={"recommend_caption": BOT, "link":link, "tag":tag}
    json_file2=json.dumps(file2)
    return tag,BOT,link


def check_input(input, tag):
    if input == "Yes" or input == "yes":
        show_advertisement(tag)
    elif input == "No" or input == "no":
        request_another_ad(tag)


def show_advertisement(tag):
    # show the add video
    show_video()
    ad_rating = "How did you find this {}".format(tag) + "? \n Give it rating from 1 to 5: \n 1  2  3  4  5"
    print(ad_rating)
    # Rating input
    input = eval(builtins.input())

    f = open("save Ads Rating.txt", "w")
    f.write(tag + ": " + str(input))
    f.write('\n')
    f.close()
    request_another_ad(tag)


def request_another_ad(tag):
    # get name of another product by Rand except the prev add
    ad = "Would you like to see another product"
    print(ad)
    input = builtins.input(str())
    if input == "No" or input == "no":
        Bye()
    else:
        show_advertisement(tag)


def Bye():
    print("Did you think i were helpful? \nRate me: \n1  2  3  4  5")
    salena_rating = eval(builtins.input())
    f = open("Salena Rating.txt", "w")
    f.write(str(salena_rating))
    f.write('\n')
    f.close()
    if salena_rating < 3:
        print("I hope you like me next time :), byee.")
    else:
        print("Thanks :), Nice to meet you ,I hope to see you soon Byeeee")


def show_video():
    cap = cv2.VideoCapture('video.mp4')
    if (cap.isOpened() == False):
        print("video error")
    while (cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:
            cv2.imshow('frame', frame)
            if cv2.waitkey(25) & 0xFF == ord('q'):
                # press q to exit
                break
        else:
            break
    cap.release()
    cv2.destroyAllWindows()
    out = cv2.VideoWriter('outpy.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), (640, 480))#(frame_width, frame_height)

image = "COCO_test2014_000000000063.jpg"  # TODO: get image using API
tag = chat_bot(image)
# take input[yes or NO] for seeing add
input = str(input())
# input="yes"
check_input(input, tag)