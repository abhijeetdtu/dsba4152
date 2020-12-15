import unittest
import geopandas

from dsba4152.utils.config import Config
from dsba4152.utils.sqlite_access import GeoPKG

class GeoTests(unittest.TestCase):

    def test_shape_file_read(self):
        mask = geopandas.read_file(Config.india_shape_file_folder)
        self.assertGreater(len(mask.columns) , 0)
        self.assertTrue("NAME_1" in mask.columns)


    def test_get_state_shape(self):
        shp = GeoPKG().get_state_geom("Delhi")
        shp = shp[0]
        self.assertIsNotNone(shp)
        self.assertIsNotNone(shp["type"])
        self.assertEqual(shp["type"] , "Polygon")

    def test_get_all_indian_states(self):
        states =GeoPKG().get_all_indian_states()
        self.assertGreater(len(states) , 20)


if __name__ == "__main__":
    unittest.main()
