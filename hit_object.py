import enum
from typing import Any

class HitObject:
    def __init__(self, x: int, y: int, time: int, type: enum.IntFlag, hitSound: enum.IntFlag, objectParams: list[Any], hitSample: str) -> None:
        self._x = x
        self._y = y
        self._time = time
        self._type = type
        self._hitSound = hitSound
        self._objectParams = objectParams
        self._hitSample = hitSample

    @property
    def x(self) -> int:
        return self._x

    @property
    def y(self) -> int:
        return self._y

    @property
    def time(self) -> int:
        return self._time

    @property
    def type(self) -> enum.IntFlag:
        return self._type

    @property
    def hitSound(self) -> enum.IntFlag:
        return self._hitSound

    @property
    def objectParams(self) -> list[Any]:
        return self._objectParams

    @property
    def hitSample(self) -> str:
        return self._hitSample
