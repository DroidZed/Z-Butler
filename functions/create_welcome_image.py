from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw


def _create_font(font_name: str) -> ImageFont.FreeTypeFont:

    return ImageFont.truetype(
        font=font_name,
        size=87,
        encoding='utf-8'
    )


def create_picture(username: str, discriminator: str) -> Image:

    with Image.open('./assets/img/bg.png') as i:

        font = _create_font("./assets/fonts/CabinSketch-Regular.ttf")

        text = _update_text_and_offset(f'{username}#{discriminator}', 305)[0]

        offset = _update_text_and_offset(f'{username}#{discriminator}', 305)[1]

        x, y = (i.size[0] // 2) - offset, 700

        draw = ImageDraw.Draw(i)

        # shadow text
        draw.multiline_text(
            xy=(x + 1, y + 1),
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


def _update_text_and_offset(text: str, offset: int) -> tuple:

    name_length = len(text.split('#')[0])

    if name_length >= 18:
        offset += 65

    if name_length > 8:
        text = text.replace('#', '\n#')

    return (text, offset)