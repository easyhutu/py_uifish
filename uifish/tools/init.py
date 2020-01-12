import os


class UiFishInit(object):
    def init(self, path=None):
        self._make_obj_folder(path)

    def run(self, path=None):
        pass

    def clear(self):
        pass

    @staticmethod
    def _make_obj_folder(path):
        if path:
            if os.path.exists(path) is None:
                raise OSError(f'{path} 文件路径不存在！')
        else:
            path = os.path.abspath(os.getcwd())
        print(path)
