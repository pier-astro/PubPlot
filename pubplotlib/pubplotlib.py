import matplotlib.pyplot as plt  # type: ignore
import os
import yaml
from .jbuilder import Journal, yaml_filename, assets_dir

# --- Constants ---
golden = (1 + 5**0.5) / 2  # golden ratio
pt = 1 / 72.27             # points to inches
cm = 1 / 2.54              # centimeters to inches

_default_journal = "aanda"
_current_journal = None

# --- Registry ---
def _load_journal_registry():
    with open(yaml_filename, "r") as file:
        raw = yaml.safe_load(file)
    return {
        name: Journal(
            name=name,
            onecol=entry.get("onecol"),
            twocol=entry.get("twocol"),
            mplstyle=assets_dir.joinpath(entry.get("mplstyle")).as_posix() if entry.get("mplstyle") else None,
        )
        for name, entry in raw.items()
    }

_journal_registry = _load_journal_registry()

def available_journals():
    """Return a list of available journals."""
    return list(_journal_registry.keys())

def get_journal(journal=None):
    """Return a Journal instance (from string or directly)."""
    if isinstance(journal, Journal):
        return journal
    if journal is not None:
        if journal not in _journal_registry:
            raise ValueError(f"Journal '{journal}' not found. Available: {available_journals()}")
        return _journal_registry[journal]
    return _journal_registry[_default_journal]

def set_journal(journal=None):
    """Apply the journal's style. Does nothing if already set."""
    global _current_journal
    j = get_journal(journal)
    if _current_journal == j.name:
        return
    
    if j.mplstyle is not None:
        if os.path.isabs(j.mplstyle):
            style_path = j.mplstyle
        else:
            style_path = str(assets_dir.joinpath(j.mplstyle))
        plt.style.use(style_path)
    _current_journal = j.name

def restore_matplotlib_default_style():
    """Restore matplotlib's default style."""
    plt.style.use('default')

def setup_figsize(journal=None, twocols=False, height_ratio=None):
    """Return (width, height) in inches for the journal."""
    j = get_journal(journal)
    set_journal(j)
    width = j.twocol if twocols else j.onecol
    if width is None:
        raise ValueError(f"Journal '{j.name}' does not support {'two' if twocols else 'one'}-column figures.")
    height = width / golden if height_ratio is None else width * height_ratio
    return width, height

def figure(journal=None, twocols=False, height_ratio=None, **kwargs):
    """Create a figure with journal-appropriate dimensions."""
    width, height = setup_figsize(journal, twocols, height_ratio)
    return plt.figure(figsize=(width, height), **kwargs)

def subplots(journal=None, twocols=False, height_ratio=None, **kwargs):
    """Create subplots with journal-appropriate dimensions."""
    width, height = setup_figsize(journal, twocols, height_ratio)
    return plt.subplots(figsize=(width, height), **kwargs)