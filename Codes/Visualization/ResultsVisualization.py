from Codes.Configuration import Result_Path
from matplotlib.ticker import MaxNLocator
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import os


class ResultsVisualization:
    def Results_plot(self, junction_id, result, method_name, x_label, y_label, name_folder='Results', step=5):
        plt.figure(figsize=(25, 8))
        plt.title(method_name)
        # for i, result in enumerate(results):
        x = np.arange(step, len(result) + step, step)
        y = result[::step]
        plt.plot(x, y, label=method_name)
        plt.scatter(x, y, s=20)
        plt.legend(loc="best")
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        ax = plt.gca()
        ax.xaxis.set_major_locator(plt.MultipleLocator(step))
        ax.xaxis.set_major_formatter(plt.ScalarFormatter(useOffset=False, useMathText=True))
        ax.xaxis.set_minor_locator(ticker.AutoMinorLocator())
        plt.xticks(rotation=45, fontsize='xx-small')
        plt.grid()
        save_path = os.path.join(Result_Path, name_folder)
        os.makedirs(save_path, exist_ok=True)

        ax.xaxis.set_major_locator(MaxNLocator(integer=True))  # Example adjustment for x-axis
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))  # Example adjustment for y-axis

        plt.savefig(os.path.join(save_path, str(method_name) + "_" + junction_id + '.png'))
        plt.savefig(os.path.join(save_path, str(method_name) + "_" + junction_id + '.svg'), format='svg')
        # plt.show()  # Display the plot