'''Makes predictions about a player's alignment based on a single post.'''

import spacy

def predict(post, model):
    nlp = spacy.load('en_core_web_lg')
    prediction = model.predict_proba()
    
    if (prediction[0] > prediction[1]):
        print('Alignment prediction is town with probability ' + str(prediction[0]))
    else:
        print('Alignment prediction is anti-town with probability ' + str(prediction[1]))
        
def main():
    # TODO
    pass

if __name__ == '__main__':
    main()