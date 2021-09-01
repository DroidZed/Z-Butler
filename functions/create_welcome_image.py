from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from discord import File
from pathlib import Path


def _create_font(font_name: str) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(
        font=font_name,
        size=87,
        encoding='utf-8'
    )


def create_picture(username: str) -> File:

    img_dir = Path("./assets/welcome_images/")
    welcome_img_path = img_dir / f"{username}-welcome.png"

    text = username
    font = _create_font("./assets/fonts/CabinSketch-Regular.ttf")
    x, y = 201, 700
    with Image.open('./assets/img/bg.png') as i:

        draw = ImageDraw.Draw(i)

        # shadow text
        draw.text(
            xy=(x + 1, y + 1),
            text=text,
            fill="black",
            font=font,
            stroke_width=1
        )
        # white text
        draw.text(
            xy=(x, y),
            text=text,
            fill="white",
            font=font,
            stroke_width=1
        )

        i.save(welcome_img_path)

    return File(fp=welcome_img_path, filename=f'{username}-welcome.png')
