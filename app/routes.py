from flask import Blueprint, render_template, request, redirect, url_for
from .scraper import extract_data
import pandas as pd
import os

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('home.html')

@main.route('/results', methods=['POST'])
def results():
    # Récupérer l'URL soumise par l'utilisateur
    url = request.form['url']
    data = extract_data(url)

    # Enregistrer les résultats dans un fichier CSV
    output_csv = 'data/extracted_info.csv'
    results_df = pd.DataFrame([data])
    if os.path.exists(output_csv):
        results_df.to_csv(output_csv, mode='a', header=False, index=False)
    else:
        results_df.to_csv(output_csv, mode='w', header=True, index=False)

    return render_template('results.html', data=data)
