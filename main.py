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
from Levenshtein import distance
import compare_strings
from sklearn.cluster import KMeans

def eprint(s):
    print(s, file=sys.stderr)


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

def find_closest_hash(h, hashes):
    closest = list(hashes)[0]
    smallest_d =  100
    for h2, name in hashes:
        d = compare_strings.compare(h, h2)
        if d < smallest_d:
            closest = (h2, name)
            smallest_d = d

    return closest

def main(argv):
    init_image_cache()
    data_path = argv[1]
    hash_video_list = []
    total_number_of_items = len(listdir(data_path))
    counter = 0

    for file_name in listdir(data_path):
        if(counter % 100 == 0):
            eprint("Hashing {}/{}".format(counter, total_number_of_items))
        counter += 1

        if isfile(join(data_path, file_name)):
            video_hash = create_video_hash(join(data_path, file_name))
            hash_video_list.append(video_hash)

    hash_video_array = np.array(hash_video_list)
    kmeans = KMeans(n_clusters=10).fit(hash_video_array)
    print(kmeans.cluster_centers_)

    eprint("Done hashing")
    
    hashes = list(hash_video_list)
    clusters = []
    counter = 0
    while hashes:
        if(counter % 100 == 0):
            eprint("Clustering {}/{}".format(counter, total_number_of_items/10))
        counter += 1

        h, name = hashes.pop()
        cluster = [(h, name)]
        for _ in range(9):
            if(hashes):
                closest_item = find_closest_hash(h, hashes)
                cluster.append(closest_item)
                hashes.remove(closest_item)
                
        clusters.append(cluster)

    eprint("Done clustering")

    for i, cluster in enumerate(clusters):
        for video_hash, file_name in cluster:
            print(video_hash, i, file_name)

    #for video_hash, file_name in hash_video_dict.items():


if __name__ == "__main__":
    main(sys.argv)
