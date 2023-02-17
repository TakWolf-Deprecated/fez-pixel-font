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


def collect_glyph_files():
    alphabet = set()
    glyph_file_paths = {}

    for glyph_file_name in os.listdir(path_define.glyphs_dir):
        if not glyph_file_name.endswith('.png'):
            continue
        glyph_file_path = os.path.join(path_define.glyphs_dir, glyph_file_name)
        glyph_file_name = glyph_file_name.removesuffix('.png')
        if glyph_file_name == 'notdef':
            glyph_file_paths['.notdef'] = glyph_file_path
            continue
        elif glyph_file_name == '10':
            cs = ['#']
        elif glyph_file_name == 'K,Q':
            cs = ['K', 'Q']
        elif glyph_file_name == 'U,V':
            cs = ['U', 'V']
        elif glyph_file_name == 'space':
            cs = [' ']
        else:
            cs = [glyph_file_name]
        for c in cs:
            alphabet.add(c)
            glyph_file_paths[ord(c)] = glyph_file_path

    fallback_letter_offsets = [code_point - ord('A') for code_point in [ord('a'), ord('Ａ'), ord('ａ')]]
    for code_point in range(ord('A'), ord('Z') + 1):
        for fallback_letter_offset in fallback_letter_offsets:
            fallback_code_point = code_point + fallback_letter_offset
            alphabet.add(chr(fallback_code_point))
            glyph_file_paths[fallback_code_point] = glyph_file_paths[code_point]

    fallback_number_offset = ord('０') - ord('0')
    for code_point in range(ord('0'), ord('9') + 1):
        fallback_code_point = code_point + fallback_number_offset
        fallback_c = chr(fallback_code_point)
        if fallback_c in alphabet:
            continue
        alphabet.add(fallback_c)
        glyph_file_paths[fallback_code_point] = glyph_file_paths[code_point]

    alphabet = list(alphabet)
    alphabet.sort()
    return alphabet, glyph_file_paths
