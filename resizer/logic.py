import os

def read_to_bytes(src):
    with open(src, 'rb') as f:
        return f.read()

def remove_file(src):
    try:
        os.remove(src)
        return True
    except IOError:
        return False
