from PIL import Image

def resize(src, out, w, h, quality=70):
    image = Image.open(src)
    image.thumbnail((w, h), Image.ANTIALIAS)
    image.convert('RGB').save(out, "JPEG", quality=quality)
    return True

def main():
    import sys

    try:
        src = sys.argv[1]
        out = sys.argv[2]
        w = int(sys.argv[3])
        h = int(sys.argv[4])
        resize(src, out, w, h)
        sys.exit(0)
    except IndexError:
        print 'Missing argument, please use the resizer like this:'
        print 'python {} source_image output_image width height'.format(__file__)
        sys.exit(1)


if __name__ == '__main__':
    main()
