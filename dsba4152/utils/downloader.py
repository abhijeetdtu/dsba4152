import requests
from bs4 import BeautifulSoup
import re
import pickle
import os
import argparse
import time

import urllib.request
from multiprocessing.dummy import Pool as ThreadPool
#https://eogdata.mines.edu/wwwdata/viirs_products/dnb_composites/v10//201912/vcmcfg/SVDNB_npp_20191201-20191231_75N180W_vcmcfg_v10_c202001140900.tgz
#https://eogdata.mines.edu/wwwdata/viirs_products/dnb_composites/v10//201212/vcmcfg/SVDNB_npp_20121201-20121231_75N180W_vcmcfg_v10_c201601041440.tgz


class Downloader:
    base_html = "https://eogdata.mines.edu/pages/download_dnb_composites_iframe.html"

    def __init__(self,dest_path , args):

        self.dest_path = dest_path
        self.args = args
        self.startidx = args.startidx
        self.base_html = Downloader.base_html

    def get_links(self):
        page = requests.get(self.base_html)
        soup = BeautifulSoup(page.text)

        links = [a.get("href" ,"") for a in soup.select("a")]

        return links
        # print(links)
        # pickle.dump(links , open("links.pkl" , "wb"))
        # return pickle.load(open("links.pkl" , "rb"))

    def parse_links(self,links):
        retvals = []
        for a in links:
            year = re.findall("(20\d{2}12)/vcmcfg/" ,a)
            region = re.findall("(\d{2}[NS]\d{3}[EW])" , a)
            if len(year) > 0:
                year = year[0]
                retvals.append((year ,region[0], a))
        return retvals

    def _download_link(self , link):
        print(f"\n-- Downloading : {link}")
        year ,region, link = link
        path  = os.path.abspath(os.path.join(self.dest_path , f"{year}_{region}.tgz"))
        #fpath = os.path.abspath(os.path.join(path,year, region + ".tgz"))

        #if not os.path.exists(path):
        #    os.mkdir(path)
        #u = "https://raw.githubusercontent.com/abhijeetdtu/dsba4152/master/README.md"
        local_filename, headers = urllib.request.urlretrieve(link , path)

        # file = requests.get(link)
        # print(f"-- Saving : {link}")
        # with open(path , "wb") as f:
        #     f.write(file.content)

    def download_links(self,links):
        batch_size = 4
        pool = ThreadPool(batch_size)
        for batch in range(0 , len(links) , batch_size):
            pool.map(self._download_link, links[batch : batch+batch_size])
            time.sleep(self.args.batch_sleep)


    def pipe(self):
        links = self.get_links()
        links_december = self.parse_links(links)[self.startidx:]
        #print(links_december)
        self.download_links(links_december)

if __name__ == "__main__":
    dest_path = "F:\Data\satimages"
    parser = argparse.ArgumentParser()
    parser.add_argument("--dest-path" , default=dest_path , help="Folder to download the content to")
    parser.add_argument("--startidx" , default=0 ,type=int, help="Starting Link to download")
    parser.add_argument("--batch-sleep" , default=30 ,type=int, help="Time in seconds to pause after each batch")

    args = parser.parse_args()
    Downloader(args.dest_path , args).pipe()
