from salenabot.captioning_module.predictor import Predictor

#predictor=None
def load_model():

    global predictor
    model_weights_path = "obj/scene_model.h5"
    predictor = Predictor(model_weights_path, beam_size=3)
