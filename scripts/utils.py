import hashlib
from typing import Annotated, Any, Self
import uuid

from pydantic import BaseModel, BeforeValidator, Field, field_validator, model_validator
from pydantic_core import core_schema
from enum import Enum, StrEnum
from pydantic import BaseModel


class LineColorRGB(Enum):
    WHITE = {"r": 1.0, "g": 1.0, "b": 1.0}  # "#FFFFFF"
    GREEN = {"r": 0.0, "g": 0.69, "b": 0.31}  #  "#00B072"
    BLUE = {"r": 0.0, "g": 0.69, "b": 0.94}  # "#00B0f0"


LineColorHumanizedMapping = {
    "white": LineColorRGB.WHITE,
    "green": LineColorRGB.GREEN,
    "blue": LineColorRGB.BLUE,
}


class CodeAbbr(StrEnum):
    BOREDOM = "BOR"
    HUSBANDRY = "HUS"
    ELECTRICAL = "ELC"
    WELDING = "MTL"
    TAILORING = "TAI"
    MECHANICS = "MEC"
    FIRST_AID = "DOC"
    CARPENTRY = "CRP"
    COOKING = "COO"
    AGRICULTURE = "FRM"
    FISHING = "FIS"
    TRAPPING = "TRA"
    FORAGING = "FOR"

    CARVING = "CRV"


class Icon(StrEnum):
    MUSIC = "music"


def hash_MD5(text) -> str:
    m = hashlib.md5()
    m.update(text.encode("utf-8"))
    return m.hexdigest()


class _(str):
    @property
    def md5(self) -> str:
        return hash_MD5(self)

    @property
    def key(self) -> str:
        return "RM_" + str(self.md5)

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: Any
    ) -> core_schema.CoreSchema:
        return core_schema.no_info_after_validator_function(
            cls, core_schema.str_schema()
        )


def code_data_loader(value: str | tuple[CodeAbbr, int]) -> tuple[CodeAbbr, int]:
    if isinstance(value, str):
        return_value = CodeAbbr(value[:3]), int(value[3:])
    else:
        return_value = value
    return return_value


CodeData = Annotated[tuple[CodeAbbr, int], BeforeValidator(code_data_loader)]

RGBFloat = Annotated[float, Field(1.0, ge=0.0, le=1.0)]


class Color(BaseModel):
    r: float = Field(1.0, ge=0, le=1)
    g: float = Field(1.0, ge=0, le=1)
    b: float = Field(1.0, ge=0, le=1)


class TapeLine(BaseModel):
    color: Color = Color(r=1.0, g=1.0, b=1.0)
    text: _ = _()
    codes: list[CodeData] = []
    icon: Icon | None = None

    @property
    def formatted_codes(self) -> str:
        formatted_codes = []
        for code, value in self.codes:
            sign = "+" if value > 0 else ""
            formatted_codes.append(code + sign + str(value))

        return ",".join(formatted_codes)

    @property
    def formatted_text(self):
        if self.icon:
            text = f"[img={self.icon}] {self.text} [img={self.icon}]"
        else:
            text = self.text
        return text

    @field_validator("color", mode="before")
    @classmethod
    def validate_color(cls, value: str | Color):
        possible_values = LineColorHumanizedMapping.keys()

        if type(value) not in (str, Color):
            raise TypeError("Color must be either str or Color.")

        if isinstance(value, str):
            if value not in possible_values:
                raise ValueError(
                    "Invalid color value. Input must be one of: "
                    + ", ".join(possible_values),
                )
            return LineColorHumanizedMapping[value].value
        elif isinstance(value, Color):
            return value.model_dump()


class ReelCategory(StrEnum):
    RETAIL = "Retail-VHS"


class Reel(BaseModel):
    key: str
    itemDisplayName: _
    title: _
    subtitle: _
    category: ReelCategory = ReelCategory.RETAIL
    lines: list[TapeLine] = []
