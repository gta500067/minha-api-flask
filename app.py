# app.py
import os
from flask import Flask, jsonify
from dotenv import load_dotenv
import boto3
from botocore.exceptions import ClientError

# Carrega as variáveis de ambiente do arquivo .env (ótimo para desenvolvimento local)
load_dotenv()

app = Flask(__name__)

# --- Configuração do Cliente S3 ---
# Boto3 vai procurar as credenciais nas variáveis de ambiente.
# Verifique se AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY e AWS_REGION estão configuradas no seu ambiente de deploy.
s3_client = boto3.client(
    's3',
    region_name=os.getenv('AWS_REGION', 'us-east-1') # Use a região do seu bucket
)

BUCKET_NAME = 'empresa-ibovespa-dividendosinvest'
LOGO_PREFIX = 'AWS S3 - BANCO DE DADOS API - LOGOS/'

@app.route('/api/logos', methods=['GET'])
def get_logos():
    try:
        # 1. Lista os objetos na pasta do S3
        response = s3_client.list_objects_v2(Bucket=BUCKET_NAME, Prefix=LOGO_PREFIX)
        
        # Garante que a chave 'Contents' existe na resposta
        if 'Contents' not in response:
            return jsonify([])

        # Filtra para não incluir o diretório em si (objetos de tamanho 0)
        objects = [obj for obj in response['Contents'] if obj['Size'] > 0]
        
        logos_data = []
        
        # 2. Gera uma URL assinada (Presigned URL) para cada objeto
        for obj in objects:
            # Parâmetros para gerar a URL
            presigned_url_params = {
                'Bucket': BUCKET_NAME,
                'Key': obj['Key']
            }
            
            # Gera a URL que expira em 1 hora (3600 segundos)
            url = s3_client.generate_presigned_url(
                'get_object',
                Params=presigned_url_params,
                ExpiresIn=3600
            )

            file_name = obj['Key'].split('/')[-1]
            
            logos_data.append({
                'id': obj['ETag'], # ETag é um hash único do objeto
                'src': url,
                'alt': f"Logo {file_name}"
            })
            
        return jsonify(logos_data)

    except ClientError as e:
        # Erro específico do cliente AWS (ex: credenciais inválidas, bucket não encontrado)
        print(f"Erro do Boto3: {e}")
        return jsonify({"message": "Erro ao contatar o serviço de armazenamento."}), 500
    except Exception as e:
        # Outros erros genéricos
        print(f"Erro inesperado: {e}")
        return jsonify({"message": "Erro interno do servidor."}), 500

# Esta parte SÓ roda em ambiente local, não em produção com Gunicorn
if __name__ == '__main__':
    app.run(debug=True, port=5001)