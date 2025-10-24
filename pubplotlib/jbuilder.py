from typing import Optional, Dict
import yaml
import os
import shutil
from importlib.resources import files

# --- Module-level paths ---
assets_dir = files("pubplotlib").joinpath("assets")
yaml_filename = assets_dir.joinpath("journals.yaml")

def build_journals(overwrite: bool = False) -> Dict[str, Dict[str, object]]:
    """
    Build and write the default journals YAML file with standard journals.
    Overwrites the file if overwrite=True.

    Args:
        overwrite: if True, overwrites the YAML file if it exists.

    Returns:
        The journal dict with dimensions in inches and style paths.
    """
    pt = 1 / 72.27  # points to inches conversion factor
    journals: Dict[str, Dict[str, object]] = {
        "aanda": {
            "onecol": 256.0 * pt,
            "twocol": 523.5 * pt,
            "mplstyle": "aanda.mplstyle",
        },
        "apj": {
            "onecol": 242.0 * pt,
            "mplstyle": "apj.mplstyle",
        },
    }

    if yaml_filename.exists() and not overwrite:
        raise FileExistsError(f"{yaml_filename} already exists. Use overwrite=True to overwrite.")

    with open(yaml_filename, "w", encoding="utf-8") as f:
        yaml.safe_dump(journals, f, default_flow_style=False)

    return journals

class Journal:
    """
    Represents a scientific journal's figure formatting requirements.

    Attributes:
        name (str): The journal's name.
        onecol (Optional[float]): Width of a single column (in inches).
        twocol (Optional[float]): Width of a double column (in inches).
        mplstyle (Optional[str]): Path to the associated .mplstyle file.
    """
    def __init__(
        self,
        name: str,
        onecol: Optional[float] = None,
        twocol: Optional[float] = None,
        mplstyle: Optional[str] = None,
    ):
        self.name = name
        self.onecol = onecol
        self.twocol = twocol

        # Always store the style filename (not full path)
        if mplstyle is None:
            style_filename = f"{self.name.lower()}.mplstyle"
        else:
            style_filename = os.path.basename(mplstyle)
        self.mplstyle = style_filename

        if self.onecol is None and self.twocol is None:
            raise ValueError("At least one of 'onecol' or 'twocol' must be provided.")

        # Check that the style file exists in assets_dir
        style_path = assets_dir.joinpath(self.mplstyle)
        if not style_path.exists():
            raise FileNotFoundError(f"Style file '{style_path}' does not exist in assets directory.")

    def register(self, overwrite: bool = False):
        """
        Register this Journal in the default journals YAML file.
        Copies the mplstyle file into the assets directory if needed.

        Args:
            overwrite (bool): If True, overwrite existing entry and style file.
        """
        style_filename = self.mplstyle
        style_dest = assets_dir.joinpath(style_filename)

        # If the style file is not in assets_dir, copy it there
        if not style_dest.exists() or overwrite:
            # If the user gave a full path, copy from there; otherwise, error
            if not style_dest.exists() and not os.path.isabs(style_filename):
                raise FileNotFoundError(
                    f"Style file '{style_dest}' does not exist. Please provide the full path to the style file."
                )
            # Only copy if the source is not already the destination
            if os.path.isabs(style_filename) and (not style_dest.exists() or overwrite):
                shutil.copyfile(style_filename, style_dest)

        # Load or create the YAML
        if yaml_filename.exists():
            with open(yaml_filename, "r", encoding="utf-8") as f:
                journals = yaml.safe_load(f) or {}
        else:
            journals = {}

        if self.name in journals and not overwrite:
            raise ValueError(
                f"Journal '{self.name}' already exists in {yaml_filename}. Use overwrite=True to replace it."
            )

        journals[self.name] = {}
        if self.onecol is not None:
            journals[self.name]["onecol"] = self.onecol
        if self.twocol is not None:
            journals[self.name]["twocol"] = self.twocol
        journals[self.name]["mplstyle"] = style_filename

        with open(yaml_filename, "w", encoding="utf-8") as f:
            yaml.safe_dump(journals, f, default_flow_style=False)
        
    def __repr__(self):
        return (
            f"Journal(name={self.name!r}, onecol={self.onecol}, "
            f"twocol={self.twocol}, mplstyle={self.mplstyle!r})"
        )