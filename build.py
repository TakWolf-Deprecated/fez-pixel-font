import logging

from configs import path_define
from services import design_service, font_service
from utils import fs_util

logging.basicConfig(level=logging.DEBUG)


def main():
    fs_util.delete_dir(path_define.build_dir)

    design_service.verify_glyph_files()
    alphabet, glyph_file_paths = design_service.collect_glyph_files()
    font_service.make_fonts(alphabet, glyph_file_paths)


if __name__ == '__main__':
    main()
