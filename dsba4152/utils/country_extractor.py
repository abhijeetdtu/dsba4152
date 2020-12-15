# %load_ext autoreload
# %autoreload 2

import shutil
import os
import tarfile
import pathlib
import time
from multiprocessing import Pool
import argparse
import subprocess
import png
import re

from dsba4152.utils.helpers import Helpers
from dsba4152.utils.config import Config


REVERSE_INDEX  = None

class CountryExtractor:

    def __init__(self,helper , source_path , dest_path , countries ,re, args=None):
        self.helper = helper
        self.source_path = source_path
        self.dest_path = dest_path
        self.countries = countries
        self.re = re
        self.args = args

    def _work(self , f):

        consider = True if self.re is None else f.find(self.re) > -1
        if consider:
            print(f"Processing {f}")
            fp = pathlib.Path(self.source_path , f).absolute()
            #tarpath= f.replace(".tar.gz" , ".log")
            year = re.findall("F\d{2}(\d{4}).v" , f)[0]
            image = self.helper.read_img_path(fp)

            print(f"-- Extraction Started")

            for country in self.countries:
                op = pathlib.Path(self.dest_path , f"{country}_{year}.png").absolute()
                if not os.path.exists(op):
                    print(f"--- Country - {country}")
                    try:
                        subimg = self.helper.subset_region(image , country)
                        print(subimg.shape)
                        png.from_array(subimg[0,:,:], 'L').save(op)
                    except Exception as e:
                        print(e)
                        print(f"Failed - {op}")
            #shutil.copyfile(pathlib.Path(expath , f).absolute() , pathlib.Path(expath , f).absolute())
            print(f"-- Extraction done")


    def Extract(self ):
        nsize = 3
        pool = Pool(nsize)
        re = self.re if self.re is not None else ''
        allfiles = [f for f in  os.listdir(self.source_path) if (f.find(re) > -1)]

        if self.args.endidx == -1:
            self.args.endidx = len(allfiles)
        if self.args.startidx < 0:
            self.arg.startidx =  len(allfiles) + self.args.startidx #-1

        batches = [allfiles[(self.args.startidx + i*nsize ): min(self.args.startidx + (i+1)*nsize, self.args.endidx)] for i in range(int(len(allfiles)/nsize))]
        #print(batches)
        for batch in batches:
            if len(batch) == 0:
                continue
            print("-----------------Batch - " ,batch )
            pool.map(self._work , batch)


if __name__ == "__main__":
    source_path="F:\\Data\\satimages\\v4composite\\untar\\untar"
    dest_path = source_path + "\\countries"

    parser = argparse.ArgumentParser()
    parser.add_argument("--source" , default=source_path)
    parser.add_argument("--dest" , default=dest_path)
    parser.add_argument("--startidx" , default=0 , type=int)
    parser.add_argument("--endidx" , default=-1 , type=int)
    parser.add_argument("--re" , default=Config.v4composite_suffix)

    args = parser.parse_args()
    helper = Helpers(extraction_mode="COUNTRY")
    CountryExtractor(helper, args.source , args.dest , Config.COUNTRIES_TO_KEEP , args.re , args).Extract()
