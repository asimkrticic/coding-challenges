import io
import os
import sys
from package.packer import Packer

if __name__ == "__main__":

    path = None
    try:
        path = sys.argv[1]
        if not os.path.isabs(path):
            path = os.path.abspath(path)
    except IndexError:
        pass

    results = Packer.pack(path)
    print results
