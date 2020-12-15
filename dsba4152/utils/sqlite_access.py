from dsba4152.utils.config import Config
import sqlite3
import geopandas
import json

from shapely.geometry import shape, mapping
from rasterio.plot import show
import shapely; shapely.speedups.disable()


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class GeoPKG(metaclass=Singleton):

    GDF_MASK = geopandas.read_file(
        geopandas.datasets.get_path("naturalearth_lowres")
    )

    def __init__(self):
        self.conn = sqlite3.connect(Config.shape_geopkg)

    def get_region_geom(self, mode , id , crs):
        if mode == "COUNTRY":
            return self.get_country_geom(id , crs)
        else:
            return self.get_state_geom(id)

    def get_country_geom(self, country_gid ,crs):
        countries_gdf = geopandas.read_file(Config.shape_geopkg ,  mask=GeoPKG.GDF_MASK[GeoPKG.GDF_MASK.iso_a3==country_gid])
        #print(json.loads(countries_gdf["geometry"].to_json()))
        countries_gdf = countries_gdf.to_crs(epsg=4326)
        #print(countries_gdf.shape)
        return countries_gdf["geometry"].apply(mapping).values
        #return [f['geometry'] for f in json.loads(countries_gdf.to_json())['features']]

    def get_state_geom(self , state_id ):
        gdf = geopandas.read_file(Config.india_shape_file_folder)
        gdf = gdf[gdf["NAME_1"] == state_id]
        #print(json.loads(countries_gdf["geometry"].to_json()))
        gdf = gdf.to_crs(epsg=4326)
        #print(countries_gdf.shape)
        return gdf["geometry"].apply(mapping).values

    def get_all_indian_states(self):
        return geopandas.read_file(Config.india_shape_file_folder)["NAME_1"].unique()

if __name__ == "__main__":
    from dsba4152.utils.helpers import Helpers
    img = Helpers().read_year_img(1992)
    print(img.crs , img.transform , img.shape)
    r= GeoPKG().get_country_geom("IND" , img.crs)
    #print(r)
    pass
