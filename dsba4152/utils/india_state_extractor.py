from dsba4152.utils.country_extractor import CountryExtractor
from dsba4152.utils.config import Config
from dsba4152.utils.helpers import Helpers
from dsba4152.utils.sqlite_access import GeoPKG

import argparse

if __name__ == "__main__":
    source_path="F:\\Data\\satimages\\v4composite\\untar\\untar"
    dest_path = source_path + "\\ind_states"

    parser = argparse.ArgumentParser()
    parser.add_argument("--source" , default=source_path)
    parser.add_argument("--dest" , default=dest_path)
    parser.add_argument("--startidx" , default=0 , type=int)
    parser.add_argument("--endidx" , default=-1 , type=int)
    parser.add_argument("--re" , default=Config.v4composite_suffix)

    args = parser.parse_args()
    helper = Helpers(extraction_mode="STATE")
    states = GeoPKG().get_all_indian_states()
    CountryExtractor(helper, args.source , args.dest , states , args.re , args).Extract()
