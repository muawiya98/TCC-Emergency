from Codes.Configuration import Result_Path
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import os
class KalmanVisualization:
    def vehicles_plot(self, edge, results, methods_name=['Measurement', 'Prediction'], name_folder='Results', step=5):
        plt.figure(figsize=(25, 8))
        plt.title(edge)
        for i, result in enumerate(results):
            x = np.arange(step, len(result) + step, step)
            y = result[::step]
            if step == 1:
                x = x[100:200]
                y = y[100:200]
            plt.plot(x, y, label=methods_name[i])
            plt.scatter(x, y, s=20)
        plt.legend(loc="best")
        plt.xlabel('Steps')
        plt.ylabel('Number Of Vehicle')
        ax = plt.gca()
        ax.xaxis.set_major_locator(plt.MultipleLocator(step))
        ax.xaxis.set_major_formatter(plt.ScalarFormatter(useOffset=False, useMathText=True))
        ax.xaxis.set_minor_locator(ticker.AutoMinorLocator())
        plt.xticks(rotation=45, fontsize='xx-small')
        plt.grid()
        save_path = os.path.join(Result_Path, name_folder)
        os.makedirs(save_path, exist_ok=True)

        plt.savefig(os.path.join(save_path, edge + '.png'))

        plt.savefig(os.path.join(save_path, edge + '.svg'), format='svg')
        # plt.show()  # Display the plot