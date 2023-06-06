import numpy as np
from era_data import Era_data
from visualizer import Visualizer
from logger import Logger, Logger_level


POZNAN_COORD={'lat': 40.37767, 'lon': 49.89201} # baku
POZNAN_COORD={'lat': 6.200000, 'lon': 106.816666} # jakarta
POZNAN_COORD={'lat': 52.40692, 'lon': 16.92993} # poznan

# Init objects
data_loader = Era_data("2m_temperature")
logger = Logger(Logger_level.INFO)
visualizer = Visualizer(5)




grb_data = data_loader.load()

# Available GRBS
logger.debug("Available GRIB msgs:")
for grb in grb_data:
    logger.debug(grb)

total_data = []
year_data = []
grb_data.rewind() # rewind the iterator
for i, grb in enumerate(grb_data):
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



visualizer.visu(total_data, data_loader.year_list)