'''Preprocess posts from Mafia Universe games into model input.'''

import re
import string

def remove_quotes(post):
    # remove outer quote tags
    for i in range(0, len(post)):
        if post[i] == ']':
            post = post[i+1:]
            break
    for i in range(1, len(post)):
        if post[-1 * i] == '[':
            post = post[:-1 * i - 1]
            break
            
    # search through string for quotes and remove
    post = re.sub('\[QUOTE=.*?\].*\[/QUOTE\]', '', post)
    
    return post

def trim(post):
    # TODO
    pass
    
def preprocess_post(post):
    # replace all whitespace characters with spaces
    post = re.sub('\s', ' ', post)
    
    # remove all quotes as well as outer quote tags
    post = remove_quotes(post)
    
    # remove all BBCode, emojis, and images
    post = trim(post)
    
    # remove all writing style differences (i.e. upper/lowercase, punctuation, etc.)
    post = post.lower()
    post = post.translate(post.maketrans('', '', string.punctuation))
    post = post.strip()
    
    return post
