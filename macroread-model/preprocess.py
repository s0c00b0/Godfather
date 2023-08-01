'''Preprocess posts into model input.'''

import sys

sys.path.append("../microread-model")

import argparse
import os
import re
import pandas as pd
import preprocess

def preprocess_posts(posts):
    df = pd.DataFrame(columns=["text", "label"])
    
    for post in posts:
        author = ((re.findall("\[QUOTE.*?\]", post, flags=re.IGNORECASE))[0])[7:-1]
        semicolon = author.find(";")
        author = author[:semicolon]
        
        if author == "Mafia Host":
            rands = (re.findall("\[BOX=Rands\].*?\[/BOX\]", post, flags=re.DOTALL | re.IGNORECASE))[0]
            alignments = re.findall("\[COLOR=\#.{6}\]\[B\].*?\[/B\]\[/COLOR\] \(.*?\)\[SPOILER\]", rands, flags=re.DOTALL | re.IGNORECASE)
            conversion = {}
            
            for alignment in alignments:
                name = ((re.findall("\[B\].*?\[/B\]", alignment, flags=re.DOTALL | re.IGNORECASE))[0])[3:-4]
                town = (alignment[8:14] == "339933")
                
                conversion[name] = town
            
            # TODO
            pass
                
        else:
            post = preprocess.preprocess_post(post)
            if not post == "":
                df = pd.concat([df, pd.Series({"text": post, "label": author}).to_frame().T], ignore_index=True)
                game_postcount += 1
    
    return df

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-load_path", default=None)
    parser.add_argument("-save_path", default=".")
    opt = parser.parse_args()
    
    if not opt.load_path:
        print("[ERROR] load_path is a required argument")
        quit()
        
    if not opt.save_path:
        print("[INFO] save_path not specified, saving to data.csv in current directory")
        
    print("[INFO] loading data...")
    posts = preprocess.load_data(opt)
    print("[INFO] loading complete")
    print("[INFO] preprocessing " + str(len(posts)) + " posts...")
    df = preprocess_posts(posts)
    print("[INFO] preprocessing complete")
    print("[INFO] saving data to " + os.path.join(opt.save_path, "data.csv"))
    preprocess.save_data(df, opt)
    print("[INFO] data saved")
    
if __name__ == '__main__':
    main()