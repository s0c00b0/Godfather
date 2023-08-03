'''Makes predictions about a player's alignment based on a single post.'''

import argparse
import os
import pickle
import spacy
from preprocess import preprocess_post, load_data

def predict(posts, model):
    nlp = spacy.load('en_core_web_lg')
    prediction = model.predict_proba([nlp(post).vector for post in posts])
    
    for i in range(len(prediction)):
        if (prediction[i][0] > prediction[i][1]):
            print('[OUTPUT] Alignment prediction for post ' + i + ' is town with probability ' + str(prediction[0][0]))
        else:
            print('[OUTPUT] Alignment prediction for post ' + i + ' is anti-town with probability ' + str(prediction[0][1]))
        
def load_model(opt):
    if not os.path.exists(opt.model_path):
        print("[ERROR] model does not exist")
        quit()
    
    return pickle.load(open(opt.model_path, "rb"))

def main():
    parser = argparse.ArgumentParser()
    
    parser.add_argument("-model_path", default=None)
    parser.add_argument("-predict_path", default=None)
    
    opt = parser.parse_args()
    
    if not opt.model_path:
        print("[ERROR] model_path is a required argument")
        quit()
    
    if not opt.predict_path:
        print("[ERROR] prediction input not specified")
        quit()
        
    model = load_model(opt)
    
    if not os.path.exists(opt.predict_path):
        print("[ERROR] prediction input does not exist")
        quit()

    posts = [preprocess_post(post) for post in load_data(opt.predict_path)]
    predict(posts, model)

if __name__ == '__main__':
    main()