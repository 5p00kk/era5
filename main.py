import numpy as np
from era_data import Era_data
from visualizer import Visualizer
from logger import Logger, Logger_level
from utils import load_locations
from tqdm import tqdm

# Init objects
data_loader = Era_data("2m_temperature")
logger = Logger(Logger_level.INFO)
visualizer = Visualizer(5)

# Load ERA data
grb_data = data_loader.load()

# Load locations
locations = load_locations("locations.csv")

# Prints
logger.debug("Available GRIB msgs:")
for grb in grb_data:
    logger.debug(grb)

total_it = len(data_loader.year_list)*12

for location in locations.values():
    total_data = []
    year_data = []

    logger.info(f"Extracting data for: {location['name'].upper()}")
    logger.info(f"Lat: {location['lat']} Lon: {location['lon']}")

    grb_data.rewind() # rewind the iterator
    with tqdm(total=total_it) as progress_bar:
        for i, grb in enumerate(grb_data):
            
            # Update progress bar
            progress_bar.set_description(f"{grb.year}")
            progress_bar.update(1)

            # Get lat/lon values
            lats, lons = grb.latlons()
            # Make sure they match
            assert(grb.values.shape == lats.shape)
            assert(lons.shape == lats.shape)
            # Get single row/col as they repeat
            lats = lats[:,0]
            lons = lons[0]

            # Find closest lat/lon
            lat_idx = np.argmin(abs(lats-location["lat"]))
            lon_idx = np.argmin(abs(lons-location["lon"]))

            # Extract temp value
            # TODO: interpolation
            temp_k = grb.values[lat_idx][lon_idx]
            temp_c = temp_k -272.15

            year_data.append(temp_c)
            
            if grb.month == 12:
                #logger.info(f"{grb.year}")
                total_data.append(year_data)
                year_data = []

    logger.info(f"Temp range: {min(min(total_data))} to {max(max(total_data))}")
    visualizer.visu(total_data, data_loader.year_list, location["name"])