from dsba4152.utils.downloader import Downloader

import argparse
import re
import pandas as pd

class V4CompositeDownloader(Downloader):

    base_html = "https://eogdata.mines.edu/dmsp/downloadV4composites.html"

    def __init__(self,dest_path , args):
        super().__init__(dest_path , args)
        self.base_html = V4CompositeDownloader.base_html

    def parse_links(self,links):
        retvals = []

        for a in links:
            year = re.findall("F\d{2}(\d{4})\.v4" ,a)
            if len(year) > 0:
                year = year[0]
                retvals.append((year ,"all", a))

        df = pd.DataFrame(retvals , columns=["year" , "all" , "link"])
        df = df.groupby("year").head(1)
        return df.values


if __name__ == "__main__":
    dest_path = "F:\\Data\\satimages\\v4composite"
    parser = argparse.ArgumentParser()
    parser.add_argument("--dest-path" , default=dest_path , help="Folder to download the content to")
    parser.add_argument("--startidx" , default=0 ,type=int, help="Starting Link to download")
    parser.add_argument("--batch-sleep" , default=30 ,type=int, help="Time in seconds to pause after each batch")

    args = parser.parse_args()
    V4CompositeDownloader(args.dest_path , args).pipe()
