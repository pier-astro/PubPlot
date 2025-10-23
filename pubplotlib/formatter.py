import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import LogFormatterSciNotation as BaseLogFormatterSciNotation
from matplotlib.ticker import ScalarFormatter as BaseScalarFormatter


# ===================
# FORMATTERS
# ===================

class LogFormatterSciNotation(BaseLogFormatterSciNotation):
    """
    Custom logarithmic formatter with configurable scientific notation bounds.
    
    Shows decimal notation for values between `low` and `high`, and scientific
    notation outside this range.
    
    Parameters
    ----------
    low : float, default 1e-3
        Lower bound for decimal notation.
    high : float, default 1e3
        Upper bound for decimal notation.
    **kwargs
        Additional arguments passed to matplotlib's LogFormatterSciNotation.
    """
    def __init__(self, low=1e-3, high=1e3, **kwargs):
        super().__init__(**kwargs)
        self.low = low
        self.high = high

    def __call__(self, x, pos=None, **kwargs):
        out = super().__call__(x, pos, **kwargs)
        if out == '':
            return out
        if x > self.low and x < self.high:
            return f"{x:g}"
        else:
            return out


class ScalarFormatter(BaseScalarFormatter):
    """
    Custom scalar formatter with configurable scientific notation bounds.
    
    Shows decimal notation for values between `low` and `high`, and scientific
    notation outside this range.
    
    Parameters
    ----------
    low : float, default 1e-3
        Lower bound for decimal notation.
    high : float, default 1e3
        Upper bound for decimal notation.
    **kwargs
        Additional arguments passed to matplotlib's ScalarFormatter.
    """
    def __init__(self, low=1e-3, high=1e3, **kwargs):
        super().__init__(**kwargs)
        self.low = low
        self.high = high
        self.set_scientific(True)
        self.set_powerlimits((np.log10(low), np.log10(high)))
        self.set_useOffset(False)
        self.set_useMathText(True)

    def __call__(self, x, pos=None, **kwargs):
        out = super().__call__(x, pos, **kwargs)
        if out == '':
            return out
        if x > self.low and x < self.high:
            return f"{x:g}"
        else:
            return out


class SelectiveFormatter(LogFormatterSciNotation):
    """
    Formatter that only displays labels for specified tick values.
    
    Useful for showing labels only on major ticks while keeping minor ticks unlabeled.
    
    Parameters
    ----------
    tick_labels : array-like
        The numerical values for which labels should be shown.
    *args, **kwargs
        Additional arguments passed to LogFormatterSciNotation.
        
    Examples
    --------
    >>> import matplotlib.pyplot as plt
    >>> import matplotlib.ticker as ticker
    >>> 
    >>> # Setup selective formatting
    >>> tickvalues = generate_log_ticks(0.01, 100)
    >>> major_ticks = generate_powers_of_10_ticks(0.01, 100)
    >>> minor_ticks = filter_major_ticks(tickvalues, major_ticks)
    >>> formatter = SelectiveFormatter(major_ticks)
    >>> 
    >>> # Apply to axes
    >>> fig, ax = plt.subplots()
    >>> ax.xaxis.set_major_formatter(formatter)
    >>> ax.xaxis.set_major_locator(ticker.FixedLocator(major_ticks))
    >>> ax.xaxis.set_minor_locator(ticker.FixedLocator(minor_ticks))
    """
    def __init__(self, tick_labels, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tick_labels = np.asarray(tick_labels, dtype=float)

    def __call__(self, x, pos=None):
        if any(np.isclose(x, val) for val in self.tick_labels):
            return super().__call__(x, pos)
        else:
            return ""



# ===================
# AXIS CONFIGURATION
# ===================

def set_formatter(ax=None, low=0.01, high=100, axis='both'):
    """
    Apply custom formatting to axis that preserves matplotlib's tick placement.
    
    Uses decimal notation for values between `low` and `high`, and scientific
    notation outside this range.
    
    Parameters
    ----------
    ax : matplotlib.axes.Axes, optional
        Axes to format. If None, uses current axes.
    low : float, default 0.01
        Lower bound for decimal notation.
    high : float, default 100
        Upper bound for decimal notation.
    axis : {'x', 'y', 'both'}, default 'both'
        Which axes to format.
        
    Examples
    --------
    >>> fig, ax = plt.subplots()
    >>> ax.loglog(x, y)
    >>> set_formatter(ax, low=0.01, high=100)
    """
    def apply_to_axis(ax_single):
        def wrap_axis(axis_obj):
            default_major_formatter = axis_obj.get_major_formatter()
            if isinstance(default_major_formatter, BaseLogFormatterSciNotation):
                axis_obj.set_major_formatter(LogFormatterSciNotation(low=low, high=high))
            elif isinstance(default_major_formatter, BaseScalarFormatter):
                axis_obj.set_major_formatter(ScalarFormatter(low=low, high=high))
            
            default_minor_formatter = axis_obj.get_minor_formatter()
            if isinstance(default_minor_formatter, BaseLogFormatterSciNotation):
                axis_obj.set_minor_formatter(LogFormatterSciNotation(low=low, high=high))
            elif isinstance(default_minor_formatter, BaseScalarFormatter):
                axis_obj.set_minor_formatter(ScalarFormatter(low=low, high=high))
            
        if axis in ['x', 'both']:
            wrap_axis(ax_single.xaxis)
        if axis in ['y', 'both']:
            wrap_axis(ax_single.yaxis)

    if ax is None:
        axes = plt.gcf().get_axes()
    elif isinstance(ax, (list, tuple, np.ndarray)):
        axes = ax
    else:
        axes = [ax]

    for axis in axes:
        apply_to_axis(axis)


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