import csv
import numpy as np
import seaborn
import matplotlib.pyplot as plt
import os

def load_locations(file_name):
    locations = {}
    with open(file_name, newline='') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        next(csv_reader, None)
        for row in csv_reader:
            name = row[0]
            lat = float(row[1])
            lon = float(row[2])
            locations[name] = {"name": name, "lat": lat, "lon": lon}
    return locations

def deviation(data):
    dev_data = np.zeros(data.shape, dtype=np.float)
    for col in range(data.shape[1]):
        col_avg = np.average(data[:,col])
        dev_data[:,col] = data[:,col]-col_avg
    return dev_data

def window_avg(data, ws):
    output_shape = ((data.shape[0] - ws + 1, data.shape[1]))
    output = np.zeros(output_shape)
    for j in range(output_shape[1]):
        for i in range(output_shape[0]):
            window = data[i:(i+ws), j]
            output[i,j] = np.mean(window)
    return output

def plot_heatmap(data, y_labels, title, prefix="", min=None, max=None):
    ax = seaborn.heatmap(data, vmin=min, vmax=max, cmap='coolwarm')
    # Set x and y ticks
    ax.set_yticks(range(0, len(y_labels), 10))
    ax.set_yticklabels(y_labels[::10])
    ax.set_xticklabels([1,2,3,4,5,6,7,8,9,10,11,12])
    # Set titles
    plt.title(title.upper())
    plt.xlabel("month")
    plt.ylabel("year")
    # Save
    filename = prefix+"_"+title+".png"
    plt.savefig(os.path.join("output", filename))
    plt.close()