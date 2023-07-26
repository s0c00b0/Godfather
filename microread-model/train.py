'''Generates and trains the model.'''

import argparse
import numpy as np
import spacy
import os
import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import log_loss, accuracy_score
from xgboost import XGBClassifier

def generate_model(text_array, label_array, opt):
    nlp = spacy.load('en_core_web_lg')
    embed = np.array([nlp(text).vector for text in text_array])
    X_train, X_test, y_train, y_test = train_test_split(embed, label_array)
    
    model = XGBClassifier(n_estimators = opt.n_estimators, learning_rate = opt.learning_rate,
                            use_label_encoder=False, eval_metric=log_loss)
    
    model.fit(X_train, y_train,
                early_stopping_rounds = opt.early_stopping_rounds,
                eval_set = [(X_test, y_test)])
    
    prediction = model.predict(X_test)
    print('[INFO] final accuracy of model: ' + str(accuracy_score(prediction, y_test)))
    
    return model

def load_training_data(opt):
    if not os.path.exists(opt.data_path):
        print("[ERROR] training data does not exist")
        quit()
    
    if not opt.data_path.endswith(".csv"):
        print("[ERROR] data must be in .csv format")
        quit()
        
    training_data = pd.read_csv(opt.data_path)
    return np.array(training_data.text), np.array(training_data.label)

def save_model(model, opt):
    if not os.path.exists(opt.model_path):
        os.mkdirs(opt.model_path)
    
    saved_model = os.path.join(opt.model_path, "microread_model.pkl")
    pickle.dump(model, open(opt.model_pat, "wb"))

def main():
    # TODO
    parser = argparse.ArgumentParser()
    
    parser.add_argument("-n_estimators", type=int, default=1000)
    parser.add_argument("-learning_rate", type=float, default=0.05)
    parser.add_argument("-early_stopping_rounds", type=int, default=10)
    parser.add_argument("-model_path", default=None)
    parser.add_argument("-data_path", default=None)
    
    opt = parser.parse_args()

    print("[INFO] loading training data...")
    text_array, label_array = load_training_data(opt)
    print("[INFO] loading complete")
    print("[INFO] generating and training model...")
    model = generate_model(text_array, label_array, opt)
    print("[INFO] training complete")
    print("[INFO] saving model to " + opt.model_path)
    save_model(model, opt)
    print("[INFO] model saved")

if __name__ == '__main__':
    main()