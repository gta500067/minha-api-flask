from flask import Flask, jsonify, send_from_directory, make_response
import os
import boto3

app = Flask(__name__)

@app.route('/')
def home():
    return """
    <h1>API Multifacetada!</h1>
    <p>Esta API demonstra como servir diferentes tipos de conteúdo.</p>
    <h3>Experimente os endpoints abaixo:</h3>
    <ul>
        <li><a href="/api/dados" target="_blank">/api/dados</a> - Retorna dados em formato JSON.</li>
        <li><a href="/saudacao" target="_blank">/saudacao</a> - Retorna uma mensagem de texto puro.</li>
        <li><a href="/imagem" target="_blank">/imagem</a> - Exibe uma imagem.</li>
        <li><a href="/relatorio" target="_blank">/relatorio</a> - Força o download de um arquivo PDF.</li>
        <li><a href="/s3-test" target="_blank">/s3-test</a> - Testa listagem de arquivos no bucket S3.</li>
    </ul>
    """

@app.route('/api/dados')
def obter_dados():
    dados_exemplo = {
        'id': 1,
        'produto': 'Laptop de Alta Performance',
        'data_consulta': '2025-06-20',
        'disponivel_em_estoque': True
    }
    return jsonify(dados_exemplo)

@app.route('/saudacao')
def saudacao_texto():
    resposta = make_response("Olá! Esta é uma resposta em texto puro.", 200)
    resposta.mimetype = "text/plain"
    return resposta

@app.route('/imagem')
def servir_imagem():
    return send_from_directory('static', 'logo.png')

@app.route('/relatorio')
def servir_pdf():
    return send_from_directory('static', 'relatorio.pdf', as_attachment=True)

@app.route("/s3-test", methods=["GET"])
def s3_test():
    bucket = os.getenv("S3_BUCKET_NAME")
    if not bucket:
        return jsonify(status="erro", mensagem="Variável de ambiente S3_BUCKET_NAME não definida."), 400
    try:
        s3 = boto3.client('s3')
        response = s3.list_objects_v2(Bucket=bucket, MaxKeys=5)
        arquivos = [obj["Key"] for obj in response.get("Contents", [])]
        return jsonify(status="ok", arquivos=arquivos)
    except Exception as e:
        return jsonify(status="erro", mensagem=str(e)), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
