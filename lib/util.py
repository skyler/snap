import os
import errno

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST:
            pass
        else: raise

def dict_sorted(d):
    '''Returns dict sorted by key as a list of tuples'''
    return sorted(d.items(), key=lambda x: x[0])
