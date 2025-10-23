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
    if ax is None:
        ax = plt.gca()

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
        wrap_axis(ax.xaxis)
    if axis in ['y', 'both']:
        wrap_axis(ax.yaxis)


def set_ticks(ax=None, minor=True, direction='in',
              right=True, top=True,
              majlen=3.5, minlen=1.75,
              majwidth=0.8, minwidth=0.8):
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
    majlen : float, default 7
        Length of major ticks (matplotlib default is 6).
    minlen : float, default 4
        Length of minor ticks (matplotlib default is 3).
    majwidth : float, default 0.8
        Width of major tick lines.
    minwidth : float, default 0.8
        Width of minor tick lines.
        
    Examples
    --------
    >>> fig, ax = plt.subplots()
    >>> set_ticks(ax, minor=True, direction='inout', majlen=8)
    """
    if ax is None:
        ax = plt.gca()

    ax.tick_params(which='major', length=majlen, width=majwidth,
                   direction=direction, right=right, top=top)
    
    if minor:
        ax.tick_params(which='minor', length=minlen, width=minwidth,
                       direction=direction, right=right, top=top)
    else:
        # Remove minor ticks
        ax.tick_params(which='minor', length=0, width=0,
                       direction=direction, right=right, top=top)
