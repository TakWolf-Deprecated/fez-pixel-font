import logging
import os
import zipfile

import configs
from configs import path_define, font_config
from utils import fs_util

logger = logging.getLogger('publish-service')


def make_release_zips():
    fs_util.make_dirs(path_define.releases_dir)
    for font_format in configs.font_formats:
        file_path = os.path.join(path_define.releases_dir, f'fez-pixel-font-{font_format}-v{font_config.VERSION}.zip')
        with zipfile.ZipFile(file_path, 'w') as file:
            font_file_name = f'{font_config.outputs_name}.{font_format}'
            file.write(os.path.join(path_define.outputs_dir, font_file_name), font_file_name)
            file.write(os.path.join(path_define.assets_dir, 'readme.txt'), 'readme.txt')
            file.write(os.path.join(path_define.project_root_dir, 'LICENSE-CC0'), 'CC0.txt')
        logger.info(f"Make release zip: '{file_path}'")
