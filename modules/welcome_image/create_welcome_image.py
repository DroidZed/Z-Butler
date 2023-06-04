from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL.ImageFont import FreeTypeFont


def _create_font(font_name: str) -> FreeTypeFont:
    return ImageFont.truetype(
        font=font_name, size=87, encoding="utf-8"
    )


def _update_text_and_offset(
    text: str, offset: int
) -> tuple[str, int]:
    name_length = len(text.split("#")[0])

    if name_length >= 18:
        offset += 65

    if name_length > 8:
        text = text.replace("#", "\n#")

    return text, offset


# TODO: remove the discriminator once the new username thing rolls out... Thanks discord 🤡
def create_welcome_image(username: str, discriminator: str):
    with Image.open("./assets/img/bg.png") as i:
        font = _create_font(
            "./assets/fonts/CabinSketch-Regular.ttf"
        )

        text, offset = _update_text_and_offset(
            f"{username}#{discriminator}", 305
        )

        x_coordinate, y_coordinate = (
            i.size[0] // 2
        ) - offset, 700

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
