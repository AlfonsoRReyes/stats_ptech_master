"""
Thanks Josh Hemann for the example
"""
from __future__ import print_function
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon


class Distributions(object):
    # Generate some data from five different probability distributions,
    # each with different characteristics. We want to play with how an IID
    # bootstrap resample of the data preserves the distributional
    # properties of the original sample, and a boxplot is one visual tool
    # to make this assessment

    def __init__(self, samples=500, num_dists=5):
        self.bp = None
        self.percentiles = None
        self.N, self.data, self.numDists, self.randomDists = self.generate_data(samples, num_dists)

    def boxplot(self):
        N, data, numDists, randomDists = self.N, self.data, self.numDists, self.randomDists

        fig, ax1 = plt.subplots(figsize=(10, 6))
        fig.canvas.set_window_title('A Boxplot Example')
        plt.subplots_adjust(left=0.075, right=0.95, top=0.9, bottom=0.25)

        bp = plt.boxplot(data, notch=0, sym='+', vert=1, whis=1.5)
        plt.setp(bp['boxes'], color='black')
        plt.setp(bp['whiskers'], color='black')
        plt.setp(bp['fliers'], color='red', marker='+')

        # Add a horizontal grid to the plot, but make it very light in color
        # so we can use it for reading data values but not be distracting
        ax1.yaxis.grid(True, linestyle='-', which='major', color='lightgrey',
                       alpha=0.5)

        # Hide these grid behind plot objects
        ax1.set_axisbelow(True)
        ax1.set_title('Comparison of IID Bootstrap Resampling Across %d Distributions' % numDists)
        ax1.set_xlabel('Distribution')
        ax1.set_ylabel('Value')

        # Now fill the boxes with desired colors
        boxColors = ['darkkhaki', 'royalblue']
        numBoxes = numDists*2
        medians = list(range(numBoxes))
        for i in range(numBoxes):
            box = bp['boxes'][i]
            boxX = []
            boxY = []
            for j in range(5):
                boxX.append(box.get_xdata()[j])
                boxY.append(box.get_ydata()[j])
            boxCoords = list(zip(boxX, boxY))
            # Alternate between Dark Khaki and Royal Blue
            k = i % 2
            boxPolygon = Polygon(boxCoords, facecolor=boxColors[k])
            ax1.add_patch(boxPolygon)
            # Now draw the median lines back over what we just filled in
            med = bp['medians'][i]
            medianX = []
            medianY = []
            for j in range(2):
                medianX.append(med.get_xdata()[j])
                medianY.append(med.get_ydata()[j])
                plt.plot(medianX, medianY, 'k')
                medians[i] = medianY[0]
            # Finally, overplot the sample averages, with horizontal alignment
            # in the center of each box
            plt.plot([np.average(med.get_xdata())], [np.average(data[i])],
                     color='w', marker='*', markeredgecolor='k')

        # Set the axes ranges and axes labels
        ax1.set_xlim(0.5, numBoxes + 0.5)
        top = np.max(data)*1.1
        bottom = -5
        ax1.set_ylim(bottom, top)
        xtickNames = plt.setp(ax1, xticklabels=np.repeat(randomDists, 2))
        plt.setp(xtickNames, rotation=45, fontsize=8)

        # Due to the Y-axis scale being different across samples, it can be
        # hard to compare differences in medians across the samples. Add upper
        # X-axis tick labels with the sample medians to aid in comparison
        # (just use two decimal places of precision)
        pos = np.arange(numBoxes) + 1
        upperLabels = [str(np.round(s, 2)) for s in medians]
        weights = ['bold', 'semibold']
        for tick, label in zip(range(numBoxes), ax1.get_xticklabels()):
            k = tick % 2
            ax1.text(pos[tick], top - (top*0.05), upperLabels[tick],
                     horizontalalignment='center', size='x-small', weight=weights[k],
                     color=boxColors[k])

        # Finally, add a basic legend
        plt.figtext(0.80, 0.08, str(N) + ' Random Numbers',
                    backgroundcolor=boxColors[0], color='black', weight='roman',
                    size='x-small')
        plt.figtext(0.80, 0.045, 'IID Bootstrap Resample',
                    backgroundcolor=boxColors[1],
                    color='white', weight='roman', size='x-small')
        plt.figtext(0.80, 0.015, '*', color='white', backgroundcolor='silver',
                    weight='roman', size='medium')
        plt.figtext(0.815, 0.013, ' Average Value', color='black', weight='roman',
                    size='x-small')
        self.bp = bp
        plt.show()

    def generate_data(self, samples=500, num_dists=5):
        numDists = 5
        randomDists = ['Normal(1,1)', ' Lognormal(1,1)', 'Exp(1)', 'Gumbel(6,4)',
                       'Triangular(2,9,11)']
        N = samples
        norm = np.random.normal(1, 1, N)
        logn = np.random.lognormal(1, 1, N)
        expo = np.random.exponential(1, N)
        gumb = np.random.gumbel(6, 4, N)
        tria = np.random.triangular(2, 9, 11, N)

        # Generate some random indices that we'll use to resample the original data
        # arrays. For code brevity, just use the same random indices for each array
        # bootstrapIndices = np.random.random_integers(0, N - 1, N)
        bootstrapIndices = np.random.randint(0, N - 1, N)

        normBoot = norm[bootstrapIndices]
        lognBoot = logn[bootstrapIndices]
        expoBoot = expo[bootstrapIndices]
        gumbBoot = gumb[bootstrapIndices]
        triaBoot = tria[bootstrapIndices]

        # data = [norm, normBoot, logn, lognBoot, expo, expoBoot, gumb, gumbBoot,
        #         tria, triaBoot]

        data = list()
        distributions = {
            0: {'name': 'Normal(1,1)',        'data_1': norm, 'data_2': normBoot},
            1: {'name': 'Lognormal(1,1)',     'data_1': logn, 'data_2': lognBoot},
            2: {'name': 'Exp(1)',             'data_1': expo, 'data_2': expoBoot},
            3: {'name': 'Gumbel(6,4)',        'data_1': gumb, 'data_2': gumbBoot},
            4: {'name': 'Triangular(2,9,11)', 'data_1': tria, 'data_2': triaBoot},
            }

        random_dists = list()
        for i in range(0, num_dists):
            random_dists.append(distributions[i]['name'])
            data.append(distributions[i]['data_1'])
            data.append(distributions[i]['data_2'])

        return N, data, num_dists, random_dists

    def _get_percentiles_from_box_plots(self):
        """
        Get the raw data generated by matplotlib boxplot. We use this data to reverse engineer
        another function to plot the boxplot given only the percentiles and outliers.
        The data returned here is not clean.
        :return:
        """
        bp = self.bp
        percentiles = []
        for i in range(len(bp['boxes'])):
            percentiles.append((bp['caps'][2 * i].get_ydata()[0],
                                bp['boxes'][i].get_ydata()[0],
                                bp['medians'][i].get_ydata()[0],
                                bp['boxes'][i].get_ydata()[2],
                                bp['caps'][2 * i + 1].get_ydata()[0],
                                (bp['fliers'][i].get_xdata(),
                                 bp['fliers'][i].get_ydata())))
        return percentiles

    def get_percentiles_array(self):
        self.percentiles = self._get_percentiles_from_box_plots()
        # for i, member in enumerate(self.percentiles):
        #     print(i, len(member))
        #     # print(member[0])
        #     (q1_start, q2_start, q3_start, q4_start, q4_end, fliers_xy) = member
        #     print(q1_start, q2_start, q3_start, q4_start, q4_end, fliers_xy)
        #     # print(member)
        #     # data = list(member)
        #     # for m in range(0, len(data[0])):
        #     #     print(m, data[0][m])
        data = list()
        for box_no, pdata in enumerate(self.percentiles):
            print(box_no, len(pdata))
            if len(pdata) == 6:
                #: outlier provided too
                (q1_start, q2_start, q3_start, q4_start, q4_end, fliers_xy) = pdata
                try:
                    if len(fliers_xy[0]) != 0:
                        print("variable %d already with complete outliers arrays" % (box_no+1))
                except TypeError:
                    print("outliers arrays being fixed for variable %d" % (box_no+1))
                    arr_len = len(fliers_xy)
                    arr = np.full((1, arr_len), box_no + 1, dtype=np.int)
                    fliers_xy = [arr, fliers_xy]
                else:
                    print("variable %d has not outliers" % (box_no+1))

            elif len(pdata) == 5:
                print("variable %d has not outliers" % (box_no+1))
                #: only percentiles and no outliers provided
                (q1_start, q2_start, q3_start, q4_start, q4_end) = pdata
                fliers_xy = None
            else:
                raise ValueError("Percentile arrays for customized_box_plot must have either 5 or 6 values")

            data.append((q1_start, q2_start, q3_start, q4_start, q4_end, fliers_xy))
        return data

    def get_percentiles(self, var):
        print("percentiles for variable")
        pctl = np.percentile(var, [0, 25, 50, 75, 100])
        print(pctl)
        print("max", var.max())

        IQR = pctl[3] - pctl[1]
        print("\nIQR = ", IQR)

        out = IQR * 1.5
        print("\n1.5 * IQR = ", out)

        left = pctl[1] - out
        right = out + pctl[3]
        print("Find outliers on the left of %f and on the right of %f" % (left, right))



