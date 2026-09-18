from flask import Flask, render_template, request, jsonify
import pandas as pd
import os

import threading
import webview
import sys

app = Flask(__name__)
CSV_FILE = 'historico_peso.csv'

if not os.path.exists(CSV_FILE):
    df_init = pd.DataFrame(columns=["Data", "Peso"])
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
    # 1. Função para rodar o Flask em segundo plano
    def run_flask():
        # use_reloader=False é essencial para rodar junto com a interface
        app.run(port=5000, debug=False, use_reloader=False)
    
    # Inicia o servidor backend
    threading.Thread(target=run_flask, daemon=True).start()
    
    # 2. Abre a janela do aplicativo (estilo software nativo)
    webview.create_window('Project-42', 'http://127.0.0.1:5000', width=1280, height=850)
    webview.start()
    
    # 3. Quando você clica no "X" para fechar a janela, o script chega aqui e mata o Flask
    sys.exit()