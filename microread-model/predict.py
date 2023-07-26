'''Makes predictions about a player's alignment based on a single post.'''

import os
import pickle
import spacy

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
    # TODO
    pass

if __name__ == '__main__':
    main()