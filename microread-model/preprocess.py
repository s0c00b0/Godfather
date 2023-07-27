'''Preprocess posts into model input.'''

import argparse
import os
import re
import string
import numpy as np

def remove_quotes(post):
    for i in range(0, len(post)):
        if post[i] == ']':
            post = post[i+1:]
            break
    for i in range(1, len(post)):
        if post[-1 * i] == '[':
            post = post[:-1 * i - 1]
            break
            
    post = re.sub('\[QUOTE=.*?\].*\[/QUOTE\]', '', post)
    
    return post

def trim(post):
    # TODO
    pass
    
def preprocess_post(post):
    post = re.sub('\s', ' ', post)
    post = remove_quotes(post)
    post = trim(post)
    post = post.lower()
    post = post.translate(post.maketrans('', '', string.punctuation))
    post = post.strip()
    
    return post

def preprocess_posts(posts):
    return np.array([preprocess_post(post) for post in posts])

def load_data(opt):
    if not os.path.exists(opt.data_path):
        print("[ERROR] data does not exist")
        quit()
    
    f = open(opt.data_path, "r")
    
    # TODO
    pass

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-data_path", default=None)
    opt = parser.parse_args()
    
    if not opt.data_path:
        print("[ERROR] data_path is a required argument")
        quit()
        
    print("[INFO] loading data...")
    posts = load_data(opt)
    print("[INFO] loading complete")
    
if __name__ == '__main__':
    main()