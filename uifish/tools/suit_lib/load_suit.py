import yamlplus
from uifish.settings import ObjPaths
import os


class LoadSuits:
    def __init__(self):
        self.suit_path = ObjPaths.suits
        self.len = 6

    def load(self, path=None):
        cases = []
        case = {
            'metadata': None,
            'path': None,

        }
        if path:
            if os.path.exists(path):
                self.suit_path = path
        folder_path = self._find_folder([self.suit_path])
        print(folder_path)
        return folder_path

    def _find_folder(self, folders: list):
        for idx in range(self.len):
            for path in folders:
                list_dir = os.listdir(path)

                for pa in list_dir:
                    current_path = os.path.join(path, pa)
                    if os.path.isdir(current_path):
                        folders.append(current_path)
                        self._find_folder(folders)
        return folders
