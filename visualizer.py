import seaborn
import matplotlib.pyplot as plt
import numpy as np

class Visualizer:
    def __init__(self) -> None:
        self.ws = 5

    def set_window(self, ws):
        self.ws = ws

    def visu(self, data, y_labels):
        data = np.array(data)
        output_shape = ((data.shape[0] - self.ws + 1, data.shape[1]))
        output = np.zeros(output_shape)

        for j in range(output_shape[1]):
            for i in range(output_shape[0]):
                window = data[i:(i+self.ws), j]
                output[i,j] = np.mean(window)
        
        y_labels=y_labels[self.ws:]
        ax = seaborn.heatmap(output, cmap=seaborn.cubehelix_palette(as_cmap=True))
        ax.set_yticks(range(0, len(y_labels), 5))
        ax.set_yticklabels(y_labels[::5])
        plt.show()