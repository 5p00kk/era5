import numpy as np
from era_data import Era_data
from logger import Logger, Logger_level
from utils import load_locations, window_avg, deviation, plot_heatmap
from tqdm import tqdm

# Init objects
data_loader = Era_data("2m_temperature")
logger = Logger(Logger_level.INFO)

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

    logger.info(f"\nExtracting data for: {location['name'].upper()}")
    logger.info(f"Lat: {location['lat']} Lon: {location['lon']}")

    # TODO this loop can be done only once
    # TODO Save all data with single loop run
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
            temp_c = temp_k-272.15

            year_data.append(temp_c)
            
            if grb.month == 12:
                #logger.info(f"{grb.year}")
                total_data.append(year_data)
                year_data = []

    # Calculate averaged total and deviation data
    WS = 3
    total_data = np.array(total_data, dtype=np.float64)
    dev_data = deviation(total_data)
    total_data_avg = window_avg(total_data, WS)
    dev_data_avg = window_avg(dev_data, WS)
    minmax = max(abs(dev_data_avg.min()), abs(dev_data_avg.min()))

    logger.info(f"Temp range: {total_data.min()} to {total_data.max()}")
    logger.info(f"Temp deviation range: {dev_data_avg.min()} to {dev_data_avg.max()}")

    plot_heatmap(total_data_avg, data_loader.year_list[WS:], location["name"], "t", -40, 40)
    plot_heatmap(dev_data_avg, data_loader.year_list[WS:], location["name"], "d", -1*minmax, minmax)