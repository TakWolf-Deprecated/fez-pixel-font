import logging
import os

from configs import path_define
from utils import glyph_util

logger = logging.getLogger('design-service')


def verify_glyph_files():
    for glyph_file_name in os.listdir(path_define.glyphs_dir):
        if not glyph_file_name.endswith('.png'):
            continue
        glyph_file_path = os.path.join(path_define.glyphs_dir, glyph_file_name)
        glyph_data, width, height = glyph_util.load_glyph_data_from_png(glyph_file_path)

        assert width == height == 6, glyph_file_path
        for alpha in glyph_data[-1]:
            assert alpha == 0, glyph_file_path
        for i in range(0, height):
            assert glyph_data[i][0] == 0, glyph_file_path

        glyph_util.save_glyph_data_to_png(glyph_data, glyph_file_path)
        logger.info(f'format glyph file {glyph_file_path}')
