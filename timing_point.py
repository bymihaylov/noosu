from bit_flags import TimingPointEffects

class TimingPoint():
    def __init__(self, time: int, beat_len: float, meter: int, sample_set: int, sample_index: int, volume: int, uninherited: bool, effects: TimingPointEffects):
        self._time = time
        self._beat_len = beat_len
        self._meter = meter
        self._sample_set = sample_set
        self._sample_index = sample_index
        self._volume = volume
        self._uninherited = uninherited
        self._effects = effects

    @property
    def time(self) -> int:
        return self._time

    @property
    def beat_len(self) -> float:
        return self._beat_len

    @property
    def meter(self) -> int:
        return self._meter

    @property
    def sample_set(self) -> int:
        return self._sample_set

    @property
    def sample_index(self) -> int:
        return self._sample_index

    @property
    def volume(self) -> int:
        return self._volume

    @property
    def uninherited(self) -> bool:
        return self._uninherited

    @property
    def effects(self) -> TimingPointEffects:
        return self._effects
