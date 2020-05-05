from uifish.tools.suit_lib.load_suit import LoadSuits
from uifish.settings import cache, log_levels, ObjPaths, cKeys
import time
from uifish.tools.log import logger
import os
import yamlplus
from uifish.core.executor import UiDriver, Executor
from uifish.tools.adb_shell import AdbShell
from uifish.tools.timer import sleep_of_countdown


def run_case(path=None, addr=None, log_level='info'):
    init_setting(log_level)
    load_config()
    cases = LoadSuits().load(path)
    logger.info('load case ...')
    logger.info(f'load success, count: {len(cases)}')
    init_device()
    for case in cases:
        try:
            logger.info('run case {}'.format(case.get('path')))
            logger.debug(f'case: {case}')
            Executor(case).main()
        except Exception as e:
            logger.error(e)
    init_device('stop')


def init_setting(log_level='info'):
    up_level = log_level.upper()
    levels_list = list(log_levels.keys())
    if up_level not in levels_list:
        logger.warn(f'log_level support {log_levels}')
        up_level = 'INFO'
    logger.info(f'log level: {up_level}')
    cache.set(cKeys.log_level, log_levels.get(up_level))
    cache.set(cKeys.tag, str(int(time.time())))
    logger.setLevel(up_level)
    logger.info(f'run tag: {cache.get(cKeys.tag)}')


def load_config():
    if os.path.exists(ObjPaths.config_file):
        with open(ObjPaths.config_file, encoding='utf8') as f:
            config = yamlplus.load(f.read())

            cache.set(cKeys.device_id, config.get(cKeys.device_id))
            cache.set(cKeys.DB_URL, config.get(cKeys.DB_URL))
            cache.set(cKeys.package, config.get(cKeys.package))
            cache.set(cKeys.start_app, config.get(cKeys.start_app))
            cache.set(cKeys.install, config.get(cKeys.install))

            logger.info(f'load config file success {config}')
            logger.debug(f'config: {config}')


def init_device(event='start'):
    device_id = cache.get(cKeys.device_id)
    is_start = cache.get(cKeys.start_app)
    package = cache.get(cKeys.package)
    install = cache.get(cKeys.install)

    if device_id and is_start and package:
        driver = UiDriver(device_id).d
        logger.info(f'app {event}...')
        try:
            if install:
                apath = os.path.join(ObjPaths.static, install)
                logger.debug(apath)
                if os.path.exists(apath):
                    logger.debug('path exist!')
                    logger.debug(AdbShell.install(apath))
            if event == 'start':
                driver.app_start(package)
            elif event == 'stop':
                sleep_of_countdown(3)
                driver.app_stop(package)
        except Exception as e:
            logger.error(e)


if __name__ == '__main__':
    run_case(r'D:\pro\py_uifish\suits')