import matplotlib.pyplot as plt #type: ignore
import yaml
from importlib.resources import files

golden = (1 + 5**0.5) / 2  # golden ratio
pt = 1 / 72.27  # points to inches
cm = 1 / 2.54  # centimeters to inches

def load_journal_sizes():
    """Load journal sizes from a YAML configuration file.

    Returns:
    dict: A dictionary containing journal sizes.
    """
    
    yaml_file = files("pubplotlib").joinpath("assets/journals.yaml")

    with open(yaml_file, "r") as file:
        jour_sizes = yaml.safe_load(file)
    
    return jour_sizes


def setup_figure(journal="aanda", columns=1, height_ratio=None, jour_sizes=None, gridspec=False, **kwargs):
    """Set up a matplotlib figure with dimensions suitable for publication.

    Parameters:
    journal (str): The target journal for the figure dimensions.
    columns (int): Number of columns the figure should span (1 or 2).
    height_ratio (float): Ratio of height to width for the figure.

    Returns:
    fig, ax: Matplotlib figure and axis objects.
    """

    if jour_sizes is None:
        jour_sizes = load_journal_sizes()
    

    if journal not in jour_sizes:
        raise ValueError(f"Journal '{journal}' not recognized. Available journals: {list(jour_sizes.keys())}")

    if columns == 1:
        width = jour_sizes[journal]["onecol"]
    elif columns == 2:
        if "twocol" in jour_sizes[journal]:
            width = jour_sizes[journal]["twocol"]
        else:
            raise ValueError(f"Journal '{journal}' does not support two-column figures.")
    else:
        raise ValueError("Columns must be either 1 or 2.")

    if height_ratio is None:
        height_ratio = 1 / golden
        height = width * height_ratio
    else:   
        height = width * height_ratio

    # match case for matplotlib style
    plt.style.use(files("pubplotlib").joinpath(f"assets/{journal.lower()}.mplstyle"))
    
    if gridspec:
        fig = plt.figure(figsize=(width, height), **kwargs)
        return fig
    else:
        fig, ax = plt.subplots(figsize=(width, height), **kwargs)
        return fig, ax