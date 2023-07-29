'''Preprocess posts into model input.'''

import argparse
import os
import re
import pandas as pd
    
def preprocess_post(post):
    for i in range(0, len(post)):
        if post[i] == ']':
            post = post[i+1:]
            break
    for i in range(1, len(post)):
        if post[-1 * i] == '[':
            post = post[:-1 * i - 1]
            break
    post = re.sub('\[QUOTE.*?\].*?\[/QUOTE\]', '', post)
    post = re.sub('\[IMG\].*?\[/IMG\]', '', post)
    post = re.sub('\[URL.*?\].*?\[/URL\]', '', post)
    post = re.sub('\[VIDEO.*?\].*?\[/VIDEO\]', '', post)
    post = re.sub('\[V\]', 'VOTE: ', post)
    post = re.sub('\[/?.*?\]', '', post)
    
    return post

def preprocess_posts(posts):
    df = pd.DataFrame(columns=["text", "label"])
    
    game_postcount = 0
    for post in posts:
        author = ((re.findall("\[QUOTE.*?\]", post))[0])[6:-1]
        
        if author == "Mafia Host":
            rands = (re.findall("\[BOX=Rands\].*?\[/BOX\]", post))[0]
            alignments = re.findall("\[COLOR=#[0-9]{6}\]\[B\].*?\[/B\]\[/COLOR\] (.*?)\[SPOILER\]", rands)
            conversion = {}
            
            for alignment in alignments:
                name = (re.findall("\[B\].*?\[/B\]", alignment))[3:-3]
                town = (alignment[7:13] == "339933")
                
                conversion[name] = town
                
                for i in range(game_postcount):
                    df.loc[-1 - i].label = "Town" if conversion[df.loc[-1-i].label] else "Mafia"
                
                game_postcount = 0
                
        else:
            post = preprocess_post(post)
            df.loc[-1] = [post, author]
            game_postcount += 1
    
    return df

def load_data(opt):
    if not os.path.exists(opt.load_path):
        print("[ERROR] data does not exist")
        quit()
    
    f = open(opt.load_path, "r")
    
    posts = []
    current_post = ""
    nested_quotes = 0
    
    for line in f:
        if line == "\n" and current_post == "":
            continue
        
        if line == "END_GAME_HERE\n":
            continue
        
        current_post = current_post + line
        
        nested_quotes += len(re.findall("\[QUOTE.*?\]", line))
        nested_quotes -= len(re.findall("\[/QUOTE\]", line))
        
        if nested_quotes == 0:
            posts.append(current_post)
            current_post = ""
    
    return posts

def save_data(df, opt):
    if not os.path.exists(opt.save_path):
        os.makedirs(opt.save_path)
    
    df.to_csv(opt.save_path)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-load_path", default=None)
    parser.add_argument("-save_path", default=None)
    opt = parser.parse_args()
    
    if not all([opt.load_path, opt.save_path]):
        print("[ERROR] load_path and save_path are required arguments")
        quit()
        
    print("[INFO] loading data...")
    posts = load_data(opt)
    print("[INFO] loading complete")
    print("[INFO] preprocessing posts...")
    df = preprocess_posts(posts)
    print("[INFO] preprocessing complete")
    print("[INFO] saving data to " + opt.load_path)
    save_data(df, opt)
    print("[INFO] data saved")
    
if __name__ == '__main__':
    main()