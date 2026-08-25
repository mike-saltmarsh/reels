import json
from os import PathLike
from pathlib import Path
from typing import TypeVar
from jinja2 import Environment, FileSystemLoader
from pydantic import BaseModel
import yaml

from scripts.utils import Reel

T = TypeVar("T", bound=BaseModel)


def _load_yaml(file_path: PathLike):
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"YAML file missing at: {path.absolute()}")
    with path.open("r", encoding="utf-8") as file:
        raw_data = yaml.safe_load(file) or {}
    return raw_data


def _parse_reels_data(o):
    reels: list[Reel] = []
    for _, skill_category in o["skills"].items():
        for _, skill in skill_category.items():
            if skill is None or "reels" not in skill:
                continue
            for reel in skill["reels"]:
                reels.append(Reel(**reel))

    return reels


def load_reels(file_path: PathLike):
    reels_data = _load_yaml(file_path)
    reels = _parse_reels_data(reels_data)
    return reels


def fill_template(reels: list[Reel], template_to_use: str):
    templates_dir = Path(__file__).parent.parent / "assets" / "templates"
    file_loader = FileSystemLoader(templates_dir)
    env = Environment(loader=file_loader, trim_blocks=True, lstrip_blocks=True)
    template = env.get_template(template_to_use)
    output = template.render({"reels": reels})
    return output


if __name__ == "__main__":
    root = Path(__file__).parent.parent
    yaml_path = root / "assets" / "reels.yml"
    reels = load_reels(yaml_path)

    t = fill_template(reels, "SMR_Recorded_Media.lua.j2")

    lua_path = (
        root
        / "build/Contents/mods/Reels/42.19/media/lua/shared/RecordedMedia/SMR_Recorded_Media.lua"
    )
    with open(lua_path, "w", encoding="utf-8") as file:
        file.write(t)

    translations: dict[str, str] = {}
    for reel in reels:
        translations[reel.itemDisplayName.key] = reel.itemDisplayName
        translations[reel.title.key] = reel.title
        translations[reel.subtitle.key] = reel.subtitle
        for line in reel.lines:
            translations[line.text.key] = line.formatted_text

    translations_path = (
        root
        / "build/Contents/mods/Reels/42.19/media/lua/shared/Translate/EN/Recorded_Media.json"
    )

    with open(translations_path, "w", encoding="utf-8") as file:
        json.dump(translations, file, indent=2)
