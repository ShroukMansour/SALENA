import base64
import re

from PIL import Image
from django import template
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
# Create your views here.
from salenabot.captioning_module.scene_model import get_scene_caption
from salenabot.chatbot_module.chatBot import get_calling_caption
from salenabot.chatbot_module.chatBot import get_recommendation_data


def index(request):
    return render(request, 'salenabot/index.html')



def wrtie_captured_img(request):
    if request.method == 'POST':
        if 'imgBase64' in request.POST:
            img64 = request.POST['imgBase64']
            imgstr = re.search(r'base64,(.*)', img64).group(1)
            img_path = 'salenabot/static/images/captured_img.jpg'
            output = open(img_path, 'wb')
            output.write(base64.b64decode(imgstr))
            output.close()
        return JsonResponse({"response": "ok"})


def get_calling_user_caption(request):
    data = {"calling_caption", "Hi, how are you"}
    if request.method == 'POST':
        img_path = 'salenabot/static/images/captured_img.jpg'
        calling_caption = get_calling_caption(img_path)
        data = {'calling_caption': calling_caption}
    return JsonResponse(data)


def get_recommended_product_data(request):
    data = {"recommendation_caption": "Do you want to see my recommended product for you", "video_link": 'https://www.youtube.com/watch?v=DDljNWP6b8E', "video_tag": 'This is Egypt'}
    if request.method == 'POST':
        img_path = 'salenabot/static/images/captured_img.jpg'
        recommendation_caption, link, tag = get_recommendation_data(img_path)
        if recommendation_caption is not None:
            data = {"recommendation_caption": recommendation_caption, "video_link": link, "video_tag": tag}
    return JsonResponse(data)


