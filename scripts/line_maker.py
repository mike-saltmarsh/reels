"""
A helper script to make it easier to work with
script in the yaml file. Just throw in some lines,
do not forget the series title and skill being leveled up.
Launch it and it will print out text you can copypaste to the yaml.
"""

d = """"""


TITLE = ""
SKILL = ""

orig_lines = d.split("\n")
orig_lines = [el for el in orig_lines if el != ""]


def populate_lines(step):
    lines = []
    bonus_count = 0

    for idx, line in enumerate(orig_lines):
        if idx == 0:
            lines.append(f"        - text: {TITLE}!")
            lines.append("          icon: music")
        lines.append(f"        - text: {line}")
        if (idx - 1) % step == 0:
            bonus_count += 1
            lines.append("          codes:")
            lines.append(f"          - {SKILL}+1")
            lines.append("          - BOR-1")
        if idx == len(orig_lines) - 1:
            lines.append(f"        - text: {TITLE}!")
            lines.append("          icon: music")
    if bonus_count < 5:
        raise Exception(f"Script too short. Line count: {len(orig_lines)}")
    return lines


try:
    lines = populate_lines(4)
except Exception:
    try:
        lines = populate_lines(3)
    except Exception:
        lines = populate_lines(2)

print("\n".join(lines))
