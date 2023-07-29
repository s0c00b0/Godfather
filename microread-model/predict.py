'''Makes predictions about a player's alignment based on a single post.'''

import argparse
import os
import pickle
import spacy
from preprocess import preprocess_post

def predict(post, model):
    nlp = spacy.load('en_core_web_lg')
    prediction = model.predict_proba()
    
    if (prediction[0] > prediction[1]):
        print('[OUTPUT] Alignment prediction is town with probability ' + str(prediction[0]))
    else:
        print('[OUTPUT] Alignment prediction is anti-town with probability ' + str(prediction[1]))
        
def load_model(opt):
    if not os.path.exists(opt.model_path):
        print("[ERROR] model does not exist")
        quit()
    
    return pickle.load(open(opt.model_path, "rb"))

def main():
    parser = argparse.ArgumentParser()
    
    parser.add_argument("-model_path", default=None)
    parser.add_argument("-predict_text", default=None)
    parser.add_argument("-predict_path", default=None)
    
    opt = parser.parse_args()
    
    if not opt.model_path:
        print("[ERROR] model_path is a required argument")
        quit()
    
    if not any([opt.predict_text, opt.predict_path]):
        print("[ERROR] prediction input not specified")
        quit()

    if all([opt.predict_text, opt.predict_path]):
        print("[ERROR] predict_text and predict_path are incompatible arguments")
        quit()
    
    model = load_model(opt)
    
    if opt.predict_text:
        post = preprocess_post(opt.predict_text)
        predict(post, model)
    else:
        if not os.path.exists(opt.predict_path):
            print("[ERROR] prediction input does not exist")
            quit()

        f = open(opt.predict_path, "r")
        post = ""
        for line in f:
            post += line
        
        predict(post, model)

if __name__ == '__main__':
    main()