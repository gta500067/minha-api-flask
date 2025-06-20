import os
import boto3
from flask import Flask, jsonify

app = Flask(__name__)

# --- Seu código existente da API pode estar aqui ---

@app.route('/testar-s3')
def testar_conexao_s3():
    """
    Endpoint de diagnóstico para verificar a conexão com o S3.
    """
    print("Iniciando teste de conexão com o S3...")
    
    # Pega o nome do bucket a partir das variáveis de ambiente
    bucket_name = os.environ.get('S3_BUCKET_NAME')
    if not bucket_name:
        print("Erro: A variável de ambiente S3_BUCKET_NAME não foi definida.")
        return jsonify({
            "sucesso": False,
            "etapa": "Configuração",
            "mensagem": "A variável de ambiente 'S3_BUCKET_NAME' não foi encontrada."
        }), 500

    try:
        # Tenta criar um cliente S3. Isso testa as credenciais.
        print(f"Tentando criar cliente S3 para a região {os.environ.get('AWS_DEFAULT_REGION')}...")
        s3_client = boto3.client('s3')
        
        # Tenta listar os objetos no bucket. Isso testa as permissões e se o bucket existe.
        print(f"Tentando listar objetos no bucket: {bucket_name}")
        s3_client.list_objects_v2(Bucket=bucket_name, MaxKeys=1) # MaxKeys=1 para ser mais rápido
        
        print("Sucesso! Conexão com S3 funcionando.")
        # Se os comandos acima funcionarem, a conexão está OK.
        return jsonify({
            "sucesso": True,
            "mensagem": "Conexão com o Amazon S3 e acesso ao bucket foram bem-sucedidos!",
            "bucket_verificado": bucket_name
        })

    except Exception as e:
        # Se ocorrer qualquer erro, captura e retorna uma mensagem detalhada.
        print(f"Falha no teste de conexão com o S3: {e}")
        return jsonify({
            "sucesso": False,
            "etapa": "Execução",
            "mensagem": "Ocorreu um erro ao tentar se conectar ao S3.",
            "detalhe_do_erro": str(e) # Converte o erro em texto
        }), 500

# --- O resto do seu código da API ---