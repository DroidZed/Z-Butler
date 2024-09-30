from PIL import Image, ImageDraw, ImageFont
from PIL.ImageFont import FreeTypeFont


def _create_font(font_name: str, font_size: int = 87) -> FreeTypeFont:
    return ImageFont.truetype(font=font_name, size=font_size, encoding="utf-8")


def _update_text_and_offset(text: str, offset: int) -> tuple[str, int]:
    name_length = len(text)

    if name_length >= 18:
        offset += 150

    return text, offset


# TODO: remove the discriminator once the new username thing rolls out... Thanks discord 🤡
def create_welcome_image(username: str):
    with Image.open("./assets/img/bg.png") as i:
        text, offset = _update_text_and_offset(f"{username}", 200)

        font = _create_font(
            "./assets/fonts/CabinSketch-Regular.ttf",
            font_size=70 if len(text) > 18 else 100,
        )

        x_coordinate, y_coordinate = (i.size[0] // 2) - offset, 700

        draw = ImageDraw.Draw(i)

        # shadow text
        draw.multiline_text(
            xy=(x_coordinate + 1, y_coordinate + 1),
            text=text,
            fill="black",
            font=font,
            stroke_width=5,
            align="center",
            spacing=5,
        )

        # white text
        draw.multiline_text(
            xy=(x_coordinate, y_coordinate),
            text=text,
            fill="white",
            font=font,
            stroke_width=1,
            align="center",
            spacing=5,
        )

    return i
