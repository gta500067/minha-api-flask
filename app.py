from flask import Flask, Response
from flask_cors import CORS
import boto3
import os

app = Flask(__name__)
CORS(app)

# Configurações da AWS - RECOMENDADO usar variáveis de ambiente
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_REGION = 'sa-east-1'
BUCKET_NAME = 'empresa-ibovespa-dividendosinvest'
S3_PREFIX = 'AWS S3 - BANCO DE DADOS API - LOGOS/'

# Inicializa o cliente S3
s3 = boto3.client(
    's3',
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

@app.route('/api/logo/<ticker>', methods=['GET'])
def get_logo(ticker):
    filename = f"{ticker.upper()}.jpg"
    s3_key = f"{S3_PREFIX}{filename}"

    try:
        # Busca o arquivo no S3
        obj = s3.get_object(Bucket=BUCKET_NAME, Key=s3_key)
        return Response(
            obj['Body'].read(),
            mimetype='image/jpeg',
            headers={"Content-Disposition": f"inline; filename={filename}"}
        )
    except s3.exceptions.NoSuchKey:
        return Response(f"Logo não encontrado: {filename}", status=404)
    except Exception as e:
        return Response(f"Erro ao acessar o S3: {str(e)}", status=500)

if __name__ == '__main__':
    app.run(debug=True)
