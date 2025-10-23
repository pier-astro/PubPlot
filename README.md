# PubPlotLib 🎨

Effortlessly create publication-ready `matplotlib` figures with dimensions and styles tailored for specific academic journals.

`PubPlotLib` is a lightweight wrapper around `matplotlib` that takes the guesswork out of sizing your figures. Simply specify the target journal and page layout, and get a perfectly dimensioned figure and axes, ready for plotting.



---

## Features

* **Journal Presets**: Automatically sets figure dimensions for journals like *Astronomy & Astrophysics* (`aanda`) and more.
* **Style Integration**: Applies a corresponding `matplotlib` stylesheet (`.mplstyle`) for your chosen journal to ensure stylistic consistency.
* **Column Aware**: Easily create figures for single (`columns=1`) or double (`columns=2`) column layouts.
* **Smart Sizing**: Defaults to the golden ratio for a pleasing aspect ratio, but allows for full control via the `height_ratio` parameter.
* **Flexible**: Directly passes keyword arguments (`**kwargs`) to `matplotlib.pyplot.subplots`, so you retain full control.

---

## Installation

To add this library to your project, simply include the `pubplotlib.py` file and the `assets` directory. Your project will need the following dependencies:

```bash
pip install pubplotlib
```

---

## Quick Start

Creating a publication-ready figure is as simple as calling `setup_figure()` before you start plotting.

```python
import numpy as np
import pubplotlib as pplt
import matplotlib.pyplot as plt

# 1. Setup the figure for a single-column A&A article
# This returns matplotlib fig and ax objects with the correct size and style.
fig, ax = pplt.setup_figure(journal="aanda", columns=1)

# 2. Create your data
x = np.linspace(0, 2 * np.pi, 200)
y = np.sin(x)

# 3. Plot your data using the returned axes object
ax.plot(x, y, label=r'$\sin(x)$')
ax.set_xlabel("Angle [rad]")
ax.set_ylabel("Amplitude")
ax.set_title("My A&A Figure")
ax.legend()
ax.grid(True)

# 4. Save the figure with a tight layout
fig.savefig("aanda_figure.pdf", bbox_inches='tight')

# Optional: display the plot
plt.show()
```

This will produce a PDF file named `aanda_figure.pdf` correctly sized and styled for the journal.

---

## Customization

### Adding a New Journal

You can easily extend `PubPlotLib` to support new journals.

1.  **Add the Dimensions**: Open the `assets/journals.yaml` file and add a new entry with the journal's name and its single-column (`onecol`) and, if applicable, double-column (`twocol`) widths in points (pt).

    ```yaml
    # assets/journals.yaml
    aanda:
      onecol: 256.0748
      twocol: 523.5307

    # Add your new journal here
    newjournal:
      onecol: 300.0
      twocol: 600.0
    ```

2.  **Create a Style File**: Create a new matplotlib style file named `newjournal.mplstyle` in the `assets` directory. Here you can define colors, font sizes, line styles, and more.

    ```css
    # assets/newjournal.mplstyle
    axes.labelsize: 10
    font.size: 10
    legend.fontsize: 8
    xtick.labelsize: 8
    ytick.labelsize: 8
    ```

Now you can use your new journal preset: `pplt.setup_figure(journal="newjournal")`.

### Using `gridspec`

If you need more complex layouts (e.g., subplots of different sizes), you can set `gridspec=True`. This tells `PubPlot` to return only the `figure` object, which you can then use to create your own grid specification.

```python
import pubplot as pplt
import matplotlib.pyplot as plt

# Get a styled figure object
fig = pplt.setup_figure(journal="aanda", columns=2, gridspec=True)

# Create a custom grid
gs = fig.add_gridspec(2, 2)
ax1 = fig.add_subplot(gs[0, :])
ax2 = fig.add_subplot(gs[1, 0])
ax3 = fig.add_subplot(gs[1, 1])

# ... now you can plot on ax1, ax2, and ax3
```