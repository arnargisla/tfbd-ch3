import sys
from random import random
from math import floor
from os import listdir
from os.path import isfile, join

def main(argv):
    data_path = argv[1]
    for file_name in listdir(data_path):
        if isfile(join(data_path, file_name)):
            print((floor(random()*10) % 10), file_name)

if __name__ == "__main__":
    main(sys.argv)
