from io import BytesIO
from string import ascii_letters

import PIL.Image
from PIL import ImageFont, ImageDraw
from PIL.Image import Image

from notificationmess.graphics import Widget
from notificationmess.graphics.shapes import Vector2D
from notificationmess.graphics.shapes.square import Square
from notificationmess.graphics.shapes.transform import Transform
from notificationmess.graphics.shapes.transformable import Transformable


def from_file(filename: str):
    return Frame(PIL.Image.open(filename))


def format_text(text: str, width: int):
    lines = []
    for line in text.splitlines():
        current = ""
        for word in line.split(' '):
            word = word + " "
            if len(current) + len(word) >= width:
                lines.append(current)
                current = word
            else:
                current += word
        if current != "":
            lines.append(current)
    return "\n".join(lines)


def from_text(text: str, size: Vector2D, font_file: str) -> 'Frame':
    size = (round(size[0]), round(size[1]))
    font = None
    font_size = 30
    current_size = None
    current_text = None
    while (current_size is None or current_size[0] > size[0] or current_size[1] > size[1]) and font_size > 0:
        font = ImageFont.truetype(font_file, font_size)
        avg_char = sum(font.getsize(c)[0] for c in ascii_letters) / len(ascii_letters)
        current_text = format_text(text, int(size[0] / avg_char))
        current_size = font.getsize_multiline(current_text)
        font_size -= 1
    frame = PIL.Image.new("RGBA", size, (255, 255, 255, 0))
    ImageDraw.Draw(frame).multiline_text((0, 0), current_text, "#000", font)
    return Frame(frame, size)


class Frame(Transformable):
    def __init__(self, image: Image, size: Vector2D = None):
        super().__init__(size or image.size)
        self.image = image

    def apply(self, transform: Transform, final_size: Vector2D = None) -> 'Frame':
        return Frame(self.image.transform(
            (int(final_size[0]), int(final_size[1])) if final_size is not None else self.size,
            PIL.Image.AFFINE,
            transform.to_pil_data(),
            PIL.Image.BILINEAR
        ))

    def transform(self, square: Square):
        return self.apply(square.get_transform(self.size), square.size)

    def paste(self, other: 'Frame', zone: Square = None):
        frame = self.image.copy()
        if zone is None:
            img = other.image
        else:
            img = other.transform(zone).image
        frame.paste(img, mask=img)
        return Frame(frame)

    def to_widget(self):
        wrap = BytesIO()
        self.image.save(wrap, format="PNG")
        return Widget.from_bytes(wrap.getvalue(), self.size)
