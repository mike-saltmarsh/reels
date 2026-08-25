import json
from pathlib import Path

import pytest

from scripts.build import _load_yaml, fill_template, load_reels
from scripts.utils import Reel, TapeLine


@pytest.fixture
def reel_path():
    return Path(__file__).parent / "assets" / "reel.yml"


pytest.mark.skip  # TODO


def test_load_line(reel_path):
    o = _load_yaml(reel_path)

    for reel_data in o:
        for line_data in reel_data["lines"]:
            TapeLine(**line_data)


def test_load_reel(reel_path):
    o = _load_yaml(reel_path)

    for reel_data in o:
        r = Reel(**reel_data)
        assert r


def test_load_whole_data(reel_path):
    yaml_path = reel_path.parent / "reels.yml"

    reels = load_reels(yaml_path)

    assert isinstance(reels, list)
    assert all(isinstance(el, Reel) for el in reels)


class TestTemplates:
    def test_lua(self, reel_path):
        yaml_path = reel_path.parent / "reels.yml"
        reels = load_reels(yaml_path)

        t = fill_template(reels, "SMR_Recorded_Media.lua.j2")

        with open(".sandbox/output.lua", "w", encoding="utf-8") as file:
            file.write(t)

    def test_translations(self, reel_path):
        yaml_path = reel_path.parent / "reels.yml"
        reels = load_reels(yaml_path)
        translations: dict[str, str] = {}
        for reel in reels:
            translations[reel.itemDisplayName.key] = reel.itemDisplayName
            translations[reel.title.key] = reel.title
            translations[reel.subtitle.key] = reel.subtitle
            for line in reel.lines:
                translations[line.text.key] = line.formatted_text

        with open(".sandbox/output.json", "w", encoding="utf-8") as file:
            json.dump(translations, file, indent=2)
