# database.py
# save dataframe to MySQL database
import sqlalchemy
from .export_table import *
from .get_weather import *


def sqldb_table_station_data():
    connect = sqlalchemy.create_engine('mysql://root:Max39629645@127.0.0.1/weather_website')
    station_data = get_data()
    station_data.to_sql("weather_station_data", connect, if_exists='replace')


def sqldb_table_weather():
    station_id, weather = get_weather_data()
    connect = sqlalchemy.create_engine('mysql://root:Max39629645@127.0.0.1/weather_website')
    weather.to_sql(f"{station_id}_weather", connect, if_exists='replace')