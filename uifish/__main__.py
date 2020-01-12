# from uifish.settings import object_folders
import os
import fire
from .tools.init import UiFishInit


def main():
    fire.Fire(UiFishInit)


if __name__ == '__main__':
    main()
