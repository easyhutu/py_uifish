import os
from uifish.settings import object_folders, object_files
from uifish.tools.parse_json import to_value, base_keys_tree
import sqlite3
from uifish.tools.template import template_content


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
                self._make_file(path, key, template_content.get(key[-1]))
            elif isinstance(val, str):
                key.append(val)
                self._make_file(path, key, template_content.get(val))

    @staticmethod
    def _make_file(base_path, keys, content=None):
        for idx, key in enumerate(keys):
            base_path = os.path.join(base_path, key)
            if os.path.exists(base_path) is False:
                os.mkdir(base_path)
                print('create', base_path)
            if idx == len(keys)-1:
                if content == 'sql':
                    file = open(base_path, 'w', encoding='utf8')
                    file.write(content)
                    file.close()
                elif content:
                    file = open(base_path, 'w', encoding='utf8')
                    file.close()
                    conn = sqlite3.connect(base_path)
                    conn.close()

