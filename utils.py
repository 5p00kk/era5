import csv

def load_locations(file_name):
    locations = {}
    with open(file_name, newline='') as csvfile:
        cav_reader = csv.reader(csvfile, delimiter=',')
        for row in cav_reader:
            name = row[0]
            lat = float(row[1])
            lon = float(row[2])
            locations[name] = {"name": name, "lat": lat, "lon": lon}
    return locations