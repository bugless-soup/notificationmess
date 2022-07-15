from io import BytesIO

import PIL.Image
from PIL import ImageSequence
from PIL.Image import Image

from notificationmess.graphics import Widget
from notificationmess.graphics.Frame import Frame
from notificationmess.graphics.shapes.square import Square


def from_file(filename: str):
    gif = PIL.Image.open(filename)
    dt = 0
    for i in range(gif.n_frames):
        gif.seek(i)
        dt += gif.info['duration']
    return Gif([frame.copy() for frame in ImageSequence.Iterator(gif)], (dt / 1000))


class Gif:
    def __init__(self, frames: list[Image], duration: float):
        self.frames = frames
        self.duration = duration
        self.size = self.frames[0].size

    def paste(self, other: Frame, zones: list[Square]):
        return Gif([
            Frame(frame).paste(other, zones[i]).image
            for i, frame in enumerate(self.frames)
        ], self.duration)

    def to_widget(self, duration: float = None):
        duration = int((duration or self.duration) * 1000 / len(self.frames))
        wrap = BytesIO()
        self.frames[0].save(wrap, format="GIF", save_all=True, background=(0, 0, 0, 0),
                            append_images=self.frames[1:], duration=duration, disposal=3)
        return Widget.from_bytes(wrap.getvalue(), self.size)
