import config
import parse_beatmap
from timing_point import TimingPoint
from hit_object import HitObject

class SongObj:
    def __init__(self, general: dict, metadata: dict, difficulty: dict, timing_points_lst: list, hit_objects_lst: list) -> None:
        self.general = {
            "audio_filename": "audio.mp3",
            "audio_lead_in": 0,
            "preview_time": 136460,
            "countdown": 0,  # Not sure what it is for, but sounds useful
            "widescreen_storyboard": 1  # Not sure what it is for, but sounds useful
        }
        
        self.metadata = {
            "title_unicode": "Title Unicode",
            "artist_unicode": "Artist Unicode",
            "creator": "Creator"
        }  # For future maybe add tags

        self.difficulty = {
            "hp_drain_rate": 3,
            "circle_size": 3.2,
            "overall_difficulty": 3,
            "approach_rate": 4.5,
            "slider_multiplier": 1.3,
            "slider_tick_rate": 1
        }

        # self.events = {}

        # numpy array instead of a list?
        self.timing_points_lst: list[TimingPoint]
        self.hit_objects_lst: list[HitObject]
