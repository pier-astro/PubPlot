import matplotlib.pyplot as plt  # type: ignore
import yaml
from importlib.resources import files

# --- Constants ---
golden = (1 + 5**0.5) / 2  # golden ratio
pt = 1 / 72.27             # points to inches
cm = 1 / 2.54              # centimeters to inches

# --- Global State ---
_default_journal = "aanda"
_current_journal = None
onecol = None
twocol = None

_style_files_cache = {}
_loaded_styles = set()

__all__ = [
    'golden', 'pt', 'cm',
    'onecol', 'twocol',
    'load_journal_sizes', 'set_journal', 'get_journal',
    'setup_figsize', 'figure', 'subplots', 'set_ticks',
    'available_journals'
]

# --- Public API ---

def load_journal_sizes():
    """Load journal sizes from a YAML configuration file (cached).

    Returns:
        dict: A dictionary containing journal sizes.
    """
    yaml_file = files("pubplotlib").joinpath("assets/journals.yaml")
    with open(yaml_file, "r") as file:
        return yaml.safe_load(file)

def available_journals():
    """Return a list of available journals."""
    return list(load_journal_sizes().keys())

def set_journal(journal):
    """Set the journal style and update global column sizes.

    Args:
        journal (str): The journal name to set.
    """
    global _default_journal, onecol, twocol, _current_journal

    if _current_journal == journal:
        return

    journal_sizes = load_journal_sizes()
    if journal not in journal_sizes:
        raise ValueError(f"Journal '{journal}' not recognized. Available journals: {list(journal_sizes.keys())}")

    onecol = journal_sizes[journal].get("onecol")
    twocol = journal_sizes[journal].get("twocol")

    if onecol is None and twocol is None:
        raise ValueError(f"Journal '{journal}' does not have defined column sizes. Please check the journals.yaml file.")

    _apply_style(journal)
    _current_journal = journal

def get_journal(journal=None):
    """Return the journal to use (passed or default).

    Args:
        journal (str, optional): Journal name.

    Returns:
        str: The journal to use.
    """
    if journal is not None:
        return journal
    if _current_journal is not None:
        return _current_journal
    else:
        return _default_journal

def setup_figsize(journal=None, twocols=False, height_ratio=None):
    """Set up figure dimensions for publication.

    Args:
        journal (str, optional): Target journal.
        twocols (bool): Use two-column width if True.
        height_ratio (float, optional): Custom height/width ratio.

    Returns:
        tuple: (width, height) in inches.
    """
    global onecol, twocol

    target_journal = get_journal(journal)
    if target_journal != _current_journal:
        set_journal(target_journal)
    else:
        _setup_journal_sizes()

    width = twocol if twocols else onecol
    if width is None:
        raise ValueError(f"Journal '{target_journal}' does not support {'two' if twocols else 'one'}-column figures.")

    height = width / golden if height_ratio is None else width * height_ratio
    return width, height

def figure(journal=None, twocols=False, height_ratio=None, **kwargs):
    """Create a figure with journal-appropriate dimensions.

    Args:
        journal (str, optional): Target journal.
        twocols (bool): Use two-column width if True.
        height_ratio (float, optional): Custom height/width ratio.

    Returns:
        matplotlib.figure.Figure: The created figure.
    """
    target_journal = get_journal(journal)
    if journal is not None and journal != _current_journal:
        set_journal(journal)
    elif _current_journal is None:
        set_journal(target_journal)

    width, height = setup_figsize(target_journal, twocols, height_ratio)
    fig = plt.figure(figsize=(width, height), **kwargs)
    return fig

def subplots(journal=None, twocols=False, height_ratio=None, **kwargs):
    """Create subplots with journal-appropriate dimensions.

    Args:
        journal (str, optional): Target journal.
        twocols (bool): Use two-column width if True.
        height_ratio (float, optional): Custom height/width ratio.

    Returns:
        tuple: (Figure, Axes) objects.
    """
    target_journal = get_journal(journal)
    if journal is not None and journal != _current_journal:
        set_journal(journal)
    elif _current_journal is None:
        set_journal(target_journal)

    width, height = setup_figsize(target_journal, twocols, height_ratio)
    fig, ax = plt.subplots(figsize=(width, height), **kwargs)
    return fig, ax



# --- Internal Helpers ---

def _get_style_file_path(journal):
    """Get and cache style file path for a journal."""
    if journal not in _style_files_cache:
        _style_files_cache[journal] = files("pubplotlib").joinpath(f"assets/{journal.lower()}.mplstyle")
    return _style_files_cache[journal]

def _apply_style(journal):
    """Apply matplotlib style for the given journal."""
    mplfile = _get_style_file_path(journal)
    if not mplfile.is_file():
        raise FileNotFoundError(f"Style file '{mplfile}' does not exist for journal '{journal}'.")
    plt.style.use(str(mplfile))
    _loaded_styles.add(journal)

def _setup_journal_sizes():
    """Initialize global onecol and twocol variables with default journal sizes."""
    global onecol, twocol, _current_journal
    if onecol is None or twocol is None:
        journal_sizes = load_journal_sizes()
        onecol = journal_sizes[_default_journal].get("onecol")
        twocol = journal_sizes[_default_journal].get("twocol")
        if _current_journal is None:
            _apply_style(_default_journal)
            _current_journal = _default_journal