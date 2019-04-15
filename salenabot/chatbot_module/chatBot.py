
import re
import builtins
import cv2
from predictor import Predictor
from predict_beam import get_best_caption
import numpy as np

def callingUser(caption):
    pattern = "wearing .*"
    match = re.search(pattern, caption)
    Match=match.group(0)
    str = "hey what's up , you who are " + Match + " come and have fun with me. Hi my name is Salena \n How are you?"
    return str


# build dictionary holds all categories
category = {"child": [
    "your baby is so cute , Would you like to try something like this {}for him,I think it will make him happy"],
            "woman": [
                "you look very pretty, I think you will be prettier if you tried this {},Would you like to see it."],
            "man": ["you look so smart, I think {} will suits you, Woulg yoyu like to see it"],
            "old woman": [""],
            "old man": [""]}



def chatBot():
    image="COCO_test2014_000000000063.jpg"
    #caption = "a woman wearing red dress"  # call function model
    model_weights_path="modified logs2/nep031-acc0.681-val_acc0.650.h5"
    predictor = Predictor(model_weights_path, beam_size=3)
    caption = get_best_caption(predictor, image)
    #tag, link = getAdds(caption)
    tag = "shambo"
    cat_child = re.search("child", caption)
    cat_woman = re.search("woman", caption)
    cat_man = re.search("man", caption)
    cat_oldWoman = re.search("old woman", caption)
    cat_oldMen = re.search("old man", caption)
    key = ""

    if (cat_child != None):
        key = "child"
    elif (cat_woman != None):
        key = "woman"
    elif (cat_man != None):
        key = "man"
    elif (cat_oldWoman != None):
        key = "old woman"
    elif (cat_oldMen != None):
        key = "old man"
    description = callingUser(caption)
    BOT = category[key]
    BOT=BOT.__getitem__(0)
    BOT=BOT.format(tag)

    print(description)
    fine = builtins.input()
    print(BOT)
    return tag


def checkInput(input,tag):
    if input=="Yes":
        showAdd(tag)
    elif input=="No":
        request(tag)

def showAdd(tag):
    # show the add video
    addRating="How did you find this {}".format(tag)+"? \n Give me rating from 1 to 5: \n 1  2  3  4  5"
    print(addRating)
    #Rating input
    input=eval(builtins.input())

    f=open("save Adds Rating.txt","w")
    f.write(tag+": "+str(input))
    f.write('\n')
    f.close()
    request(tag)

def request(tag):
    # get name of another product by Rand except the prev add
    add = "Would you like to see another product"
    print(add)
    # take input [yes or No ]to see another add
    input=builtins.input(str())

    #input = "NO"
    if input=="No":
        Bye()
    else:
        showAdd(tag)

def Bye():
    print("Did you think i were helpful? \n Give me rating from 1 to 5: \n 1  2  3  4  5")
    SalenaRating=eval(builtins.input())
    f = open("Salena Rating.txt", "w")
    f.write(str(SalenaRating))
    f.write('\n')
    f.close()
    print("Thanks :), Nice to meet you ,I hope to see you soon Byeeee")


def showVideo():
    cap=cv2.VideoCapture('video.mp4')
    if(cap.isOpened()==False):
        print("video error")
    while(cap.isOpened()):
        ret,frame=cap.read()
        if ret==True:
            cv2.imshow('frame',frame)
            if cv2.waitkey(25)&0xFF==ord('q'):
                #press q to exit
                break
        else:
            break
    cap.release()
    cv2.destroyAllWindows()
    out=cv2.VideoWriter('outpy.avi',cv2.VideoWriter_fourcc('M','J','P','G'),(frame_width,frame_height))








tag=chatBot()
#take input[yes or NO] for seeing add
input=__builtin__.input(str())
#input="yes"
checkInput(input,tag)
