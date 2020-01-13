import os
from uifish.settings import object_folders, object_files
from uifish.tools.parse_json import to_value, base_keys_tree
from uifish.tools.template import template_paths
import sqlite3
import shutil


class UiFishInit(object):
    def init(self, path=None):
        if path:
            if os.path.exists(path) is None:
                raise OSError(f'{path} 文件路径不存在！')
        else:
            path = os.path.abspath(os.getcwd())

        self._make_obj_folder(path)
        self._make_obj_files(path)
        print('success init uifish')

    def run(self, path=None):
        pass

    def clear(self):
        pass

    def _make_obj_folder(self, path):
        object_folders_keys = base_keys_tree(object_folders)
        for key in object_folders_keys:
            val = to_value(object_folders, key)
            if isinstance(val, str):
                key.append(val)
                self._make_dir(path, key)
            else:
                self._make_dir(path, key)

    @staticmethod
    def _make_dir(base_path, keys):
        for key in keys:
            base_path = os.path.join(base_path, key)
            if os.path.exists(base_path) is False:
                os.mkdir(base_path)
                print('create', base_path)

    def _make_obj_files(self, path):
        object_files_keys = base_keys_tree(object_files)
        for key in object_files_keys:
            val = to_value(object_files, key)
            if val is None:
                self._make_file(path, key, key[-1])
            elif isinstance(val, str):
                key.append(val)
                self._make_file(path, key, val)

    @staticmethod
    def _make_file(base_path, keys, content=None):
        for idx, key in enumerate(keys):
            base_path = os.path.join(base_path, key)
            if idx == len(keys) - 1:
                src_path = template_paths.get(content)
                if src_path:
                    print('create', base_path)
                    shutil.copy2(src_path, base_path)
            else:
                if os.path.exists(base_path) is False:
                    os.mkdir(base_path)
                    print('create', base_path)
