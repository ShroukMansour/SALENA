
from salenabot.captioning_module.crop_model import YOLO
from salenabot.captioning_module.predictor import Predictor

def load_scene_model():
    global predictor
    model_weights_path = "salenabot/captioning_module/obj/scene_model.h5"
    predictor = Predictor(model_weights_path, beam_size=3)


def load_crop_model():
    global yolo
    yolo = YOLO(model_path="salenabot/captioning_module/obj/yolo_model.h5")

