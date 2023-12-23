import config
from hit_object import HitObject
from timing_point import TimingPoint
from song_object import SongObj
import zipfile
from pathlib import Path
from collections.abc import Iterable

def uncompress_archive(src_path: str) -> None:
    with zipfile.ZipFile(src_path, "r") as zip_ref:
        path = Path(config.assets_dir, src_path.stem)
        zip_ref.extractall(path=path) 
        zip_ref.extract

def parse_osu_file(src_path: str) -> SongObj:
    with open(src_path, "r") as osu_file:
        content = osu_file.read()
    
    sections = [section.strip() for section in content.split("\n\n") if section.strip()]
    general: dict = parse_general(filter(lambda x: x.startswith("[General]"), sections))
    metadata: dict = parse_metadata(filter(lambda x: x.startswith("[Metadata]"), sections))
    difficulty: dict = parse_difficulty(filter(lambda x: x.startswith("[Difficulty]"), sections))
    #parse timing_point & hit_object

    #return SongObj(general, metadata, difficulty, timing_points_lst=, hit_objects_lst=)

def parse_general(content: Iterable) -> dict:
    for i in content:
        print(f"{i=}")

def parse_metadata(content: Iterable) -> dict:
    pass

def parse_difficulty(content: Iterable) -> dict:
    pass

def parse_timing(content: Iterable) -> TimingPoint:
    """
    Timing point syntax: time,beatLength,meter,sampleSet,sampleIndex,volume,uninherited,effects
    
    time (Integer) - Start time of the timing section, in milliseconds from the beginning of the beatmap's audio. The end of the timing section is the next timing point's time (or never, if this is the last timing point).
    
    beatLength (Decimal) - For uninherited timing points, the duration of a beat, in milliseconds.
                         - For inherited timing points, a negative inverse slider velocity multiplier, as a percentage. For example, -50 would make all sliders in this timing section twice as fast as SliderMultiplier
    
    meter (Integer): Amount of beats in a measure. Inherited timing points ignore this property.
    
    sampleSet (Integer): Default sample set for hit objects (0 = beatmap default, 1 = normal, 2 = soft, 3 = drum)
    
    sampleIndex (Integer): Custom sample index for hit objects. 0 indicates osu!'s default hitsounds.
    
    volume (Integer): Volume percentage for hit objects.
    
    uninherited (0 or 1): Whether or not the timing point is uninherited.
    
    effects (Integer): Bit flags that give the timing point extra effects.

    ------
    source: https://osu.ppy.sh/wiki/en/Client/File_formats/osu_%28file_format%29
    """

def parse_hit_object(content: Iterable) -> HitObject:
    """
    Hit object syntax: x,y,time,type,hitSound,objectParams,hitSample

    x (Integer) and y (Integer): Position in osu! pixels of the object.

    time (Integer): Time when the object is to be hit, in milliseconds from the beginning of the beatmap's audio.

    type (Integer): Bit flags indicating the type of the object. See the type section.

    hitSound (Integer): Bit flags indicating the hitsound applied to the object. See the hitsound section.

    objectParams (Comma-separated list): Extra parameters specific to the object's type.

    hitSample (Colon-separated list): Information about which samples are played when the object is hit. It is closely related to hitSound; see the hitsounds section. If it is not written, it defaults to 0:0:0:0:.

    -----
    source: https://osu.ppy.sh/wiki/en/Client/File_formats/osu_%28file_format%29
    """
