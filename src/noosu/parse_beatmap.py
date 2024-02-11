from src.config import config
from src.noosu.hit_object import HitObject
from src.noosu.timing_point import TimingPoint
from src.noosu.noosu_object import NoosuObject
import zipfile
from pathlib import Path


def uncompress_archive(src_path: str) -> None:
    with zipfile.ZipFile(src_path, "r") as zip_ref:
        path = config.assets_dir / Path(src_path).stem
        zip_ref.extractall(path=path)


def parse_osu_file(src_path: str | Path) -> NoosuObject:
    with open(src_path, "r") as osu_file:
        content = osu_file.read()

    src_dir_path = Path(src_path).parent

    sections = [section.strip() for section in content.split("\n\n") if section.strip()]
    osu_file_content = {section.split('\n')[0]: section for section in sections if section.startswith("[")}

    general: dict = parse_general(osu_file_content["[General]"], src_dir_path)
    metadata: dict = parse_metadata(osu_file_content["[Metadata]"])
    difficulty: dict = parse_difficulty(osu_file_content["[Difficulty]"])

    timing_points: list[TimingPoint] = parse_timing(osu_file_content["[TimingPoints]"])
    hit_objects: list[HitObject] = parse_hit_object(osu_file_content["[HitObjects]"])

    image_path: Path | None = parse_events_to_get_img_path(osu_file_content["[Events]"], src_dir_path)

    return NoosuObject(general, metadata, difficulty, timing_points, hit_objects, image_path)


def extract_to_dict(content: str, include_fields: tuple) -> dict[str, str]:
    """
    Extracts key-value pairs from the given content based on the specified include fields.

    Parameters:
        content (str): The content to extract key-value pairs from.
        include_fields (tuple): A tuple of field names to include in the result.

    Returns:
        dict[str, str]: A dictionary containing key-value pairs extracted from the content.
    """

    lines = content.split('\n')
    return {key: val for line in lines if line.startswith(include_fields) for key, val in
            [map(str.strip, line.split(':', 1))]}


def cast_val_to_int(data: dict, key: str) -> None:
    data[key] = int(data[key])


def cast_val_to_float(data: dict, key: str) -> None:
    data[key] = float(data[key])


def parse_general(content: str, src_dir_path: str | Path) -> dict:
    include_fields = ("AudioFilename", "AudioLeadIn", "PreviewTime")
    data: dict[str, str] = extract_to_dict(content, include_fields)

    data["AudioFilename"] = src_dir_path / data["AudioFilename"]

    cast_val_to_int(data, "AudioLeadIn")
    cast_val_to_int(data, "PreviewTime")
    if data["PreviewTime"] < 0:
        data["PreviewTime"] = 0
    return data


def parse_metadata(content: str) -> dict:
    include_fields = ("TitleUnicode", "ArtistUnicode", "Creator")
    return extract_to_dict(content, include_fields)


def parse_difficulty(content: str) -> dict:
    include_fields = (
        "HPDrainRate", "CircleSize", "OverallDifficulty", "ApproachRate", "SliderMultiplier", "SliderTickRate")
    data = extract_to_dict(content, include_fields)
    [cast_val_to_float(data=data, key=key) for key in include_fields]
    return data


def parse_timing(content: str) -> list[TimingPoint]:
    lines = content.split("\n")
    return [parse_timing_line(line) for line in lines[1:]]


def parse_timing_line(line: str) -> TimingPoint:
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
    time, beat_len, meter, sample_set, sample_index, volume, uninherited, effect = map(
        lambda x: int(x) if x.isdigit() else float(x),
        line.split(',')
    )
    uninherited = bool(uninherited)

    return TimingPoint(time, beat_len, meter, sample_set, sample_index, volume, uninherited, effect)


def parse_hit_object_line(line: str) -> HitObject:
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

    x, y, time, obj_type, hit_sound, *obj_params, hit_sample = map(str, line.split(','))
    x, y, time, obj_type, hit_sound = map(int, [x, y, time, obj_type, hit_sound])  # Cast to int

    return HitObject(x, y, time, obj_type, hit_sound, obj_params, hit_sample)


def parse_hit_object(content: str) -> list[HitObject]:
    lines = content.split("\n")
    return [parse_hit_object_line(line) for line in lines[1:]]


"""
Example:
[Events]
//Background and Video events
0,0,"CRAB RAVE BG.png",0,0
...

We need CRAB RAVE BG.png
"""


def parse_events_to_get_img_path(content: str, src_dir_path: str | Path) -> Path | None:
    # Find the index of the first occurrence of double quotes
    start_index = content.find('"')

    # Find the index of the second occurrence of double quotes
    end_index = content.find('"', start_index + 1)

    # Extract the image path between the double quotes
    if start_index != -1 and end_index != -1:
        filename = content[start_index + 1:end_index]
        return src_dir_path / filename
    else:
        return None
