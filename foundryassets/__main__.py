from os import walk, rename, remove
from os.path import join, basename
from glob import glob
from pathlib import Path
from subprocess import run
import re
from rich.progress import track
import click

FOUNDRY_DATA = Path(__file__).parent

TOKENS_ROOT = FOUNDRY_DATA / "maps"
MAPS_ROOT = FOUNDRY_DATA / "maps"

cli = click.Group(name="foundryassets")

def apply_naming_conventions(name):
    name_without_spaces = re.sub(r'\s|\_', '-', name.lower())
    name_without_metadata = name_without_spaces.replace("gridless", "").replace("grid", "")
    if name_without_metadata.endswith("-"):
        name_without_metadata = name_without_metadata[:-1]
    return name_without_metadata

@cli.group(name="maps")
def maps_cmd():
    ...

@maps_cmd.command()
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

@cli.group(name="tokens")
def tokens_cmd():
    ...

@tokens_cmd.command(name="rename")
def rename_tokens():
    extensions = ('*.png', '*.jpg')
    tokens = [
        path 
        for ext in extensions
        for path in Path(TOKENS_ROOT).rglob(ext)
    ]

    for token in track(tokens, description="Renaming tokens"):
        ext = "".join(token.suffixes)
        normalized_token_name = apply_naming_conventions(token.name.removesuffix(ext))
        try:
            rename(token, token.parent / f"{normalized_token_name}{ext}")
        except FileExistsError:
            print(f"{token} already exists")


@tokens_cmd.command()
def convert_to_webp():
    extensions = ('*.png', '*.jpg')
    tokens = [
        path 
        for ext in extensions
        for path in Path(TOKENS_ROOT).rglob(ext)
    ]
    for token in track(tokens, description="Renaming tokens"):
        ext = "".join(token.suffixes)
        normalized_token_name = apply_naming_conventions(token.name.removesuffix(ext))
        run(["cwebp", "-m", "6", "-q", "100", token, "-o", token.parent / f"{normalized_token_name}.webp"])
        remove(token)

if __name__ == "__main__":
    cli()
