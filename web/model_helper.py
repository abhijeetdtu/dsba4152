import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Model

import pathlib
import os
import matplotlib.pyplot as plt
import numpy as np


path_to_img = "C:\\Users\\Abhijeet\\Documents\\GitHub\\dsba4152\\web\\image.png"

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class ModelHelper(metaclass=Singleton):

    def __init__(self, path_to_model):
        self.model = keras.models.load_model(path_to_model)
        self.feature_model_1 = Model(inputs=self.model.input[1], outputs=self.model.layers[1].output)
        self.feature_model_8 = Model(inputs=self.model.input[1], outputs=self.model.layers[8].output)

    def _model_predict(self,tensor_img ,model , id , same_scale):
        feature_maps = model.predict(tensor_img)
        n_filters = 8
        fig , axs = plt.subplots(2,4, figsize=(15,8))

        vmin = np.min(feature_maps[0 , : , : , :n_filters ])
        vmax = np.max(feature_maps[0 , : , : , :n_filters ])

        for i in range(n_filters):
          # get the filter
            f = feature_maps[0, :, :, i]
            ax = axs[int(i/4)][i%4]
            # plot filter channel in grayscale
            if same_scale:
                ax.imshow(f, cmap='gray' ,   vmin=vmin, vmax=vmax)
            else:
                ax.imshow(f, cmap='gray')

        out_path = pathlib.Path(".").absolute()
        out_path = os.path.abspath(os.path.join(out_path , "static" , "out_img" , f"output_{id}.png"))
        plt.savefig(out_path ,bbox_inches='tight',  pad_inches=0)

    def predict(self , same_scale):
        img = plt.imread(path_to_img )
        tensor_img = tf.convert_to_tensor(img[:,:,0].reshape((1,256,256)))
        self._model_predict(tensor_img , self.feature_model_1 , "1" , same_scale)
        self._model_predict(tensor_img , self.feature_model_8 , "8" , same_scale)
