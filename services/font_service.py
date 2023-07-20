import logging
import os

from pixel_font_builder import FontBuilder, Glyph, StyleName, SerifMode, WidthMode

from configs import path_define, font_config
from utils import fs_util, glyph_util

logger = logging.getLogger('font-service')


def format_glyph_files():
    for glyph_file_dir, glyph_file_name in fs_util.walk_files(path_define.glyphs_dir):
        if not glyph_file_name.endswith('.png'):
            continue
        glyph_file_path = os.path.join(glyph_file_dir, glyph_file_name)
        glyph_data, glyph_width, glyph_height = glyph_util.load_glyph_data_from_png(glyph_file_path)
        assert glyph_width == glyph_height == 6, f"Incorrect glyph data: '{glyph_file_path}'"
        for alpha in glyph_data[-1]:
            assert alpha == 0, f"Incorrect glyph data: '{glyph_file_path}'"
        for i in range(0, glyph_height):
            assert glyph_data[i][0] == 0, f"Incorrect glyph data: '{glyph_file_path}'"
        glyph_util.save_glyph_data_to_png(glyph_data, glyph_file_path)
        logger.info("Format glyph file: '%s'", glyph_file_path)


def _collect_glyph_files():
    character_mapping = {}
    glyph_file_paths = {}

    for glyph_file_dir, glyph_file_name in fs_util.walk_files(path_define.glyphs_dir):
        if not glyph_file_name.endswith('.png'):
            continue
        glyph_file_path = os.path.join(glyph_file_dir, glyph_file_name)
        c_name = glyph_file_name.removesuffix('.png')
        if c_name == 'notdef':
            glyph_name = '.notdef'
        else:
            if c_name == '10':
                code_points = [ord('#')]
            elif c_name == 'K,Q':
                code_points = [ord('K'), ord('Q')]
            elif c_name == 'U,V':
                code_points = [ord('U'), ord('V')]
            elif c_name == 'space':
                code_points = [ord(' ')]
            else:
                code_points = [ord(c_name)]
            glyph_name = f'uni{code_points[0]:04X}'
            for code_point in code_points:
                character_mapping[code_point] = glyph_name
        glyph_file_paths[glyph_name] = glyph_file_path

    fallback_letter_offsets = [code_point - ord('A') for code_point in [ord('a'), ord('Ａ'), ord('ａ')]]
    for code_point in range(ord('A'), ord('Z') + 1):
        if code_point not in character_mapping:
            continue
        glyph_name = character_mapping[code_point]
        for fallback_letter_offset in fallback_letter_offsets:
            fallback_code_point = code_point + fallback_letter_offset
            character_mapping[fallback_code_point] = glyph_name

    fallback_number_offset = ord('０') - ord('0')
    for code_point in range(ord('0'), ord('9') + 1):
        if code_point not in character_mapping:
            continue
        glyph_name = character_mapping[code_point]
        fallback_code_point = code_point + fallback_number_offset
        character_mapping[fallback_code_point] = glyph_name

    return character_mapping, glyph_file_paths


def _create_builder() -> FontBuilder:
    character_mapping, glyph_file_paths = _collect_glyph_files()

    builder = FontBuilder(
        font_config.size,
        font_config.ascent,
        font_config.descent,
        font_config.x_height,
        font_config.cap_height,
    )

    builder.character_mapping.update(character_mapping)
    for glyph_name, glyph_file_path in glyph_file_paths.items():
        glyph_data, glyph_width, glyph_height = glyph_util.load_glyph_data_from_png(glyph_file_path)
        builder.add_glyph(Glyph(
            name=glyph_name,
            advance_width=glyph_width,
            offset=(0, font_config.descent),
            data=glyph_data,
        ))

    builder.meta_infos.version = font_config.VERSION
    builder.meta_infos.family_name = font_config.FAMILY_NAME
    builder.meta_infos.style_name = StyleName.REGULAR
    builder.meta_infos.serif_mode = SerifMode.SANS_SERIF
    builder.meta_infos.width_mode = WidthMode.MONOSPACED
    builder.meta_infos.manufacturer = font_config.MANUFACTURER
    builder.meta_infos.designer = font_config.DESIGNER
    builder.meta_infos.description = font_config.DESCRIPTION
    builder.meta_infos.copyright_info = font_config.COPYRIGHT_INFO
    builder.meta_infos.license_info = font_config.LICENSE_INFO
    builder.meta_infos.vendor_url = font_config.VENDOR_URL
    builder.meta_infos.designer_url = font_config.DESIGNER_URL
    builder.meta_infos.license_url = font_config.LICENSE_URL

    return builder


def make_font_files():
    fs_util.make_dirs(path_define.outputs_dir)

    builder = _create_builder()
    otf_builder = builder.to_otf_builder()
    otf_file_path = os.path.join(path_define.outputs_dir, f'{font_config.OUTPUTS_NAME}.otf')
    otf_builder.save(otf_file_path)
    logger.info("Make font file: '%s'", otf_file_path)
    otf_builder.font.flavor = 'woff2'
    woff2_file_path = os.path.join(path_define.outputs_dir, f'{font_config.OUTPUTS_NAME}.woff2')
    otf_builder.save(woff2_file_path)
    logger.info("Make font file: '%s'", woff2_file_path)
    ttf_file_path = os.path.join(path_define.outputs_dir, f'{font_config.OUTPUTS_NAME}.ttf')
    builder.save_ttf(ttf_file_path)
    logger.info("Make font file: '%s'", ttf_file_path)
    bdf_file_path = os.path.join(path_define.outputs_dir, f'{font_config.OUTPUTS_NAME}.bdf')
    builder.save_bdf(bdf_file_path)
    logger.info("Make font file: '%s'", bdf_file_path)
