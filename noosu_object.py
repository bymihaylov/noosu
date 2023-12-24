import config
import parse_beatmap
from timing_point import TimingPoint
from hit_object import HitObject
import numpy as np

class NoosuObject:
    def __init__(self, general: dict, metadata: dict, difficulty: dict, timing_points: list, hit_objects: list) -> None:
        self._general = general
        self._metadata = metadata
        self._difficulty = difficulty

        # self.events = {}

        # numpy array instead of a list?
        self._timing_points: np.array = np.array(object=TimingPoint, *timing_points)
        self._hit_objects: np.array = np.array(object=HitObject, *hit_objects)

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