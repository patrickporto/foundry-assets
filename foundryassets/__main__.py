from os import walk, rename
from os.path import join, basename
from glob import glob
from pathlib import Path
import re
from rich.progress import track
import click

FOUNDRY_DATA = Path(__file__).parent

TOKENS_ROOT = FOUNDRY_DATA / "maps"
MAPS_ROOT = FOUNDRY_DATA / "maps"

cli = click.Group(name="housekeeping")

def apply_naming_conventions(name):
    name_without_spaces = re.sub(r'\s|\_', '-', name.lower())
    name_without_metadata = name_without_spaces.replace("gridless", "").replace("grid", "")
    if name_without_metadata.endswith("-"):
        name_without_metadata = name_without_metadata[:-1]
    return name_without_metadata

@cli.command()
def rename_animated_maps():
    animated_maps = [y for x in walk(MAPS_ROOT) for y in glob(join(x[0], '*.webm'))]

    for map_path in track(animated_maps, description="Renaming maps"):
        map_name, ext = basename(map_path).split(".")
        map_dir = Path(map_path).parent
        normalized_map_name = apply_naming_conventions(map_name)
        try:
            rename(map_path, join(map_dir, f"{normalized_map_name}.{ext}"))
        except FileExistsError:
            print(f"{map_path} already exists")

@cli.command()
def rename_tokens():
    tokens = [y for x in walk(MAPS_ROOT) for y in glob(join(x[0], '*.webm'))]

    for token_path in track(tokens, description="Renaming tokens"):
        token_name, ext = basename(token_path).split(".")
        token_dir = Path(token_path).parent
        normalized_token_name = apply_naming_conventions(token_name)
        try:
            rename(token_path, join(token_dir, f"{normalized_token_name}.{ext}"))
        except FileExistsError:
            print(f"{token_path} already exists")


if __name__ == "__main__":
    cli()
