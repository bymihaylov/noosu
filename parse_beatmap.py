import config
import zipfile
from pathlib import Path

def uncompress_beatmap_to_dest(src_path: str) -> None:
    with zipfile.ZipFile(src_path, "r") as zip_ref:
        path = Path(config.assets_dir, src_path.split('/')[1].split('.')[0])
        zip_ref.extractall(path=path) 
        zip_ref.extract 

