import json
from pathlib import Path

from pydantic import ValidationError
import yaml

import pytest

from scripts.utils import Color, Icon, LineColorRGB, Reel, ReelCategory, TapeLine, _
import re


@pytest.fixture
def rgb() -> dict[str, int]:
    return {"r": 0, "g": 0, "b": 0}


class TestTranslateableString:
    def test_md5_signature(self):
        o = _()

        result = o.md5

        assert re.match(r"^[0-9a-f]{32}$", result)

    @pytest.mark.parametrize(
        "test_str, expected_hash",
        [
            ("", "d41d8cd98f00b204e9800998ecf8427e"),
            ("whatever", "008c5926ca861023c1d2a36653fd88e2"),
        ],
    )
    def test_md5(self, test_str, expected_hash):
        o = _(test_str)

        result = o.md5

        assert result == expected_hash

    @pytest.mark.parametrize(
        "test_str, expected_result",
        [
            ("", "RM_d41d8cd98f00b204e9800998ecf8427e"),
            ("whatever", "RM_008c5926ca861023c1d2a36653fd88e2"),
        ],
    )
    def test_formatted_hash(self, test_str, expected_result):
        o = _(test_str)

        assert o.key == expected_result


class TestTapeLine:
    @pytest.fixture
    def o(self) -> TapeLine:
        return TapeLine(text=_("whatever"))

    def test_color(self):
        o = TapeLine(text="")

        assert hasattr(o, "color")

    def test_default_values(self):
        c = Color()

        assert c.r == 1.0
        assert c.g == 1.0
        assert c.b == 1.0

    @pytest.mark.parametrize("test_value", [-0.1, 1.1])
    @pytest.mark.parametrize("field", ["r", "g", "b"])
    def test_rgb_boundaries_errors(self, test_value, field):
        with pytest.raises(ValidationError):
            c = Color(**{field: test_value})
            assert c

    def test_text(self, o):
        assert hasattr(o, "text")
        # RM_ + md5 of 'text'
        assert o.text.key == "RM_008c5926ca861023c1d2a36653fd88e2"

    def test_no_codes_defaults_to_empty_list(self, o: TapeLine):
        assert o.codes == []

    def test_codes_creation(self):
        TapeLine(text=_("whatever"), codes=[("BOR", -1), ("ELC", 1)])

    def test_codes_format(self):
        o = TapeLine(text=_("whatever"), codes=[("BOR", -1), ("ELC", 1)])

        assert o.formatted_codes in ["BOR-1,ELC+1", "ELC+1,BOR-1"]

    def test_no_icon_by_default(self):
        o = TapeLine(text=_(""))

        assert not o.icon

    def test_no_icon_info_in_formatted(self, o: TapeLine):
        assert o.text == "whatever"
        assert "[img=music]" not in o.text

    def test_icon_info_in_formatted(self):
        o = TapeLine(
            text=_("whatever"),
            icon=Icon.MUSIC,
        )
        assert o.formatted_text.startswith("[img=music] ")
        assert o.formatted_text.endswith(" [img=music]")

    def test_default_color(self):
        o = TapeLine()

        assert o.color.r == 1.0
        assert o.color.g == 1.0
        assert o.color.b == 1.0

    @pytest.mark.parametrize("test_color", ["magenta", None])
    def test_error_on_wrong_color(self, test_color):
        with pytest.raises(Exception):
            TapeLine(color=test_color)

    @pytest.mark.parametrize("test_color", ["green", Color(r=1, g=1, b=1)])
    def test_color(self, test_color):
        TapeLine(color=test_color)


class TestReel:
    @pytest.fixture
    def r(self):
        return Reel(
            key="Whatever key",
            title="Whatever title",
            subtitle="Whatever subtitle",
            itemDisplayName="Whatever itemDisplayName",
        )

    def test_init(self, r):
        for field in [
            "key",
            "itemDisplayName",
            "title",
            "subtitle",
            "category",
            "lines",
        ]:
            assert hasattr(r, field)
        assert r.lines == []

    def test_default_category_is_retail(self, r):
        assert r.category == ReelCategory.RETAIL
