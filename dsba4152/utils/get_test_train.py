import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
import cv2

from PIL import Image

Image.MAX_IMAGE_PIXELS = None

class GetTestTrain:

    def __init__(self, root_path ,gdp_csv_path, selector=None ,resize = False ,resize_shape=(128,128)):

        self.root_path = root_path
        self.gdp_csv_path = gdp_csv_path
        self.selector = selector
        self.resize_shape = resize_shape
        self.resize =resize


    def get_img_paths(self):
        mex_impaths = [f for f in os.listdir(self.root_path) if  ((self.selector is None ) or ((self.selector is not None ) and (f.find(self.selector) > -1)))]
        data = []
        for m in mex_impaths:
            country , year  = m.split(".")[0].split("_")
            data.append((country,year,m))

        img_df = pd.DataFrame(data , columns=["code" , "year" , "path"])
        img_df["year"] = img_df["year"].astype(int)
        #img_df.head()
        return img_df

    def get_gdp_data(self):
        gdp = pd.read_csv(self.gdp_csv_path)
        gdp["year"] = gdp["year"].astype(int)
        return gdp



    def get_train_test_split_data(self , img_path_df , gdp_df):
        merged_df = pd.merge(img_path_df, gdp_df , on=["code" , "year"])
        imgs = merged_df.apply(lambda row  : plt.imread(self.root_path + row["path"]),axis=1)
        y = merged_df["gdp"].values
        return train_test_split(imgs , y , stratify=merged_df["year"])

    def train_test_split(self):
        img_path_df = self.get_img_paths()
        gdp = self.get_gdp_data()
        return self.get_train_test_split_data(img_path_df  , gdp)

    def get_all_data(self):
        img_path_df = self.get_img_paths()
        gdp = self.get_gdp_data()
        merged_df = pd.merge(img_path_df, gdp , on=["code" , "year"])
        #imgs = merged_df.apply(lambda row  : plt.imread(self.root_path + row["path"]),axis=1)
        imgs = []
        for name,row in merged_df.iterrows():
            #print(name,row) # memory explosion when using df.apply
            im = plt.imread(self.root_path + row["path"])
            if self.resize:
                im = cv2.resize(im , self.resize_shape , cv2.INTER_CUBIC)
            imgs.append(im)
            #imgs = imgs.apply(lambda im :)
        y = merged_df["gdp"]
        years = merged_df["year"].values
        code = merged_df["code"]
        return np.array(imgs) , y, years , code
