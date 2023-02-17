import logging

from services import design_service

logging.basicConfig(level=logging.DEBUG)


def main():
    design_service.verify_glyph_files()
    alphabet, glyph_file_paths = design_service.collect_glyph_files()


if __name__ == '__main__':
    main()
