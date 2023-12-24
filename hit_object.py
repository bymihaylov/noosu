import enum
from typing import Any

class HitObject:
    def __init__(self, x: int, y: int, time: int, type: enum.IntFlag, hitSound: enum.IntFlag, objectParams: list[Any], hitSample: str) -> None:
        self.__pos: tuple[int, int] = x, y
        self._time = time
        self._type = type
        self._hitSound = hitSound
        self._objectParams = objectParams
        self._hitSample = hitSample

    @property
    def x(self) -> int:
        return self.__pos[0]

    @property
    def y(self) -> int:
        return self.__pos[1]
    
    @property
    def xy_position(self) -> tuple(int, int):
        return self.__pos

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
