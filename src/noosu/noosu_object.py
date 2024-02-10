from pathlib import Path

from src.noosu.timing_point import TimingPoint
from src.noosu.hit_object import HitObject
import numpy as np


class NoosuObject:
    def __init__(self, general: dict, metadata: dict, difficulty: dict, timing_points: list[TimingPoint],
                 hit_objects: list[HitObject], img_path: Path | None) -> None:
        self._general = general
        self._metadata = metadata
        self._difficulty = difficulty

        # self.events = {}

        self._timing_points: np.array = np.array(timing_points)
        self._hit_objects: np.array = np.array(hit_objects)

        self.image_path: Path | None = img_path

    @property
    def general(self):
        return self._general

    @property
    def metadata(self):
        return self._metadata

    @property
    def difficulty(self):
        return self._difficulty

    @property
    def timing_points(self):
        return self._timing_points

    @property
    def hit_objects(self):
        return self._hit_objects
