
px = 6
box_origin_y_px = 5
x_height_px = 5
cap_height_px = 5
px_units = 100

display_name = 'FEZ Pixel - Zu'
unique_name_prefix = 'FEZ-Pixel-Zu'
font_file_name_prefix = 'fez-pixel-zu'
release_zip_file_name_prefix = 'fez-pixel-font'
style_name = 'Regular'
version = '1.0.0'
copyright_string = 'This Font Software is made by TakWolf (https://takwolf.com). The Copyright of Alphabet belongs to Polytron (http://www.polytroncorporation.com).'
designer = 'TakWolf'
description = 'A font for the Alphabet in the game FEZ (https://fezgame.com) called "Zu Language".'
vendor_url = 'https://fez-pixel-font.takwolf.com'
designer_url = 'https://takwolf.com'
license_description = 'This Font Software is licensed under the Creative Commons Zero v1.0 Universal. The Copyright of Alphabet belongs to Polytron (http://www.polytroncorporation.com).'
license_info_url = 'https://creativecommons.org/publicdomain/zero/1.0/'


class VerticalMetrics:
    def __init__(self, ascent, descent, x_height, cap_height):
        self.ascent = ascent
        self.descent = descent
        self.x_height = x_height
        self.cap_height = cap_height


def get_units_per_em():
    return px * px_units


def get_box_origin_y():
    return box_origin_y_px * px_units


def get_vertical_metrics():
    ascent = box_origin_y_px * px_units
    descent = ascent - px * px_units
    x_height = x_height_px * px_units
    cap_height = cap_height_px * px_units
    return VerticalMetrics(ascent, descent, x_height, cap_height)


def get_name_strings():
    return {
        'copyright': copyright_string,
        'familyName': display_name,
        'styleName': style_name,
        'uniqueFontIdentifier': f'{unique_name_prefix}-{style_name};{version}',
        'fullName': display_name,
        'version': version,
        'psName': f'{unique_name_prefix}-{style_name}',
        'designer': designer,
        'description': description,
        'vendorURL': vendor_url,
        'designerURL': designer_url,
        'licenseDescription': license_description,
        'licenseInfoURL': license_info_url,
    }
