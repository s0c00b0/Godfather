'''Preprocess posts into model input.'''

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

def main():
    # TODO
    pass

if __name__ == '__main__':
    main()