import sys
from random import random
from math import floor
from os import listdir
from os.path import isfile, join
from moviepy.editor import VideoFileClip
from image_hash import image_hash
from PIL import Image
import numpy as np

def create_video_hash(file_name):

    #Get the video file
    clip = VideoFileClip(file_name)

    #For each video, create an average frame of the pixels
    n_frames = 0
    dimensions = list(reversed(clip.size)) + [3]
    pixel_matrix = np.zeros(tuple(dimensions), dtype=np.uint8)
    for frame in clip.iter_frames():
        pixel_matrix = pixel_matrix + frame
        n_frames = n_frames + 1

    average_frame_matrix = pixel_matrix / n_frames
    avg_frame = Image.fromarray(average_frame_matrix, 'RGB')

    #Create an image hash for the average frame
    h = image_hash(avg_frame)
    return h



def main(argv):
    data_path = argv[1]
    for file_name in listdir(data_path):
        if isfile(join(data_path, file_name)):
            video_hash = create_video_hash(join(data_path, file_name))
            print(video_hash)
            print((floor(random()*10) % 10), file_name)

if __name__ == "__main__":
    main(sys.argv)
