# Arquivo: aplicacao_web.py
# -*- coding: utf-8 -*-

import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash
from werkzeug.utils import secure_filename
from processador import executar_analise_completa # Importa nossa função principal

# --- Configuração da Aplicação Flask ---
app = Flask(__name__)

# Configuração de pastas e extensões permitidas
PASTA_UPLOADS = 'uploads'
PASTA_RELATORIOS = 'relatorios_gerados'
EXTENSOES_PERMITIDAS = {'csv'}
app.config['PASTA_UPLOADS'] = PASTA_UPLOADS
app.config['PASTA_RELATORIOS'] = PASTA_RELATORIOS
app.config['SECRET_KEY'] = 'uma-chave-secreta-muito-forte' # Necessário para usar 'flash messages'

# Garante que as pastas de upload e relatórios existam
os.makedirs(PASTA_UPLOADS, exist_ok=True)
os.makedirs(PASTA_RELATORIOS, exist_ok=True)

def arquivo_permitido(nome_arquivo):
    """Verifica se a extensão do arquivo é permitida."""
    return '.' in nome_arquivo and nome_arquivo.rsplit('.', 1)[1].lower() in EXTENSOES_PERMITIDAS

# --- Definição das Rotas (Páginas) ---

@app.route('/')
def index():
    """Rota para a página inicial."""
    return render_template('index.html')
# Em aplicacao_web.py, substitua a função upload_de_arquivo por esta:

@app.route('/upload', methods=['POST'])
def upload_de_arquivo():
    """Rota para lidar com o upload, processamento e limpeza do arquivo."""
    if 'arquivo_csv' not in request.files:
        flash('Nenhum arquivo enviado.')
        return redirect(url_for('index'))

    arquivo = request.files['arquivo_csv']

    if arquivo.filename == '':
        flash('Nenhum arquivo selecionado.')
        return redirect(url_for('index'))

    if arquivo and arquivo_permitido(arquivo.filename):
        nome_seguro = secure_filename(arquivo.filename)
        caminho_salvo = os.path.join(app.config['PASTA_UPLOADS'], nome_seguro)
        
        # =======================================================
        #      NOVO BLOCO TRY...FINALLY PARA GARANTIR A LIMPEZA
        # =======================================================
        try:
            # 1. Salva o arquivo temporariamente
            arquivo.save(caminho_salvo)
            
            # 2. Executa a análise completa
            resultado = executar_analise_completa(caminho_salvo, app.config['PASTA_RELATORIOS'])

            # 3. Retorna o resultado para o usuário
            if resultado["sucesso"]:
                return render_template('resultado.html', resumo=resultado["resumo"], nome_arquivo_pdf=resultado["nome_arquivo_pdf"])
            else:
                flash(f'Erro ao processar o arquivo: {resultado["erro"]}')
                return redirect(url_for('index'))
        
        finally:
            # 4. LIMPEZA: Este bloco é executado SEMPRE, após o try.
            # Remove o arquivo CSV da pasta /uploads para não deixar rastros.
            if os.path.exists(caminho_salvo):
                os.remove(caminho_salvo)
                print(f"✔ Arquivo temporário '{nome_seguro}' foi removido com sucesso.")

    else:
        flash('Extensão de arquivo não permitida. Por favor, envie um arquivo .csv.')
        return redirect(url_for('index'))
@app.route('/download/<nome_do_arquivo>')
def download_de_relatorio(nome_do_arquivo):
    """Rota para fazer o download do PDF gerado."""
    return send_from_directory(app.config['PASTA_RELATORIOS'], nome_do_arquivo, as_attachment=True)

# --- Execução da Aplicação ---
if __name__ == '__main__':
    app.run(debug=True) # debug=True é ótimo para desenvolvimento