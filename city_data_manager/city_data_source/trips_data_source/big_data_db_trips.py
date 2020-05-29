import os
import datetime
import pytz

import numpy as np
import pandas as pd

from city_data_manager.city_data_source.trips_data_source.trips_data_source import TripsDataSource


class BigDataDBTrips(TripsDataSource):

    def __init__(self, city_name):
        super().__init__(city_name, "big_data_db_polito", "car_sharing")

    def load_raw(self):

        raw_trips_data_path = os.path.join(
            self.raw_data_path,
            "Dataset_" + self.city_name + ".csv"
        )
        self.trips_df = pd.read_csv(raw_trips_data_path)
        return self.trips_df

    def normalise(self, year, month):

        self.trips_df_norm = self.trips_df
        self.trips_df_norm = self.trips_df_norm.rename({
            col: col.replace("init", "start").replace("final", "end").replace(
                "lon", "longitude"
            ).replace("_lat", "_latitude").replace("distance", "euclidean_distance")
            for col in self.trips_df_norm
        }, axis=1)

        self.trips_df_norm = self.trips_df_norm[[
            "plate",
            "start_time",
            "end_time",
            "start_longitude",
            "start_latitude",
            "end_longitude",
            "end_latitude",
            "euclidean_distance"
        ]]

        self.trips_df_norm.start_time = self.trips_df_norm.start_time.apply(
            lambda ts: datetime.datetime.fromtimestamp(ts)
        )
        self.trips_df_norm.end_time = self.trips_df_norm.end_time.apply(
            lambda ts: datetime.datetime.fromtimestamp(ts)
        )

        self.trips_df_norm.start_time = self.trips_df_norm.start_time - datetime.timedelta(hours=2)
        self.trips_df_norm.end_time = self.trips_df_norm.end_time - datetime.timedelta(hours=2)
        self.trips_df_norm.start_time = pd.to_datetime(self.trips_df_norm.start_time, utc=True)
        self.trips_df_norm.end_time = pd.to_datetime(self.trips_df_norm.end_time, utc=True)

        if self.city_name == "Torino":
            tz = pytz.timezone("Europe/Rome")
        elif self.city_name == "Berlin":
            tz = pytz.timezone("Europe/Berlin")

        self.trips_df_norm.start_time = self.trips_df_norm.start_time.dt.tz_convert(tz)
        self.trips_df_norm.end_time = self.trips_df_norm.end_time.dt.tz_convert(tz)
        if month == 12:
            self.trips_df_norm = self.trips_df_norm[
                (self.trips_df_norm.start_time > datetime.datetime(year, month, 1, tzinfo=datetime.timezone.utc)) & (
                    self.trips_df_norm.start_time < datetime.datetime(year + 1, 1, 1, tzinfo=datetime.timezone.utc)
                )
            ]
        else:
            self.trips_df_norm = self.trips_df_norm[
                (self.trips_df_norm.start_time > datetime.datetime(year, month, 1, tzinfo=datetime.timezone.utc)) & (
                    self.trips_df_norm.start_time < datetime.datetime(year, month + 1, 1, tzinfo=datetime.timezone.utc)
                )
            ]

        self.trips_df_norm = super().normalise()
        self.save_norm()

        return self.trips_df_norm
