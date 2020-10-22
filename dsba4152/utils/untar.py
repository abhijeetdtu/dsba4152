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

class TarMove:

    def __init__(self,source_path , dest_path , startidx=0 , re=None , args=None):
        self.source_path = source_path
        self.dest_path = dest_path
        self.startidx = startidx
        self.re = re
        self.args = args

    def winrar(self,f):
        subprocess.call(f"winrar x -ibck {f} *.* {self.dest_path}" , shell=False)

    def tar(self,f):
        tar = tarfile.open()
        tar.extractall(path=self.dest_path)
        tar.close()

    def _work(self , f):
        consider = True if self.re is None else f.find(self.re) > -1
        if (f.find(self.args.tar_format) > -1) and consider:
            print(f"Processing {f}")
            #tarpath= f.replace(".tar.gz" , ".log")

            #shutil.copyfile(pathlib.Path(expath , f).absolute() , pathlib.Path(expath , f).absolute())
            print(f"-- Extraction Started")
            f = pathlib.Path(self.source_path , f).absolute()
            if self.args.tar_format == ".gz":
                self.winrar(f)
            else:
                self.tar(f)
            print(f"-- Extraction done")


    def Extract(self ):
        nsize = 4
        pool = Pool(nsize)
        re = self.re if self.re is not None else self.args.tar_format
        allfiles = [f for f in  os.listdir(self.source_path) if (f.find(self.args.tar_format) > -1) and (f.find(re) > -1)]

        if self.args.endidx == -1:
            self.args.endidx = len(allfiles)
        if self.startidx < 0:
            self.startidx =  len(allfiles) + self.startidx #-1

        batches = [allfiles[(self.startidx + i*nsize ): min(self.startidx + (i+1)*nsize, self.args.endidx)] for i in range(int(len(allfiles)/nsize))]
        #print(batches)
        for batch in batches:
            if len(batch) == 0:
                continue
            print("-----------------Batch - " ,batch )
            pool.map(self._work , batch)


if __name__ == "__main__":
    source_path="F:\\Data\\satimages\\v4composite"
    dest_path = source_path + "\\untar"

    parser = argparse.ArgumentParser()
    parser.add_argument("--source" , default=source_path)
    parser.add_argument("--dest" , default=dest_path)
    parser.add_argument("--startidx" , default=0 , type=int)
    parser.add_argument("--endidx" , default=-1 , type=int)
    parser.add_argument("--re" , default=None)
    parser.add_argument("--tar-format" , default=".tgz")

    args = parser.parse_args()

    TarMove(args.source , args.dest , args.startidx , args.re , args).Extract()
