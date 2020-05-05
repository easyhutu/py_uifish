import os
from cacheout import Cache
import logging

sqlite3_file = 'uifish.db'
config_file = 'config.yml'
case_template_file = 'uifish_eg.yml'

object_folders = {
    'suits': None,
    'static': {
        'screenshots': None,
        'videos': None,
        'reports': None,
    }
}

object_files = {
    'static': {
        'dbs': sqlite3_file
    },
    'config': {
        config_file: None
    },
    'suits': case_template_file

}

video_file_format = '{idx}_{timestamp}_{tag}'
screenshots_file_format = '{idx}_{timestamp}_{tag}'
reports_file_format = '{idx}_{timestamp}_{tag}.html'

cwd_path = os.getcwd()


def join_cwd_path(folder, base_path=None):
    if base_path:
        return os.path.join(base_path, folder)
    else:
        return os.path.join(cwd_path, folder)


class ObjPaths:
    suits = join_cwd_path('suits')
    static = join_cwd_path('static')
    screenshots = join_cwd_path('screenshots', static)
    videos = join_cwd_path('videos', static)
    reports = join_cwd_path('reports', static)
    config = join_cwd_path('config')
    config_file = join_cwd_path(config_file, config)
    dbs = join_cwd_path('dbs', static)
    sqlite3 = join_cwd_path(sqlite3_file, dbs)


HEALTH_LEVEL = 10

BATTERY_HEALTH = {
    1: 'BATTERY_HEALTH_UNKNOWN',
    2: 'BATTERY_HEALTH_GOOD',
    3: 'BATTERY_HEALTH_OVERHEAT',
    4: 'BATTERY_HEALTH_DEAD',
    5: 'BATTERY_HEALTH_OVER_VOLTAGE',
    6: 'BATTERY_HEALTH_UNSPECIFIED_FAILURE',
    7: 'BATTERY_HEALTH_COLD',
}

log_levels = {'DEBUG': logging.DEBUG,
              'INFO': logging.INFO,
              'WARNING': logging.WARNING,
              'ERROR': logging.ERROR
              }

cache = Cache()


class Case:
    init = 'init'
    click = 'click'
    input = 'input'
    diff = 'diff'
    end = 'end'
    press = 'press'
    sleep = 'sleep'
    adb = 'adb'
    check_pkg = 'check_pkg'
    key_events = [
        'home',
        'back',
        'left',
        'right',
        'up',
        'down',
        'center',
        'search',
        'enter',
        'delete',
        'power',
    ]

    @staticmethod
    def step(event: str):
        if event.startswith('step'):
            return True
        return


class cKeys:
    start_app = 'start_app'
    package = 'package'
    DB_URL = 'DB_URL'
    device_id = 'device_id'
    tag = 'tag'
    log_level = 'log_level'
    install = 'install'

    case = Case

    @staticmethod
    def get_val(value, key):
        return value.get(key) if value.get(key) else cache.get(key)
