
#: new version of the function
#: we will check if the variable provided has outliers with order


from __future__ import print_function
import matplotlib.pyplot as plt
import numpy as np

def customized_box_plot(percentiles, xtlabels=None, redraw = True, printdata=False, *args, **kwargs):
    """
    Generates a customized boxplot based on the given percentile values
    """
    xtlabel = list()
    fig, ax = plt.subplots()
    axes = ax
    n_box = len(percentiles)      
    
    box_plot = axes.boxplot([[-9, -4, 2, 4, 9],]*n_box, *args, **kwargs) 
    # Creates len(percentiles) no of box plots

    min_y, max_y = float('inf'), -float('inf')

    for box_no, pdata in enumerate(percentiles):
        if xtlabels is None:
            xtlabel.append(str(box_no+1))
        else:
            xtlabel = xtlabels
        
        if len(pdata) == 6:
            #: outlier provided too
            (q1_start, q2_start, q3_start, q4_start, q4_end, fliers_xy) = pdata
            try:
                if len(fliers_xy[0]) != 0:
                    print("variable already with complete outliers arrays")
            except TypeError:
                arr_len = len(fliers_xy) 
                arr = np.full((1, arr_len), box_no+1, dtype=np.int)
                fliers_xy = [arr, fliers_xy]
                print("outliers arrays being fixed for variable %d" % box_no)
            
        elif len(pdata) == 5:
            #: only percentiles and no outliers provided
            (q1_start, q2_start, q3_start, q4_start, q4_end) = pdata
            fliers_xy = None
        else:
            raise ValueError("Percentile arrays for customized_box_plot must have either 5 or 6 values")
        if printdata:
            print(percentiles)
        # Lower cap
        box_plot['caps'][2*box_no].set_ydata([q1_start, q1_start])
        # xdata is determined by the width of the box plot

        # Lower whiskers
        box_plot['whiskers'][2*box_no].set_ydata([q1_start, q2_start])

        # Higher cap
        box_plot['caps'][2*box_no + 1].set_ydata([q4_end, q4_end])

        # Higher whiskers
        box_plot['whiskers'][2*box_no + 1].set_ydata([q4_start, q4_end])

        # Box
        path = box_plot['boxes'][box_no].get_path()
        path.vertices[0][1] = q2_start
        path.vertices[1][1] = q2_start
        path.vertices[2][1] = q4_start
        path.vertices[3][1] = q4_start
        path.vertices[4][1] = q2_start

        # Median
        box_plot['medians'][box_no].set_ydata([q3_start, q3_start])

        # Outliers
        if fliers_xy is not None and len(fliers_xy[0]) != 0:
            # If outliers exist
            box_plot['fliers'][box_no].set(xdata = fliers_xy[0],
                                           ydata = fliers_xy[1])

            min_y = min(q1_start, min_y, fliers_xy[1].min())
            max_y = max(q4_end, max_y, fliers_xy[1].max())

        else:
            min_y = min(q1_start, min_y)
            max_y = max(q4_end, max_y)

        # The y axis is rescaled to fit the new box plot completely with 10% 
        # of the maximum value at both ends
        # print(min_y, max_y)
        axes.set_ylim([min_y*1.1, max_y*1.1])
    ax.set_xticklabels(xtlabel)

    # If redraw is set to true, the canvas is updated.
    if redraw:
        axes.figure.canvas.draw()
    plt.show()
    return box_plot