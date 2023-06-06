import cdsapi
import pygrib
import os

class Era_data:
    def __init__(self, variable = "2m_temperature") -> None:
        self.cdsapi = cdsapi.Client()
        self.variable = variable
        self.filename = variable+".grib"
        self.year_list = [str(year) for year in range(1940,2023)]
        self.request = {
                        "variable": self.variable,
                        "product_type": "monthly_averaged_reanalysis",
                        "year": self.year_list,
                        "month": ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"],
                        "time": '00:00',
                        "grid": ['1', '1'],
                        "format": "grib"
                        }

    def load(self):
        if not os.path.exists(self.filename):
            self.cdsapi.retrieve("reanalysis-era5-single-levels-monthly-means", self.request, self.filename)
        return pygrib.open(self.filename)