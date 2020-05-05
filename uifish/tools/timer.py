import time
from uifish.tools.log import logger
from datetime import datetime


def sleep_of_countdown(second):
    for idx in range(int(second)):
        logger.info(f'Time: {second-idx}S')
        time.sleep(1)


def strf_time(date: datetime, format: str = '%Y-%m-%d %H:%M:%S'):
    return date.strftime(format)


if __name__ == '__main__':
    sleep_of_countdown(3)
