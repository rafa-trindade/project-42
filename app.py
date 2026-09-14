from flask import Flask, render_template, request, jsonify
import pandas as pd
import os

app = Flask(__name__)
CSV_FILE = 'historico_peso.csv'

if not os.path.exists(CSV_FILE):
    df_init = pd.DataFrame({
        "Data": ["2026-08-30", "2026-09-06", "2026-09-13"],
        "Peso": [139.0, 133.9, 132.8]
    })
    df_init.to_csv(CSV_FILE, index=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/pesos', methods=['GET'])
def get_pesos():
    df = pd.read_csv(CSV_FILE)
    df.rename(columns={'Data': 'date', 'Peso': 'peso'}, inplace=True)
    return jsonify(df.to_dict(orient='records'))

@app.route('/api/pesos', methods=['POST'])
def save_pesos():
    data = request.json
    df = pd.DataFrame(data)
    df.rename(columns={'date': 'Data', 'peso': 'Peso'}, inplace=True)
    df.to_csv(CSV_FILE, index=False)
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)