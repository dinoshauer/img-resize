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

def main():
    import sys
    import argparse

    parser = argparse.ArgumentParser(description='Resizes images, maintaining aspect ratio')
    parser.add_argument('--width', type=int, help='Desired width of the image')
    parser.add_argument('--height', type=int, help='Desired height of the image')
    parser.add_argument('-i', '--input', required=True, help='Path to image')
    parser.add_argument('-o', '--output', required=True, help='Path to output image')
    args = parser.parse_args()

    if args.width and args.height:
        resize(args.input, args.output, args.width, args.height)
    else:
        resize_with_specific_ratio(args.input, args.output, width=args.width, height=args.height)
    sys.exit(0)

if __name__ == '__main__':
    main()
