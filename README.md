# PubPlotLib

[![PyPI version](https://badge.fury.io/py/pubplotlib.svg)](https://badge.fury.io/py/pubplotlib)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

`PubPlotLib` is a Python library built on top of Matplotlib that simplifies the creation of publication-quality figures. It provides pre-configured styles and sizes for major scientific journals, allowing you to focus on your data, not the boilerplate code for plotting.

## Key Features

*   **Journal-Ready Figures**: Automatically create figures with the correct dimensions and styles for journals like A&A, ApJ, and more.
*   **Simple API**: Use `pubplotlib.figure` and `pubplotlib.subplots` as drop-in replacements for their Matplotlib counterparts.
*   **Flexible Sizing**: Easily switch between single-column and double-column layouts and control the aspect ratio.
*   **Smart Formatting**: Apply sensible defaults for axis tick formatters that avoid scientific notation for numbers like 1.0 (i.e., no more $10^0$).
*   **Customizable Ticks**: Fine-tune the appearance of major and minor ticks with a single function call.
*   **Extensible**: Add your own custom journal styles and sizes with ease.

## Installation

You can install PubPlotLib via pip:

```bash
pip install pubplotlib
```

## Quick Start

Creating a journal-styled figure is as simple as importing `pubplotlib` and using its `subplots` function.

```python
import numpy as np
import matplotlib.pyplot as plt
import pubplotlib as pplt

# 1. Set your target journal (optional, can be done per-figure)
pplt.set_journal('apj')

# 2. Create data
x = np.linspace(0.1, 10, 500)
y = np.sin(x) / x

# 3. Create a figure using pubplotlib's wrapper
fig, ax = pplt.subplots()
ax.plot(x, y)
ax.set_xlabel("Time (s)")
ax.set_ylabel("Signal")

# 4. Customize ticks and formatters for a professional look
pplt.set_ticks(ax)
pplt.set_formatter(ax)

plt.show()
```

## Usage

### Figure Sizing

`PubPlotLib` makes it easy to create figures that fit perfectly into your manuscript's columns.

#### Single and Double Column Figures

Use the `twocols=True` argument to create a figure with the width of a double column.

```python
# A figure spanning two columns in an 'aanda' paper
fig, ax = pplt.subplots(journal='aanda', twocols=True)
ax.plot(...)
```

#### Custom Aspect Ratio

Control the figure's height using the `height_ratio` argument. The height will be `width * height_ratio`. If not provided, it defaults to the golden ratio.

```python
# Create a wide, short figure
fig, ax = pplt.subplots(twocols=True, height_ratio=0.3)
ax.plot(...)
```

### Axis Styling

#### Tick Customization

The `set_ticks()` function provides control over the appearance of axis ticks across all subplots in a figure.

```python
fig, ax = pplt.subplots()
ax.plot(...)

# Show ticks on all sides, pointing inwards
pplt.set_ticks(ax, direction='in', top=True, right=True)
```

#### Smart Axis Formatters

Logarithmic axes in Matplotlib often format the number 1 as $10^0$. `set_formatter()` applies a more readable formatter that uses decimal notation for numbers within a sensible range and scientific notation outside of it.

```python
fig, ax = pplt.subplots()
ax.loglog(x, 10**(y*4))

# Apply the formatter to both axes
pplt.set_formatter(ax) # No more "10^0"!
```

### Managing Journals

`PubPlotLib` comes with built-in support for several journals.

#### List Available Journals

See which journals are available out-of-the-box:

```python
print(pplt.available_journals())
```

#### Adding a New Journal

You can easily define and register your own journal style.

1.  **Create a `Journal` object**: Specify its name and column widths in inches. You can optionally link a `.mplstyle` file.

    ```python
    # Assumes 'my_style.mplstyle' exists in your working directory
    my_journal = pplt.Journal(
        name="my_journal",
        onecol=3.5,          # 3.5 inches wide
        twocol=7.1,          # 7.1 inches wide
        mplstyle="my_style.mplstyle"
    )
    ```

2.  **Register the journal**: This makes it available globally by copying the style file into the package's assets and adding it to the configuration.

    ```python
    my_journal.register(overwrite=True)
    ```

Now you can use it like any other journal:

```python
fig, ax = pplt.subplots(journal="my_journal")
```

#### Removing a Journal

You can remove a custom journal you've added.

```python
pplt.jbuilder.remove_journal("my_journal")
```

## Contributing

Contributions are welcome! If you'd like to add a new journal style, fix a bug, or suggest an improvement, please open an issue or submit a pull request on our GitHub repository.