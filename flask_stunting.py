# -*- coding: utf-8 -*-
"""flask_weatherprediction.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1wCEC-ZgsIZ9fNmzlTtjX3fdfCuiOjQXv
"""

from flask import Flask, request, render_template
import joblib
import os

app = Flask(__name__)

file_path = 'C:/web_server/knn.model'

# Handling kesalahan saat membuka file model
try:
    with open(file_path, 'rb') as model_file:
        model = joblib.load(model_file)
except Exception as e:
    print(f"Error loading the model: {str(e)}")
    model = None

template_dir = os.path.abspath('C:/web_server')
app = Flask(__name__, template_folder=template_dir)

@app.route('/')
def index():
    return render_template('index.html',  Status_Gizi=0, Umur=0, Jenis_Kelamin=0, Tinggi_Badan=0)

@app.route('/predict', methods=['POST'])
def predict():
    # Menerima input dari form
    Umur, Jenis_Kelamin, Tinggi_Badan = [float(x) for x in request.form.values()]

    # Menyiapkan data untuk prediksi
    data = [Umur, Jenis_Kelamin, Tinggi_Badan]

    try:
        # Melakukan prediksi dengan model
        if model:
            prediction = model.predict([data])
            output = round(float(prediction[0]), 2)
        else:
            output = 0
    except Exception as e:
        print(f"Error during prediction: {str(e)}")
        output = 0

    # Menampilkan hasil prediksi di halaman HTML
    return render_template('index.html', Status_Gizi=output, Umur=Umur, Jenis_Kelamin=Jenis_Kelamin, Tinggi_Badan=Tinggi_Badan)

if __name__ == '__main__':
    app.run(debug=True)