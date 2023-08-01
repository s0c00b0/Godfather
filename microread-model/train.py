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

def confusion_matrix(model, X_test, y_test):
    y_predict = model.predict(X_test)
    
    TP = 0
    TN = 0
    FP = 0
    FN = 0
    
    for i in range(len(y_test)):
        if y_test[i] == y_predict[i] and y_test[i] == 1:
            TP += 1
        elif y_test[i] == y_predict[i] and y_test[i] == 0:
            TN += 1
        elif y_test[i] != y_predict[i] and y_test[i] == 1:
            FN += 1
        elif y_test[i] != y_predict[i] and y_test[i] == 0:
            FP += 1
    
    print('[OUTPUT] true positives: ' + str(TP))
    print('[OUTPUT] true negatives: ' + str(TN))
    print('[OUTPUT] false positives: ' + str(FP))
    print('[OUTPUT] false negatives: ' + str(FN))

def generate_model(text_array, label_array, opt):
    nlp = spacy.load('en_core_web_lg')
    embed = np.array([nlp(text).vector for text in text_array])
    X_train, X_test, y_train, y_test = train_test_split(embed, label_array)
    
    model = XGBClassifier(n_estimators = opt.n_estimators, learning_rate = opt.learning_rate, eval_metric=log_loss, verbosity=1)
    
    model.fit(X_train, y_train, early_stopping_rounds = opt.early_stopping_rounds, eval_set = [(X_test, y_test)])
    
    prediction = model.predict(X_test)
    print('[OUTPUT] final accuracy of model: ' + str(accuracy_score(prediction, y_test)))
    
    confusion_matrix(model, X_test, y_test)
    
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
        os.makedirs(opt.model_path)
    
    pickle.dump(model, open(os.path.join(opt.model_path, "microread-model.pkl"), "wb"))

def main():
    parser = argparse.ArgumentParser()
    
    parser.add_argument("-n_estimators", type=int, default=1000)
    parser.add_argument("-learning_rate", type=float, default=0.05)
    parser.add_argument("-early_stopping_rounds", type=int, default=10)
    parser.add_argument("-model_path", default=".")
    parser.add_argument("-data_path", default=None)
    
    opt = parser.parse_args()

    if not opt.data_path:
        print("[ERROR] data_path is a required argument")
        quit()
        
    if not opt.model_path:
        print("[INFO] model_path not specified, saving model as microread_model.pkl in current directory")

    print("[INFO] loading training data...")
    text_array, label_array = load_training_data(opt)
    print("[INFO] loading complete")
    print("[INFO] generating and training model...")
    model = generate_model(text_array, label_array, opt)
    print("[INFO] training complete")
    print("[INFO] saving model to " + os.path.join(opt.model_path, "microread-model.pkl"))
    save_model(model, opt)
    print("[INFO] model saved")

if __name__ == '__main__':
    main()