import config
import zipfile
from pathlib import Path

def uncompress_archive(src_path: str) -> None:
    with zipfile.ZipFile(src_path, "r") as zip_ref:
        path = Path(config.assets_dir, src_path.stem)
        zip_ref.extractall(path=path) 
        zip_ref.extract 

