from enum import IntFlag


class TimingPointEffects(IntFlag):
    KIAI_TIME_ENABLED = 1  # Bit 0
    OMIT_FIRST_BARLINE = 8  # Bit 3


class HitObjectType(IntFlag):
    HIT_CIRCLE = 1  # Bit 0
    SLIDER = 2  # Bit 1
    NEW_COMBO = 4  # Bit 2
    SPINNER = 8  # Bit 3
    COLOR_HAX_MASK = 112  # Bits 4, 5, 6
    MANIA_HOLD_NOTE = 128  # Bit 7


class HitSoundsType(IntFlag):
    NORMAL = 1  # Bit 0
    WHISTLE = 2  # Bit 1
    FINISH = 4  # Bit 2
    CLAP = 8  # Bit 3


