import numpy as np
import matplotlib.pyplot as plt

def set_ticks(ax=None, minor=True, direction='in',
              right=True, top=True,
              major_length=3.5, minor_length=1.75,
              major_width=0.8, minor_width=0.8):
    """
    Configure tick appearance on axes.

    Parameters
    ----------
    ax : matplotlib.axes.Axes, optional
        Axes to configure. If None, uses current axes.
    minor : bool, default True
        Whether to show minor ticks.
    direction : {'in', 'out', 'inout'}, default 'inout'
        Direction of tick marks.
    right : bool, default False
        Whether to show ticks on right y-axis.
    top : bool, default False
        Whether to show ticks on top x-axis.
    major_length : float, default 3.5
        Length of major ticks.
    minor_length : float, default 1.75
        Length of minor ticks.
    major_width : float, default 0.8
        Width of major tick lines.
    minor_width : float, default 0.8
        Width of minor tick lines.
    """
    def apply_to_axis(ax_single):
        ax_single.tick_params(which='major', length=major_length, width=major_width,
                              direction=direction, right=right, top=top)
        if minor:
            ax_single.minorticks_on()
            ax_single.tick_params(which='minor', length=minor_length, width=minor_width,
                                  direction=direction, right=right, top=top)
        else:
            ax_single.tick_params(which='minor', length=0, width=0,
                                  direction=direction, right=right, top=top)

    if ax is None:
        axes = plt.gcf().get_axes()
    elif isinstance(ax, (list, tuple, np.ndarray)):
        axes = ax
    else:
        axes = [ax]

    for axis in axes:
        apply_to_axis(axis)