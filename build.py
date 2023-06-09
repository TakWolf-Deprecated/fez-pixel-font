import logging

from configs import path_define
from services import font_service, publish_service
from utils import fs_util

logging.basicConfig(level=logging.DEBUG)


def main():
    fs_util.delete_dir(path_define.build_dir)

    font_service.format_glyph_files()
    font_service.make_font_files()
    publish_service.make_release_zips()


if __name__ == '__main__':
    main()
