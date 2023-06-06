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

# Load ERA data
grb_data = data_loader.load()

# Prints
logger.debug("Available GRIB msgs:")
for grb in grb_data:
    logger.debug(grb)

total_data = []
year_data = []

grb_data.rewind() # rewind the iterator
for i, grb in enumerate(grb_data):

    # Get lat/lon values (single row/col)
    lats, lons = grb.latlons()
    lats = lats[:,0]
    lons = lons[0]

    # Make sure they match
    assert(grb.values.shape == lats.shape)
    assert(lons.shape == lats.shape)
   
    # Find closest lat/lon
    lat_idx = np.argmin(abs(lats-POZNAN_COORD["lat"]))
    lon_idx = np.argmin(abs(lons-POZNAN_COORD["lon"]))

    # Extract temp value
    # TODO: interpolation
    temp_k = grb.values[lat_idx][lon_idx]
    temp_c = temp_c -272.15

    year_data.append(temp_c)
    
    if grb.month == 12:
        logger.info(f"{grb.year}")
        total_data.append(year_data)
        year_data = []

visualizer.visu(total_data, data_loader.year_list)