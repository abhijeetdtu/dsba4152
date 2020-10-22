import os
import pickle
import gzip
from collections import defaultdict
import logging
import re

import matplotlib.pyplot as plt
import fiona
import rasterio
import rasterio.mask

from dsba4152.utils.config import Config


class Helpers:

    def __init__(self):
        self.cache = {}

    def prepare_shape_reverse_index(self
    , path_to_shape_file=Config.shape_geopkg
    , countries_to_keep = Config.COUNTRIES_TO_KEEP
    , pickle_out = Config.reverse_index_out):
        inverted_index = defaultdict(list)
        #https://www.geonames.org/countries/

        print(path_to_shape_file)
        with fiona.open(path_to_shape_file) as layer:
            for feature in layer:
                gid = feature["properties"]["GID_0"]
                if gid in countries_to_keep:
                    inverted_index[gid].append(feature["geometry"])

        pickle.dump(inverted_index,  open(pickle_out , "wb"))
        return inverted_index

    def read_img_path(self, path):
        return rasterio.open(path)

    def _read_img(self,f , source_path , i=0):
        if len(f) == 0:
            logging.log(logging.ERROR , "No file exists for the year")
            return None

        f = f[i]
        fp = os.path.abspath(os.path.join( source_path , f))
        return rasterio.open(fp)

    def read_year_img(self, year , source_path = Config.img_dir):
        f = [f for f in os.listdir(source_path) if (f.find(str(year)) > -1) and (f.find(Config.v4composite_suffix) > -1)]
        return self._read_img(f, source_path)

    def read_country_all_years(self, country , source_path = Config.country_img_dir):
        f = [f for f in os.listdir(source_path) if (f.find(country) > -1)]
        years = [ re.findall("(\d{4})",fi)[0] for fi in f]
        return [self._read_img(f, source_path ,i) for i in range(len(f))] , years

    def read_country_year_img(self, country ,year, source_path = Config.country_img_dir):
        f = [f for f in os.listdir(source_path) if (f.find(str(year)) > -1) and (f.find(country) > -1)]
        return self._read_img(f, source_path)

    def show_img(self , imdata , figsize=(15,5)):
        fig, ax = plt.subplots(1,1,figsize=figsize)
        ax.imshow(imdata[0 , : , :], cmap='pink')

    def load_reverse_index(self,pickle_path = Config.reverse_index_out):

        if os.path.exists(pickle_path):
            return pickle.load(open(pickle_path , "rb"))
        else:
            logging.log(logging.WARNING , "Reverse Index Does Not Exist.Creating")
            return self.prepare_shape_reverse_index()

    def subset_country(self,composite_img, country_id ):
        from dsba4152.utils.sqlite_access import GeoPKG
        if country_id in self.cache:
            shape = self.cache[country_id]
        else:
            shape = GeoPKG().get_country_geom(country_id , composite_img.crs.data)
            self.cache[country_id] = shape
        #print(shape)
        out_image, out_transform = rasterio.mask.mask(composite_img, shape, crop=True)
        return out_image
