from flask import Flask, request, jsonify

import pandas as pd
import pickle
import logging
import os

app = Flask(__name__)

with open('ml-model.pkl', 'rb') as f:
    MODEL = pickle.load(f)

FEATURES_MASK = ['CRIM', 'ZN', 'INDUS', 'CHAS', 'NOX', 'RM', 'AGE', 'DIS',\
                 'RAD', 'TAX', 'PTRATIO', 'B', 'LSTAT']

@app.route('/', methods=['GET'])
def server_check():
    return "I'M ALIVE!  <<<  2  <<<  4"

@app.route('/predict', methods=['POST'])
def predictor():
    content = request.json

    try:
        features = pd.DataFrame([content])
        features = features[FEATURES_MASK]
    except:
        logging.exception("An exception was thrown!")
        return jsonify(status='error', predict=-1)

    pred = MODEL.predict(features)[0]

    return jsonify(status='ok', predict=pred)

if __name__=='__main__':
    app.run( debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)) )