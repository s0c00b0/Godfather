'''Generates and trains the model.'''

import numpy as np
import spacy
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import log_loss, accuracy_score
from xgboost import XGBClassifier

def generate_model(text_array, label_array,
                    n_estimators = 1000, learning_rate = 0.05, early_stopping_rounds = 10):
    nlp = spacy.load('en_core_web_lg')
    embed = np.array([nlp(text).vector for text in text_array])
    X_train, X_test, y_train, y_test = train_test_split(embed, label_array)
    
    model = XGBClassifier(n_estimators = 1000, learning_rate = 0.05,
                            use_label_encoder=False, eval_metric=log_loss)
    
    model.fit(X_train, y_train,
                early_stopping_rounds = 10,
                eval_set = [(X_test, y_test)])
    
    prediction = model.predict(X_test)
    print('Final accuracy of model: ' + str(accuracy_score(prediction, y_test)))
    
    return model
