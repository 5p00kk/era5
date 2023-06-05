
import cdsapi
import pygrib

DOWNLOAD = False

if DOWNLOAD:
    c = cdsapi.Client()
    c.retrieve("reanalysis-era5-single-levels-monthly-means",
    {
    "variable": "2m_temperature",
    "product_type": "monthly_averaged_reanalysis",
    "year": "2008",
    "month": ["01", "02"],
    'time': '00:00',
    "format": "grib",
    }, "download.grib")

grbs = pygrib.open('download.grib')

# Available GRBS
for grb in grbs:
    print(grb)
#for key in grbs[1].keys():
#    print(key)

grbs.rewind() # rewind the iterator
i = 0
for grb in grbs:
    lats, lons = grb.latlons()
    
    print(grb.values.shape)
    print(lats.shape)
    print(lons.shape)

    print(f"{grb.values.min()} {grb.values.max()}")
    print(f"{lats.min()} {lats.max()}")
    print(f"{lons.min()} {lons.max()}")
    
    #for j in range(len(grb.values)):
        #print(f"{i}, {j}: {len(lats[j])}, {len(lons[j])}, {len(grb.values[j])}")

