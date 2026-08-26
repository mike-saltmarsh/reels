"""
A helper script to make it easier to work with
script in the yaml file. Just throw in some lines,
do not forget the series title and skill being leveled up.
Launch it and it will print out text you can copypaste to the yaml.
"""

d = """Welcome back to Woodcarving. I am Rick Bütz.
Today we are whittling a classic wooden goblet.
We will carve this from a block of soft basswood.
This project is excellent for practicing tool control.
Draw the goblet profile on all sides of your wood.
Use a sharp detail knife to outline the outer cup.
Carefully hollow out the bowl using a spoon gouge.
Take thin shavings and work slowly from the center.
Always keep your non-carving hand behind the blade.
Next, slice downward to rough out the slender stem.
Relieve the wood gradually to prevent any splitting.
Shape the base with sweeping cuts toward the edge.
Use fine sandpaper to smooth out the final details.
Our beautiful wooden goblet is complete and ready.
Next week, we will carve a rustic wooden whistle.
Keep your knives sharp, be safe, and happy carving.
"""


TITLE = "Woodcarving with Rick Bütz"
SKILL = "CRV"

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
        if idx == len(orig_lines)-1:
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