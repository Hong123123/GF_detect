import glob
import os

def load_frames(FRAMES_PATH_BASE):
    NUM_FRAMES = 0
    for filename in glob.iglob(FRAMES_PATH_BASE.format('*'), recursive=True):
        NUM_FRAMES += 1
    filenames = [FRAMES_PATH_BASE.format(i) for i in range(NUM_FRAMES)]
    return filenames

def ensure_dir(file_dir):
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    return file_dir
