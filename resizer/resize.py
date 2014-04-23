from PIL import Image

def resize(src, out, w, h):
    try:
        image = Image.open(src)
        print 'image', image
        print 'image.thumbnail((w, h), Image.ANTIALIAS)', image.thumbnail((w, h), Image.ANTIALIAS)
        print 'image.save(out, "JPEG")', image.save(out, "JPEG")
    except IOError, e:
        print 'IOError'
        print e


if __name__ == '__main__':
    import sys

    try:
        src = sys.argv[1]
        out = sys.argv[2]
        w = sys.argv[3]
        h = sys.argv[4]
        resize(src, out, w, h)
    except IndexError:
        print 'Missing argument, please use the resizer like this:'
        print 'python {} source_image output_image width height'.format(__file__)
