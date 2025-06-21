from flask import Flask, jsonify
from flask_cors import CORS
import boto3
import os
import urllib.parse

app = Flask(__name__)
CORS(app)

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_REGION = 'sa-east-1'
BUCKET_NAME = 'empresa-ibovespa-dividendosinvest'
PREFIX = 'AWS S3 - BANCO DE DADOS API - LOGOS/'

s3 = boto3.client(
    's3',
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

S3_BASE_URL = f"https://{BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/"

@app.route('/api/logos', methods=['GET'])
def list_logos():
    try:
        response = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=PREFIX)

        if 'Contents' not in response:
            return jsonify([])

        logos = []
        for obj in response['Contents']:
            key = obj['Key']
            filename = key[len(PREFIX):]
            url_encoded_key = urllib.parse.quote(key)
            url = f"{S3_BASE_URL}{url_encoded_key}"

            logos.append({
                'filename': filename,
                'url': url
            })

        return jsonify(logos)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
