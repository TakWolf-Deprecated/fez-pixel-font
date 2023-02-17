import logging
import os
import zipfile

import configs
from configs import path_define, font_config
from utils import fs_util

logger = logging.getLogger('publish-service')


def make_release_zips(font_formats=None):
    if font_formats is None:
        font_formats = configs.font_formats

    fs_util.make_dirs_if_not_exists(path_define.releases_dir)
    for font_format in font_formats:
        zip_file_path = os.path.join(path_define.releases_dir, f'{font_config.release_zip_file_name_prefix}-{font_format}-v{font_config.version}.zip')
        with zipfile.ZipFile(zip_file_path, 'w') as zip_file:
            font_file_name = f'{font_config.font_file_name_prefix}.{font_format}'
            zip_file.write(os.path.join(path_define.outputs_dir, font_file_name), font_file_name)
        logger.info(f'make {zip_file_path}')
