from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from pathlib import Path


def _create_font(font_name: str) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(
        font=font_name,
        size=87,
        encoding='utf-8'
    )


def create_picture(username: str, discriminator: str) -> Image:

    img_dir = Path("./assets/welcome_images/")
    welcome_img_path = img_dir / f"{username}-welcome.png"

    text = f'{username}#{discriminator}'
    font = _create_font("./assets/fonts/CabinSketch-Regular.ttf")

    with Image.open('./assets/img/bg.png') as i:

        x, y = (i.size[0]//2)-260, 700
        draw = ImageDraw.Draw(i)

        if (len(text.split('#')[0]) > 8):
            text = text.replace('#', '\n#')

        # shadow text
        draw.multiline_text(
            xy=(x+1, y+1),
            text=text,
            fill="black",
            font=font,
            stroke_width=5,
            align="center",
            spacing=5,
        )

        # white text
        draw.multiline_text(
            xy=(x, y),
            text=text,
            fill="white",
            font=font,
            stroke_width=1,
            align="center",
            spacing=5,
        )

    return i
