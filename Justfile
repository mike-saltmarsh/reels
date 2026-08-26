project_root := justfile_directory()

launch: redeploy_locally
    steam steam://rungameid/108600

redeploy_locally: build
    #!/usr/bin/env bash
    rm -rf ~/Zomboid/Workshop/reels
    cp -r ~/projects/reels/build ~/Zomboid/Workshop/reels    

test_scripts: format typecheck
    uv run pytest --cov=scripts --cov-report=xml scripts/tests

format:
    uv run black ./scripts/

typecheck:
    uv run ty check

_export_png:

build: format test_scripts
    #!/usr/bin/env bash
    rm -rf {{project_root}}/build/
    mkdir -p {{project_root}}/build/Contents/mods/Reels/common
    mkdir -p {{project_root}}/build/Contents/mods/Reels/42.19/media/lua/shared/RecordedMedia
    mkdir -p {{project_root}}/build/Contents/mods/Reels/42.19/media/lua/shared/Translate/EN
    cp {{project_root}}/assets/mod.info {{project_root}}/build/Contents/mods/Reels/42.19/
    convert {{project_root}}/assets/mod_favicon.xcf -flatten {{project_root}}/build/Contents/mods/Reels/42.19/mod_favicon.png
    convert {{project_root}}/assets/poster.xcf -flatten {{project_root}}/build/Contents/mods/Reels/42.19/poster.png
    convert {{project_root}}/assets/poster.xcf -flatten {{project_root}}/build/preview.png
    uv run python -m scripts.build
    