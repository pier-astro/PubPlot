from .pubplotlib import (
    golden, pt, cm,
    set_journal, get_journal,
    available_journals, restore_matplotlib_default_style,
    setup_figsize, figure, subplots
)
from .formatter import set_formatter
from .ticksetter import set_ticks
from . import pubplotlib as _pubplotlib
from . import jbuilder
from .jbuilder import Journal
from . import formatter