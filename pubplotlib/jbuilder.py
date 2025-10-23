from typing import Dict, Optional, Mapping
import yaml

def build_journal_sizes(
    filename: str = "journals.yaml",
    pt: float = 1 / 72.27,
    custom: Optional[Mapping[str, Mapping[str, float]]] = None,
    write_yaml: bool = True,
) -> Dict[str, Dict[str, float]]:
    """
    Build a dictionary of journal column sizes (in inches) and optionally
    write it to a YAML file.

    Args:
        filename: path to write YAML file (default "journals.yaml").
        pt: points-to-inches conversion factor (default 1/72.27).
        custom: optional mapping to add or override journal entries.
                Example: {"mnras": {"onecol": 240.0 * pt}}
        write_yaml: if True, writes the resulting dict to `filename`.

    Returns:
        The journal sizes dict with dimensions in inches.
    """
    jour_sizes: Dict[str, Dict[str, float]] = {
        "aanda": {"onecol": 256.0 * pt, "twocol": 523.5 * pt},
        "apj": {"onecol": 242.0 * pt},
    }

    if custom:
        # Shallow merge: override existing journal keys or add new ones.
        for journal, cols in custom.items():
            existing = jour_sizes.get(journal, {})
            jour_sizes[journal] = {**existing, **cols}

    if write_yaml:
        with open(filename, "w", encoding="utf-8") as f:
            yaml.safe_dump(jour_sizes, f, default_flow_style=False)

    return jour_sizes