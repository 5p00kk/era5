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
total_data = {}
year_data = {}
for location in locations.values():
    total_data[location["name"]] = []
    year_data[location["name"]] = []

logger.info(f"\nLoading all data (1940-2022)")
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

        for location in locations.values():
            # Find closest lat/lon
            lat_idx = np.argmin(abs(lats-location["lat"]))
            lon_idx = np.argmin(abs(lons-location["lon"]))

            # Extract temp value
            # TODO: interpolation
            temp_k = grb.values[lat_idx][lon_idx]
            temp_c = temp_k-272.15

            year_data[location["name"]].append(temp_c)
            
            if grb.month == 12:
                total_data[location["name"]].append(year_data[location["name"]])
                year_data[location["name"]] = []


for location in locations.values():
    logger.info(f"\nExtracting data for: {location['name'].upper()}")
    logger.info(f"Lat: {location['lat']} Lon: {location['lon']}")

    # Calculate averaged total and deviation data
    WS = 3
    data = np.array(total_data[location["name"]], dtype=np.float64)
    data_dev = deviation(data)
    data_avg = window_avg(data, WS)
    data_dev_avg = window_avg(data_dev, WS)
    minmax = max(abs(data_dev_avg.min()), abs(data_dev_avg.min()))

    logger.info(f"Temp range: {data.min()} to {data.max()}")
    logger.info(f"Temp deviation range: {data_dev_avg.min()} to {data_dev_avg.max()}")

    plot_heatmap(data_avg, data_loader.year_list[WS:], location["name"], "t", -40, 40)
    plot_heatmap(data_dev_avg, data_loader.year_list[WS:], location["name"], "d", -1*minmax, minmax)