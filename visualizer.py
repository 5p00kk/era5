import seaborn
import matplotlib.pyplot as plt
import numpy as np

class Visualizer:
    def __init__(self, ws=5) -> None:
        self.ws = ws

    def set_window(self, ws):
        self.ws = ws

    def visu(self, data, y_labels, title):
        data = np.array(data)
        output_shape = ((data.shape[0] - self.ws + 1, data.shape[1]))
        output = np.zeros(output_shape)

        for j in range(output_shape[1]):
            for i in range(output_shape[0]):
                window = data[i:(i+self.ws), j]
                output[i,j] = np.mean(window)
        
        y_labels=y_labels[self.ws:]
        ax = seaborn.heatmap(output, vmin = -40, vmax=40, cmap='coolwarm')
        ax.set_yticks(range(0, len(y_labels), 10))
        ax.set_yticklabels(y_labels[::10])
        ax.set_xticklabels([1,2,3,4,5,6,7,8,9,10,11,12])
        plt.title(title.upper())
        plt.xlabel("month")
        plt.ylabel("year")
        plt.savefig(title+".png")
        plt.close()