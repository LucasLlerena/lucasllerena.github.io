"""Generate og.png (1200x630) for the portfolio's Open Graph card.

Design tokens mirror index.html: charcoal #101010, gold #c2a15c, serif display.
Fonts: Georgia (the declared serif fallback in the site's CSS) + Segoe UI for the
letterspaced sans labels. EB Garamond and Inter are web fonts and are not
installed locally, so the fallback stack is used deliberately.

Run:  python _gen_og.py
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630

BG = (16, 16, 16)
INK = (236, 233, 226)
INK_FAINT = (110, 106, 97)
GOLD = (194, 161, 92)
LINE = (42, 41, 37)

FONTS = "C:/Windows/Fonts/"
serif = ImageFont.truetype(FONTS + "georgia.ttf", 60)
serif_italic = ImageFont.truetype(FONTS + "georgiai.ttf", 60)
sans_label = ImageFont.truetype(FONTS + "seguisb.ttf", 18)
sans_meta = ImageFont.truetype(FONTS + "segoeui.ttf", 19)


def tracked_width(draw, text, font, tracking):
    """Width of text rendered with manual letterspacing."""
    return sum(draw.textlength(c, font=font) for c in text) + tracking * (len(text) - 1)


def draw_tracked(draw, xy, text, font, fill, tracking):
    x, y = xy
    for char in text:
        draw.text((x, y), char, font=font, fill=fill)
        x += draw.textlength(char, font=font) + tracking


def centered(draw, y, text, font, fill, tracking=0):
    if tracking:
        x = (W - tracked_width(draw, text, font, tracking)) / 2
        draw_tracked(draw, (x, y), text, font, fill, tracking)
    else:
        x = (W - draw.textlength(text, font=font)) / 2
        draw.text((x, y), text, font=font, fill=fill)


def sheen_layer():
    """Soft diagonal gold light band, matching the .sheen element on the site."""
    small_w, small_h = 240, 126
    layer = Image.new("RGBA", (small_w, small_h), (0, 0, 0, 0))
    px = layer.load()
    for y in range(small_h):
        for x in range(small_w):
            # distance from a diagonal running bottom-left to top-right
            d = abs((x * 0.86 + y * 0.51) - small_w * 0.52)
            a = max(0.0, 1.0 - d / (small_w * 0.30))
            if a > 0:
                px[x, y] = (214, 178, 106, int(26 * a * a))
    return layer.resize((W, H), Image.LANCZOS)


img = Image.new("RGB", (W, H), BG)
img = Image.alpha_composite(img.convert("RGBA"), sheen_layer()).convert("RGB")
d = ImageDraw.Draw(img)

# hairline frame, same weight as the section rules on the site
d.rectangle([40, 40, W - 41, H - 41], outline=LINE, width=1)

# eyebrow
centered(d, 118, "LUCAS LLERENA · AI PRODUCT ENGINEER", sans_label, GOLD, tracking=5.0)

# short gold rule under the eyebrow
d.line([(W / 2 - 34, 162), (W / 2 + 34, 162)], fill=GOLD, width=1)

# display lines
centered(d, 236, "Software that earns its keep.", serif, INK)
centered(d, 322, "Built end to end.", serif_italic, GOLD)

# footer rule + meta
d.line([(210, 470), (W - 210, 470)], fill=LINE, width=1)
centered(
    d,
    500,
    "Brazil · GMT\u22123     French & Brazilian citizen     EN · FR · PT · ES",
    sans_meta,
    INK_FAINT,
    tracking=1.2,
)

img.save("og.png", "PNG", optimize=True)
print("og.png written:", img.size)
