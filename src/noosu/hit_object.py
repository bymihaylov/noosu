

class HitObject:
    def __init__(self, x: int, y: int, time: int, obj_type: int, hit_sound: int, object_params: list[str], hit_sample: str) -> None:
        self.__pos: tuple[int, int] = x, y
        self._time = time
        self._type = obj_type
        self._hit_sound = hit_sound
        self._object_params = object_params
        self._hit_sample = hit_sample

    @property
    def x(self) -> int:
        return self.__pos[0]

    @property
    def y(self) -> int:
        return self.__pos[1]
    
    @property
    def xy_position(self) -> tuple[int, int]:
        return self.__pos

    @property
    def time(self) -> int:
        return self._time

    @property
    def type(self) -> int:
        return self._type

    @property
    def hitSound(self) -> int:
        return self._hit_sound

    @property
    def objectParams(self) -> list[str]:
        return self._object_params

    @property
    def hitSample(self) -> str:
        return self._hit_sample
