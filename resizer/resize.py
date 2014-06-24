from PIL import Image

def resize(src, out, w, h, quality=70):
    image = Image.open(src)
    image.thumbnail((w, h), Image.ANTIALIAS)
    image.convert('RGB').save(out, "JPEG", quality=quality)
    return True

def _width_or_height(width, height):
    if width:
        return 'width'
    return 'height'

def resize_with_specific_ratio(src, out, width=None, height=None, quality=70):
    which = _width_or_height(width, height)
    image = Image.open(src)
    old_width, old_height = image.size
    if which is 'height':
        new_height = height
        new_width = int((float(new_height) / old_height) * old_width)
    else:
        new_width = width
        new_height = int((float(new_width) / old_width) * old_height)
    image = image.resize((new_width, new_height), Image.ANTIALIAS)
    image.convert('RGB').save(out, "JPEG", quality=quality)
    return True
