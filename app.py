# Importa as classes e funções necessárias do pacote Flask.
# Flask: A classe principal para criar a aplicação.
# jsonify: Para converter dicionários Python em respostas JSON.
# send_from_directory: Para enviar arquivos de uma pasta de forma segura.
# make_response: Para criar um objeto de resposta customizado.
from flask import Flask, jsonify, send_from_directory, make_response

# Cria a instância principal da aplicação.
# '__name__' é uma variável especial do Python que ajuda o Flask a
# localizar recursos como a pasta 'static'.
app = Flask(__name__)

# --- DEFINIÇÃO DAS ROTAS (ENDPOINTS) ---

@app.route('/')
def home():
    """
    Endpoint principal (homepage).
    Retorna uma simples página HTML.
    O navegador interpreta isso como HTML por padrão.
    Content-Type: text/html
    """
    return """
    <h1>API Multifacetada!</h1>
    <p>Esta API demonstra como servir diferentes tipos de conteúdo.</p>
    <h3>Experimente os endpoints abaixo:</h3>
    <ul>
        <li><a href="/api/dados" target="_blank">/api/dados</a> - Retorna dados em formato JSON.</li>
        <li><a href="/saudacao" target="_blank">/saudacao</a> - Retorna uma mensagem de texto puro.</li>
        <li><a href="/imagem" target="_blank">/imagem</a> - Exibe uma imagem.</li>
        <li><a href="/relatorio" target="_blank">/relatorio</a> - Força o download de um arquivo PDF.</li>
    </ul>
    """

@app.route('/api/dados')
def obter_dados():
    """
    Endpoint que serve dados estruturados.
    Ideal para ser consumido por outras aplicações.
    Content-Type: application/json
    """
    dados_exemplo = {
        'id': 1,
        'produto': 'Laptop de Alta Performance',
        'data_consulta': '2025-06-20',
        'disponivel_em_estoque': True
    }
    return jsonify(dados_exemplo)

@app.route('/saudacao')
def saudacao_texto():
    """
    Endpoint que serve texto simples.
    Útil para respostas leves ou quando o formato não importa.
    Content-Type: text/plain
    """
    # Criamos uma resposta customizada para definir o tipo de conteúdo (mimetype).
    resposta = make_response("Olá! Esta é uma resposta em texto puro.", 200)
    resposta.mimetype = "text/plain"
    return resposta

@app.route('/imagem')
def servir_imagem():
    """
    Endpoint que serve um arquivo de imagem estático.
    O Flask define o Content-Type (ex: image/png) automaticamente
    baseado na extensão do arquivo.
    """
    return send_from_directory('static', 'logo.png')

@app.route('/relatorio')
def servir_pdf():
    """
    Endpoint que serve um arquivo PDF e força o download.
    O 'as_attachment=True' é o que diz ao navegador para baixar
    em vez de tentar exibir o arquivo.
    """
    return send_from_directory('static', 'relatorio.pdf', as_attachment=True)

# --- SEÇÃO PARA EXECUÇÃO LOCAL (PARA TESTES) ---

# Este bloco só é executado quando você roda o script diretamente com 'python app.py'.
# A plataforma de hospedagem (Render) não usará este bloco, ela usará o Gunicorn.
if __name__ == '__main__':
    # Inicia o servidor de desenvolvimento do Flask.
    # debug=True é ótimo para desenvolver, pois recarrega o servidor
    # a cada mudança e mostra erros detalhados.
    app.run(debug=True, port=5000)