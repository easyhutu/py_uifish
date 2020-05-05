import yamlplus
from uifish.settings import ObjPaths
import os
from uifish.tools.parse_json import base_keys_tree, to_value, change_value
from uifish.tools.log import logger


_img_folder_name = '_img'
_img_key_path = ['click', 'img']


class LoadSuits:
    def __init__(self):
        self.suit_path = ObjPaths.suits
        self.len = 6
        self.allow_ext = ['.yml', '.yaml']

    def _is_suit_file(self, filename):
        _, ext = os.path.splitext(filename)
        if ext in self.allow_ext:
            return True
        return

    @staticmethod
    def _check_case_img(content: dict, img_obj):
        key_tree = base_keys_tree(content)
        for key in key_tree:
            if len(key) > 1:
                img_val = to_value(content, key)
                if key[-2:] == _img_key_path and img_val in list(img_obj):
                    change_value(content, key, img_obj.get(img_val))

    def load(self, path=None):
        cases = []
        case = {
            'metadata': None,
            'path': None,
            'content': None,

        }
        if path:
            if os.path.exists(path):
                self.suit_path = path
        folder_path = self._find_folder([self.suit_path])
        for folder in folder_path:
            all_files = os.listdir(folder)
            img_path = os.path.join(folder, _img_folder_name)
            img_obj = {}
            if os.path.exists(img_path):
                for img_filename in os.listdir(img_path):
                    img_obj[img_filename] = os.path.join(img_path, img_filename)

            for filename in all_files:
                file_path = os.path.join(folder, filename)
                if os.path.isfile(file_path) and self._is_suit_file(filename):
                    ca = case.copy()
                    ca['path'] = file_path
                    metadata = dict(
                        create_time=os.path.getctime(file_path),
                        update_time=os.path.getmtime(file_path),
                        size=os.path.getsize(file_path),
                        filename=filename,
                        path=file_path
                    )
                    ca['metadata'] = metadata
                    with open(file_path, encoding='utf8') as f:
                        content = yamlplus.load(f.read())
                        self._check_case_img(content, img_obj)

                        ca['content'] = content
                    cases.append(ca)
        return cases

    def _find_folder(self, folders: list):
        for idx in range(self.len):
            for path in folders:
                list_dir = os.listdir(path)
                for pa in list_dir:
                    current_path = os.path.join(path, pa)
                    if os.path.isdir(current_path) and current_path not in folders:
                        folders.append(current_path)
                    else:
                        break
        return folders
