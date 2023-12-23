import config
import os

class Setup:
    def __init__(self) -> None:
        self.assets_dir: os.PathLike  = config.assets_dir
        self.external_packs: os.PathLike =  config.external_packs_dir

        self.create_dir_if_missing(self.assets_dir)
        self.create_dir_if_missing(self.external_packs)

    def does_dir_exists(self, path: os.PathLike) -> bool:
        return os.path.isdir(path)
    
    def create_dir_if_missing(self, path: os.PathLike) -> None:
        if not self.does_dir_exists(path):
            print(f"'{path}' not found. Creating '{path}' directory...")
            os.mkdir(path)