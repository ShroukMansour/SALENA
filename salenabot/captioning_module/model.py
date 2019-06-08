from PIL import Image

from salenabot.captioning_module.predict_beam import get_best_caption
from salenabot.captioning_module.predictor import Predictor
import os
import salenabot.captioning_module.model_loader as loader
def get_scene_caption(image):
    """
    :type image: PIL Image object
    """
    caption = get_best_caption(loader.predictor, image)
    return caption


img = Image.open("../chatbot_module/COCO_test2014_000000000063.jpg")
print(get_scene_caption(img))