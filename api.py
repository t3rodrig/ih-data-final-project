import os
import json
import pandas as pd
from joblib import load
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
from myroutines import clean_up, get_recommendation

load_dotenv()

URL_CLIENT = os.getenv("URL_CLIENT")


text_series = load('./data/text_series.joblib')
df = pd.read_json('./data/products.json', orient='records')

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": URL_CLIENT}})

@app.route('/api/results', methods=['POST'])
def get_results():
    try:
        data = request.get_json(force=True)
    except:
        return {'message': 'Expecting json format'}
    desc = data.get('description', "Lapiz labial rojo mate")
    recommendation = get_recommendation(desc, text_series, df)

    return jsonify(recommendation.to_dict(orient='records'))

@app.route('/')
def home():
    return {'message': 'Wrong path.'}