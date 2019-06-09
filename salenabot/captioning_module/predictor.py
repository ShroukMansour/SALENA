from keras.engine.saving import load_model, model_from_json
import numpy as np
from keras.backend import expand_dims

from salenabot.captioning_module.im2txt_model import create_prediction_cnn, create_prediction_lstm, \
    create_training_model

from keras_applications.nasnet import preprocess_input
from PIL import Image


def preprocess_image(image, input_shape, proc_img):
    iw, ih = image.size
    h, w = input_shape

    # resize image
    scale = min(w / iw, h / ih)
    nw = int(iw * scale)
    nh = int(ih * scale)
    dx = (w - nw) // 2
    dy = (h - nh) // 2
    image_data = 0
    if proc_img:
        image = image.resize((nw, nh), Image.BICUBIC)
        new_image = Image.new('RGB', (w, h), (128, 128, 128))
        new_image.paste(image, (dx, dy))
        image_data = np.array(new_image)
        image_data = preprocess_input(image_data)
    return image_data


class Predictor:
    def __init__(self, trained_model_weights=None, method='json', beam_size=3):
        self.beam_size = beam_size
        trained_model = self.get_model(trained_model_weights, method)
        self._init_image_model(trained_model)
        self._init_caption_model(trained_model)
        del trained_model
        self.features = None

    def get_model(self, weights_only_path=None, method='json'):
        model = None
        if method == 'json':
            json_file = open('E:/SALENA/SALENA/salenabot/captioning_module/obj/model_structure.json', 'r')
            loaded_model_json = json_file.read()
            json_file.close()
            model = model_from_json(loaded_model_json, custom_objects={"expand_dims": expand_dims})
            model.load_weights(weights_only_path)
        elif method == 'create':
            model = create_training_model()
            model.load_weights(weights_only_path)
        elif method == 'load':
            model = load_model('obj/final_model.h5', custom_objects={"expand_dims": expand_dims})
        return model

    def _init_image_model(self, trained_model=None, method='create'):
        if method == 'create':
            self.image_model = create_prediction_cnn(weighted_model=trained_model)
        elif method == 'load':
            self.image_model = load_model('obj/cnn_model.h5', custom_objects={"expand_dims": expand_dims})

    def _init_caption_model(self, trained_model, method="create"):
        if method == 'create':
            self.caption_model = create_prediction_lstm(weighted_model=trained_model, batch_size=self.beam_size)
        else:
            self.caption_model = load_model('obj/lstm_model.h5', custom_objects={"expand_dims": expand_dims})

    def feed_image(self, image):
        self.image_model.reset_states()
        image_size = (224, 224)
        image = np.expand_dims(preprocess_image(image, image_size, proc_img=True), axis=0)
        state_h, state_c = self.image_model.predict([image])
        return [state_h[0, :], state_c[0, :]]

    def predict(self, sequence, states=None):
        outputs, state_h, state_c = self.caption_model.predict([sequence, states[0], states[1]])
        return outputs, [state_h, state_c]
