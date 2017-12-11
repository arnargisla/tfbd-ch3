import config
import pickle
from os import path, makedirs

def save_obj(obj, name):
    if not path.exists('obj'):
        makedirs('obj')
    with open('obj/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name):
    object_path = 'obj/' + name + '.pkl'
    if path.exists(object_path):
        with open(object_path, 'rb') as f:
            return pickle.load(f)
    else:
        return {}

def add_hash(key, hash_string):
    hashes[key] = hash_string
    save_obj(hashes, "cached_hashes")

def reset_cache():
    global hashes
    hashes = {}
    save_obj({}, "cached_hashes")

hashes = load_obj("cached_hashes")
