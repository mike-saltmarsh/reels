from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


class _Settings(BaseSettings):
    changenote: str
    app_id: int = 108600
    workshop_id: int = 3789896874

    model_config = SettingsConfigDict(
        env_file=Path(__file__).parent.parent / ".env", env_file_encoding="utf-8", extra="ignore"
    )


settings = _Settings()


def main():

    proj_root = Path(__file__).parent.parent
    build_dir = proj_root / "build"
    vdf_content = f""""workshopitem"
{{
  "appid"            "{settings.app_id}"
  "publishedfileid"  "{settings.workshop_id}"
  "contentfolder"    "{build_dir}"
  "previewfile"      "{build_dir / 'preview.png'}"
  "changenote"       "{settings.changenote}"
}}
"""

    output_vdf = proj_root / "build.vdf"
    with open(output_vdf, "w", encoding="utf-8") as f:
        f.write(vdf_content)

    print(f"Success: Generated SteamCMD build configuration at: {output_vdf}")
    print(f"The changenote is: {settings.changenote}")
    print("Now, use 'just upload' to upload it to the workshop")


if __name__ == "__main__":
    main()
