
import cdsapi
import pygrib
import os
import numpy as np

FILE_NAME = "download.grib"
DOWNLOAD = not os.path.exists("download.grib")
REQUEST = {
    "variable": "2m_temperature",
    "product_type": "monthly_averaged_reanalysis",
    "year": "2008",
    "month": ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"],
    'time': '00:00',
    'grid': ['1', '1'],
    "format": "grib",
}
POZNAN_COORD={'lat': 52.40692, 'lon': 16.92993}

c = cdsapi.Client()
if DOWNLOAD:
    c.retrieve("reanalysis-era5-single-levels-monthly-means", REQUEST, "download.grib")

grbs = pygrib.open('download.grib')

# Available GRBS
print("Available msgs:")
for grb in grbs:
    print(grb)

grbs.rewind() # rewind the iterator
for i, grb in enumerate(grbs):
    print(f"\nMsg {i} ({grb})")

    lats, lons = grb.latlons()
    
    #print(f"Values: {grb.values.shape} [{grb.values.min()}-{grb.values.max()}]")
    #print(f"Lats: {lats.shape} [{lats.min()}-{lats.max()}]")
    #print(f"Lons: {lons.shape} [{lons.min()}-{lons.max()}]")
   
    lat_idx = np.argmin(abs(lats[:,0]-POZNAN_COORD["lat"]))
    lon_idx = np.argmin(abs(lons[0]-POZNAN_COORD["lon"]))

    print(f"{lats[lat_idx,0]}, {lons[0][lon_idx]}")
    print(f"{grb.values[lat_idx][lon_idx]-273}")

    #for j in range(len(grb.values)):
        #print(f"{i}, {j}: {len(lats[j])}, {len(lons[j])}, {len(grb.values[j])}")

