
import cdsapi
import pygrib
import os
import numpy as np
from visualizer import Visualizer
from logger import Logger, Logger_level

logger = Logger(Logger_level.DEBUG)

visualizer = Visualizer()
visualizer.set_window(5)

year_list = [str(year) for year in range(1940,2023)]
FILE_NAME = "download.grib"
DOWNLOAD = not os.path.exists("download.grib")
REQUEST = {
    "variable": "2m_temperature",
    "product_type": "monthly_averaged_reanalysis",
    "year": year_list,
    "month": ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"],
    'time': '00:00',
    'grid': ['1', '1'],
    "format": "grib",
}
POZNAN_COORD={'lat': 40.37767, 'lon': 49.89201} # baku
POZNAN_COORD={'lat': 6.200000, 'lon': 106.816666} # jakarta
POZNAN_COORD={'lat': 52.40692, 'lon': 16.92993} # poznan

c = cdsapi.Client()
if DOWNLOAD:
    c.retrieve("reanalysis-era5-single-levels-monthly-means", REQUEST, "download.grib")

grbs = pygrib.open('download.grib')

# Available GRBS
print("Available msgs:")
for grb in grbs:
    print(grb)

total_data = []
year_data = []
grbs.rewind() # rewind the iterator
for i, grb in enumerate(grbs):
    lats, lons = grb.latlons()
    
    assert(grb.values.shape == lats.shape)
    assert(lons.shape == lats.shape)
   
    lat_idx = np.argmin(abs(lats[:,0]-POZNAN_COORD["lat"]))
    lon_idx = np.argmin(abs(lons[0]-POZNAN_COORD["lon"]))

    logger.debug(f"{lats[lat_idx,0]}, {lons[0][lon_idx]}")

    year_data.append(grb.values[lat_idx][lon_idx]-273)
    
    if grb.month == 12:
        logger.info(f"{grb.year}")
        total_data.append(year_data)
        year_data = []



visualizer.visu(total_data, year_list)