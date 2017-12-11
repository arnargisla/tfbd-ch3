import sys
from random import random
from math import floor
from os import listdir, makedirs, path
from os.path import isfile, join, exists
from moviepy.editor import VideoFileClip
from image_hash import image_hash
from PIL import Image
import numpy as np
import config
import multiprocessing
import cached_results

def create_average_frame(video_clip):
    n_frames = 0
    dimensions = list(reversed(video_clip.size)) + [3]
    pixel_matrix = np.zeros(tuple(dimensions), dtype=np.uint8)
    for frame in video_clip.iter_frames():
        pixel_matrix = pixel_matrix + frame
        n_frames = n_frames + 1

    average_frame_matrix = pixel_matrix / n_frames
    return Image.fromarray(average_frame_matrix, 'RGB')

def load_frame_from_cache(file_name):
    image_name = path.basename(file_name).split('.')[0] + ".jpg"
    image_path = path.join(config.image_path, image_name)
    #print("Loading image {}".format(image_path))
    return Image.open(image_path)

def average_frame_is_cached(file_name):
    image_name = path.basename(file_name).split('.')[0] + ".jpg"
    image_path = path.join(config.image_path, image_name)
    if exists(image_path):
        return True
    return False

def cache_image(image, file_name):
    image_name = path.basename(file_name).split('.')[0] + ".jpg"
    image_path = path.join(config.image_path, image_name)
    image.save(image_path)
    
def create_video_hash(file_name):
    average_frame = None
    if average_frame_is_cached(file_name):
        average_frame = load_frame_from_cache(file_name)
    else:
        video_clip = VideoFileClip(file_name)
        average_frame = create_average_frame(video_clip)
        cache_image(average_frame, file_name)

    if file_name in cached_results.hashes:
        return cached_results.hashes[file_name]
    else:
        average_frame_hash = image_hash(average_frame)
        cached_results.add_hash(file_name, average_frame_hash)
        return average_frame_hash

def init_image_cache():
    if not exists(config.image_path):
        makedirs(config.image_path)

def main(argv):
    init_image_cache()
    data_path = argv[1]
    for file_name in listdir(data_path):
        if isfile(join(data_path, file_name)):
            video_hash = create_video_hash(join(data_path, file_name))
            print(video_hash, (floor(random()*10) % 10), file_name)

if __name__ == "__main__":
    main(sys.argv)
