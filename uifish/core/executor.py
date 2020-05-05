import uiautomator2 as u2
from uifish.settings import HEALTH_LEVEL, BATTERY_HEALTH, cKeys
import time
from PIL import Image
from PIL import ImageDraw
import math
import aircv as ac
import os
from uifish.settings import cache, ObjPaths
import requests
from uifish.tools.log import logger
import time
from uifish.tools.timer import sleep_of_countdown
from uifish.tools.adb_shell import AdbShell
import subprocess


class Executor:
    def __init__(self, content):
        self.content = content
        self.case_info = content.get('content')
        self.event = None
        self.device_id = self.case_info.get(cKeys.device_id)
        self.package = self.case_info.get(cKeys.package)

    def init_event(self, value):
        self.device_id = cKeys.get_val(value, cKeys.device_id)
        self.package = cKeys.get_val(value, cKeys.package)
        self.event = Event(device_id=self.device_id)
        try:
            if cKeys.case.check_pkg:
                now_activity = subprocess.check_output('adb shell "dumpsys window | grep mCurrentFocus"')
                logger.debug(now_activity.decode())
                if self.package in now_activity.decode():
                    logger.debug('stop app {}...'.format(self.package))
                    self.event.driver.d.app_stop(self.package)
            self.event.driver.d.app_start(self.package)
        except Exception as e:
            logger.error(e)

    def main(self):
        logger.info('running...')
        for event in self.case_info.keys():
            logger.debug(event)
            if event == cKeys.case.init:
                logger.debug(f'{event}|| {self.case_info[event]}')
                self.init_event(self.case_info[event])

            elif cKeys.case.step(event):
                cron = self.case_info[event]
                logger.debug(f'{event}|| {cron}')
                for key in cron:
                    if key == cKeys.case.click:
                        logger.debug(f'{key}|| {cron[key]}')
                        self.event.click(cron[key])
                    if key == cKeys.case.input:
                        logger.debug(f'{key}|| {cron[key]}')
                        self.event.input(cron[key])
                    if key == cKeys.case.press:
                        logger.debug(f'{key}|| {cron[key]}')
                        self.event.press(cron[key])
                    if key == cKeys.case.sleep:
                        t = cron[key]
                        logger.debug(f'sleep: {t}s')
                        sleep_of_countdown(t)
                    if key == cKeys.case.adb:
                        logger.debug(f'{key}|| {cron[key]}')
                        if isinstance(cron[key], str):
                            AdbShell.shell(cron[key])
                        elif isinstance(cron[key], dict):
                            for adb_key in cron[key].keys():
                                if adb_key in AdbShell().adb_list:
                                    AdbShell().adb[adb_key](cron[key][adb_key])

            elif event == cKeys.case.end:
                if self.case_info[event]:
                    sleep_of_countdown(3)
                    self.event.driver.d.app_stop(self.package)


class Event:
    def __init__(self, video=None,
                 device_id=None,
                 diff_tag=None):
        self.device_id = device_id
        self.is_video = video
        self.diff_tag = diff_tag

        if self.device_id is None:
            self.device_id = cache.get(cKeys.device_id)
        if self.device_id is None:
            logger.error('device id is None!')

        self.driver = UiDriver(device_id)

        self.arg_click = {
            'rid': self._rid_event,
            'xy': lambda params: self.driver.d.click(*params['xy']),
            'xpath': lambda params: self.driver.d.xpath(params['xpath']).click(),
            'img': lambda params: self.driver.click_by_search_icon_img(params['img'])
        }

        self.arg_input = {
            'rid': self._rid_event,
            'xpath': lambda params: self.driver.d.xpath(params.get('xpath')).set_text(params.get('val'))
        }

    def _rid_event(self, params):
        ty = params.get('ty')
        if ty == cKeys.case.click:
            logger.debug(f'click {params}')
            self.driver.d(**params.get('rid')).click()
        elif ty == cKeys.case.input:

            p = params.get('rid')
            val = p.get('val')
            if val:
                p.pop('val')
            logger.debug(f'input {p}, {val}')
            self.driver.d(**p).send_keys(val)

    def click(self, params):
        if isinstance(params, dict):
            pass_keys = list(self.arg_click)
            for key in list(params.keys()):
                if key in pass_keys:
                    logger.debug(params)
                    params['ty'] = cKeys.case.click
                    self.arg_click[key](params)

    def input(self, params):
        if isinstance(params, dict):
            pass_keys = list(self.arg_input)
            for key in list(params.keys()):
                if key in pass_keys:
                    logger.debug(params)
                    params['ty'] = cKeys.case.input
                    self.arg_input[key](params)

    def press(self, key):
        if key in cKeys.case.key_events:
            logger.debug(f'key: {key}')
            self.driver.d.press(key)


class UiDriver(object):
    def __init__(self, device_id):
        self.d = u2.connect(device_id)

    def device_info(self):
        info = self.d.device_info
        return info

    def _check_device_heath(self):
        info = self.device_info()
        battery = info.get('battery')
        level = battery.get('level')
        health = battery.get('health')
        logger.info('check device status... ')
        logger.info('model: {}, version: {}, sdk: {} ---> '.format(info.get('model'),
                                                                   info.get('version'),
                                                                   info.get('sdk')), end='')
        if health != 2:
            raise Exception('电池状态异常，参考码：{}->{}'.format(health, BATTERY_HEALTH.get(health)))
        if level <= HEALTH_LEVEL:
            raise Exception(f'设备电池电量低于{HEALTH_LEVEL}%,禁止相关操作')
        logger.info('device ok')

    @staticmethod
    def image_draw_lines(path, xys, fill='red', width=2):
        img = Image.open(path)
        draw = ImageDraw.Draw(img)
        for xy in xys:
            draw.line(xy, fill=fill, width=width)
        img.show()

    @staticmethod
    def move_coordinate(x, y, o=0, z_len=100):
        """o >=0, =<360"""
        if 0 <= o <= 360:
            t = [0, 90, 180, 270, 360]
            if o in t:
                if o == 0 or o == 360:
                    return x + z_len, y
                elif o == 90:
                    return x, y + z_len
                elif o == 180:
                    return x - z_len, y
                elif o == 270:
                    return x, y - z_len
            else:
                p = 180 / math.pi
                if 0 < o < 90:
                    cx = z_len * math.cos(o / p)
                    cy = z_len * math.sin(o / p)
                    return x + cx, y + cy
                elif 90 < o < 180:
                    o = 90 - (o - 90)
                    cx = z_len * math.cos(o / p)
                    cy = z_len * math.sin(o / p)
                    return x - cx, y + cy
                elif 180 < o < 270:
                    o = 90 - (o - 180)
                    cx = z_len * math.cos(o / p)
                    cy = z_len * math.sin(o / p)
                    return x - cx, y - cy

                elif 270 < o < 360:
                    o = 90 - (o - 270)
                    cx = z_len * math.cos(o / p)
                    cy = z_len * math.sin(o / p)
                    return x + cx, y - cy
        else:
            return x, y

    @staticmethod
    def _find_all_img_sift(icon_path, path, is_show=False, threshold=10):
        try:
            if cache.get('log_level') == 'DEBUG':
                is_show = True

            imsrc = ac.imread(path)
            imsch = ac.imread(icon_path)
            img = Image.open(path)
            results = ac.find_all_sift(imsrc, imsch, min_match_count=threshold)
            for result in results:
                if is_show:
                    draw = ImageDraw.Draw(img)
                    logger.debug(result)
                    res = (result.get('result')[0], result.get('result')[1], result.get('result')[0] + 1,
                           result.get('result')[1] + 1)
                    draw.line(res, fill='red', width=3)
                    rec = result.get('rectangle')
                    draw.line((rec[0], rec[3], rec[2], rec[1], rec[0]), fill='red', width=5)
            try:
                img.show()
            except:
                pass
            return results
        except:
            return False

    @staticmethod
    def _find_img_sift(icon_path, path=None, is_show=False, threshold=10):
        try:
            if cache.get('log_level') == 'DEBUG':
                is_show = True
            imsrc = ac.imread(path)
            imsch = ac.imread(icon_path)
            img = Image.open(path)
            result = ac.find_sift(imsrc, imsch, min_match_count=threshold)
            x = result.get('result')[0]
            y = result.get('result')[1]
            if is_show:
                draw = ImageDraw.Draw(img)
                logger.debug(result)
                res = (result.get('result')[0], result.get('result')[1], result.get('result')[0] + 1,
                       result.get('result')[1] + 1)
                draw.line(res, fill='red', width=3)
                rec = result.get('rectangle')
                draw.line((rec[0], rec[3], rec[2], rec[1], rec[0]), fill='red', width=5)
                try:
                    img.show()
                except:
                    pass
            return x, y
        except:
            return False

    def click_by_search_icon_img(self, icon_path=None, is_show=False, threshold=60):

        if os.path.exists(icon_path):
            path = os.path.join(ObjPaths.screenshots, 'screenshot.png')
            time.sleep(0.5)
            self.screenshot_minicap(save_path=path)
            result = self._find_img_sift(icon_path=icon_path, path=path, is_show=is_show, threshold=threshold)
            if result:
                if result[0] > 0 and result[1] > 0:
                    self.d.click(*result)
                    logger.info('click x:{}, y:{}'.format(*result))
                    return True
                else:
                    return False
            else:
                return False
        else:
            logger.warn('{} 不存在'.format(icon_path))
            return False

    def screenshot_adb(self, save_path=None):
        self.d.adb_shell('screencap -p /sdcard/screenshot.png')
        if save_path is None:
            save_path = os.path.join(ObjPaths.screenshots, 'screenshot.png')
        self.d.pull("/sdcard/screenshot.png", save_path)
        logger.debug('adb screenshot {}'.format(save_path))
        time.sleep(0.2)

    def screenshot_minicap(self, minicap=False, save_path=None):
        """使用内置的uiautomator截图"""
        url = '{}?minicap={}'.format(self.d.screenshot_uri, 'true' if minicap else 'false')
        html = requests.get(url)
        if save_path is None:
            save_path = os.path.join(ObjPaths.screenshots, 'screenshot.png')
        if save_path:
            with open(save_path, 'wb') as f:
                f.write(html.content)
                logger.debug(url)
                logger.debug('save screenshot success {}'.format(save_path))
        return html.content

    def send_key(self, sleep=0.3, text=None, **kwargs):
        self.d(**kwargs).send_keys(text)
        time.sleep(sleep)

    def click(self, x, y, sleep=0.3):
        try:
            logger.debug(f'click {x}, {y}')
            self.d().click(x, y)
            time.sleep(sleep)
        except Exception as e:
            logger.error(e)
