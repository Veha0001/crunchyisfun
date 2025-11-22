"""
Tool to customize Crunchyroll app theme colors by modifying drawable XML files.
"""

import os
import re
from pathlib import Path

import typer

app = typer.Typer(
    add_completion=False, context_settings={"help_option_names": ["-h", "--help"]}
)
color_draw = {
    "#ff5e00": "#ffffff",
    "#ff640a": "#6200ee",
    "#f58220": "#3700b3",
    "#ffc94d": "#6e00ee",
    "#f57421": "#370bba",  # star rating color
}

color_value = {
    "#ff5e00": "#5a0bb6",
    "#ff640a": "#6e00ee",
    "#f7573e": "#6200ee",
    # "#fab818": "#3700b3", # Honey gold (Premium tab)
    "#ef4323": "#370bbb",  # Red Orange
    "#d9ef4323": "#d9370bbb",  # 85 of red orange
    "#23252b": "#1a1a2e",
    "#213944": "#11111b",
    "#202020": "#202025",
    "#ff6750a4": "#3700b3a5",
    # NOTE: First two digits after # are fake.
    "#fff47521": "#ff6200ee",
    "#99ff640a": "#993700b3",  # seek bar watching
    "#59595b": "#c8b6ff",  # tap hover
}


def update_colors(resdir: Path, draw: bool = True, val: bool = True):
    """
    Customize theme colors in drawable and values XML files.
    """

    def process_folder(folder: str, replacements: dict, label: str):
        if not os.path.isdir(folder):
            return
        for root, _, files in os.walk(folder):
            for name in files:
                if name.endswith(".xml"):
                    path = os.path.join(root, name)
                    with open(path, "r", encoding="utf-8") as f:
                        text = f.read()

                    for old, new in replacements.items():
                        text = re.sub(re.escape(old), new, text, flags=re.IGNORECASE)

                    with open(path, "w", encoding="utf-8") as f:
                        f.write(text)

                    print(f"Updated {label}:", path)

    if not draw:
        process_folder(os.path.join(resdir, "drawable"), color_draw, "drawable")
        for draw_dir in Path(resdir).glob("drawable-*"):
            if draw_dir.is_dir():
                process_folder(str(draw_dir), color_draw, "drawable")

    if not val:
        process_folder(os.path.join(resdir, "values"), color_value, "values")
        for val_dir in Path(resdir).glob("values-*"):
            if val_dir.is_dir():
                process_folder(str(val_dir), color_value, "values")


def update_lazyout_home_maskw(resdir: Path):
    """
    Customize Lazyout mask color in drawable XML files.
    Converts @drawable/cr_logo_mark → @drawable/cr_logo_mark_white
    Only in home*.xml files.
    """

    # regex:
    # @drawable/cr_logo_mark  (but NOT ..._white)
    pattern = re.compile(r"@drawable/cr_logo_mark(?!_white)\b", re.IGNORECASE)

    def process_dir(directory):
        if not os.path.isdir(directory):
            return
        for root, _, files in os.walk(directory):
            for name in files:
                if name.endswith(".xml") and "home" in name.lower():
                    path = os.path.join(root, name)
                    with open(path, "r", encoding="utf-8") as f:
                        text = f.read()

                    new_text = pattern.sub("@drawable/cr_logo_mark_white", text)

                    if new_text != text:
                        with open(path, "w", encoding="utf-8") as f:
                            f.write(new_text)
                        print("Updated Lazyout mask:", path)

    process_dir(os.path.join(resdir, "layout"))
    process_dir(os.path.join(resdir, "layout-sw600dp"))


@app.command()
def main(
    resdir: Path = typer.Argument(
        None,
        file_okay=False,
        metavar="<dir>",
        help="Path to the 'res' directory of the Crunchyroll APK.",
    ),
    # -w --maskw
    maskw: bool = typer.Option(
        False,
        "--maskw",
        "-w",
        help="Update Lazyout home mask to white logo.",
    ),
    nd: bool = typer.Option(
        False,
        "-nd/--no-draw",
        help="Update drawable colors.",
    ),
    nv: bool = typer.Option(
        False,
        "-nv/--no-val",
        help="Update values colors.",
    ),
):
    """Update Crunchyroll theme colors in drawable XML files."""
    baseres = os.environ.get("BASE_RESDIR", None)
    if baseres:
        resdir = Path(baseres)
    if resdir is None or not resdir.exists():
        typer.echo("Error: oops! 'res' directory not found.", err=True)
        raise typer.Exit(code=1)
    if maskw:
        update_lazyout_home_maskw(resdir)
    update_colors(resdir, draw=nd, val=nv)


if __name__ == "__main__":
    app()
