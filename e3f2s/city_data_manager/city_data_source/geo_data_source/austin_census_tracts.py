import os

import geopandas as gpd

from e3f2s.city_data_manager.city_data_source.geo_data_source.geo_data_source import GeoDataSource


class AustinCensusTracts(GeoDataSource):

    def __init__(self):
        super().__init__("Austin", "us_census_bureau")

    def load_raw(self):
        raw_geo_data_path = os.path.join(
            self.raw_data_path,
            "census_tracts_2010_msa.dbf"
        )
        self.gdf = gpd.read_file(raw_geo_data_path)
        return self.gdf

    def normalise(self):
        self.gdf_norm = self.gdf
        self.gdf_norm = self.gdf_norm.rename({
            "TRACTCE10": "census_tract_id"
        }, axis=1)
        self.gdf_norm = self.gdf_norm[[
            "census_tract_id", "geometry"
        ]]
        self.gdf_norm.census_tract_id = self.gdf_norm.census_tract_id.astype(int)

        self.gdf_norm.to_file(
            os.path.join(
                self.norm_data_path,
                "census_tracts.shp"
            )
        )
        return self.gdf_norm
