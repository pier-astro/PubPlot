from . import pubplotlib as _pubplotlib
from . import jbuilder
from . import formatter
from .formatter import set_formatter, set_ticks

# Import functions and constants
from .pubplotlib import (
    golden, pt, cm,
    load_journal_sizes, set_journal, get_journal,
    setup_figsize, figure, subplots
)

# Create properties to access the dynamic global variables
def __getattr__(name):
    if name == 'onecol':
        return _pubplotlib.onecol
    elif name == 'twocol':
        return _pubplotlib.twocol
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")