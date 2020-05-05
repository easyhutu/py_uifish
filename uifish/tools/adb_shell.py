from uifish.tools.log import logger
import subprocess


def adb_type(key):
    def decorator(func):
        def wrapper(*args):
            if args:
                logger.debug(f'adb: {key} {args[0]}')
            return func(*args, key=key)
        return wrapper
    return decorator


class AdbShell:
    def __init__(self):
        self.adb = {
            'input': self.input_text,
            'install': self.install
        }
        self.adb_list = list(self.adb.keys())

    @staticmethod
    @adb_type('install')
    def install(path, key=None):
        subprocess.run(f'adb {key} {path}')

    @staticmethod
    @adb_type('shell input text')
    def input_text(text, key=None):
        subprocess.run(f'adb {key} {text}')

    @staticmethod
    def shell(cmd):
        logger.debug(cmd)
        subprocess.run(cmd)
