
import cdsapi
import pygrib
import os

FILE_NAME = "download.grib"
DOWNLOAD = not os.path.exists("download.grib")
REQUEST = {
    "variable": "2m_temperature",
    "product_type": "monthly_averaged_reanalysis",
    "year": "2008",
    "month": ["01", "02"],
    'time': '00:00',
    "format": "grib",
}

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
    
    print(f"Values: {grb.values.shape} [{grb.values.min()}-{grb.values.max()}]")
    print(f"Lats: {lats.shape} [{lats.min()}-{lats.max()}]")
    print(f"Lons: {lons.shape} [{lons.min()}-{lons.max()}]")
   
    #for j in range(len(grb.values)):
        #print(f"{i}, {j}: {len(lats[j])}, {len(lons[j])}, {len(grb.values[j])}")

