from PIL import Image
from tensorflow import Graph, Session

from salenabot.captioning_module.predict_beam import get_best_caption
from salenabot.captioning_module.predictor import Predictor
import os
import salenabot.captioning_module.model_loader as loader
from keras import backend as K

def load_models():
    global scene_graph
    scene_graph = Graph()
    with scene_graph.as_default():
        global scene_session
        scene_session = Session()
        with scene_session.as_default():
            loader.load_scene_model()

    global yolo_graph
    yolo_graph = Graph()
    with yolo_graph.as_default():
        global yolo_session
        yolo_session = Session()
        with yolo_session.as_default():
            loader.load_crop_model()

def get_scene_caption(image_path):
    """
    :type image: PIL Image object
    """
    image = Image.open(image_path)
    K.set_session(yolo_session)
    with yolo_graph.as_default():
        person = loader.yolo.crop_person(image)

    if person is not None:
        # person.show()
        K.set_session(scene_session)
        with scene_graph.as_default():
            caption = get_best_caption(loader.predictor, person)
    else:
        caption = None
    return caption


