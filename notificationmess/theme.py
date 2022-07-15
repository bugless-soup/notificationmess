import json
import os.path

from notificationmess.graphics import Gif, Frame
from notificationmess.graphics.shapes.square import Square


class Theme:
    def __init__(self, config_file: str):
        config: dict = json.load(open(config_file))
        self.gif = Gif.from_file(os.path.join(os.path.dirname(config_file), config["gif"]))
        self.duration = config["duration"] if "duration" in config else None
        self.font = config["font"]
        self.zones = [Square(row) for row in config["zones"]]
        self.size = [0, 0]
        for zone in self.zones:
            square, _ = zone.get_transform_no_scale()
            if square.size[0] > self.size[0]:
                self.size[0] = square.size[0]
            if square.size[1] > self.size[1]:
                self.size[1] = square.size[1]

    def generate(self, text: str):
        return self.gif.paste(
            Frame.from_text(text, (self.size[0], self.size[1]), self.font), self.zones
        ).to_widget(self.duration)
