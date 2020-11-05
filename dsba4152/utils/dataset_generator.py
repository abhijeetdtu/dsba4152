import os
from multiprocessing import Pool
import argparse
import logging

import matplotlib.pyplot as plt

from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img

from dsba4152.utils.helpers import Helpers
from dsba4152.utils.config import Config

class DatasetGenerator:

    def __init__(self,num_per_img, source_path, dest_path , args):
        self.num_per_img = num_per_img
        self.source_path = source_path
        self.dest_path = dest_path
        self.args = args


    def pipe(self):
        pool = Pool(self.args.num_process)
        #print(os.listdir(self.source_path))
        imgs = [(os.path.abspath(os.path.join(self.source_path , f)) , f) for f in os.listdir(self.source_path)]
        pool.map(self.generate , imgs)

    def generate(self, img):

        path , name = img
        logging.info(f"--Processing {name}")

        image = plt.imread(path)
        datagen = ImageDataGenerator(rotation_range=40,horizontal_flip=True,fill_mode='nearest')

        x = img_to_array(image)
        x = x.reshape((1,) + x.shape)
        i = 0
        for batch in datagen.flow(x, batch_size=1,
                                  save_to_dir=self.dest_path, save_prefix=name, save_format='jpeg'):
            i += 1
            if i > self.num_per_img:
                break


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--num-per-img" , default=20 , type=int)
    parser.add_argument("--num-process" , default=3 , type=int)
    parser.add_argument("--source-path" , default=Config.country_img_dir )
    parser.add_argument("--dest-path" , default=os.path.abspath(os.path.join(Config.country_img_dir , "dataset" )))

    args = parser.parse_args()

    if not os.path.exists(args.dest_path):
        os.mkdir(args.dest_path)
        
    logging.basicConfig(level=logging.INFO)
    DatasetGenerator(args.num_per_img , args.source_path , args.dest_path, args).pipe()
