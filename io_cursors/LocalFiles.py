import os
import json
from datetime import datetime
import boto3
import dotenv

class LocalFiles:

    @staticmethod
    def salvar_local(dados: list[dict]):

        dotenv.load_dotenv()

        bucket_raw = os.getenv("BUCKET_NAME_RAW")

        print("\n\tGravando dados para locamente...")
        path = "./logs"
        filename = "telemetry_{}.json".format(datetime.now().strftime("%d-%m-%Y_%H-%M-%S .%f")[:-3])

        if not os.path.exists(path):
            os.mkdir(path)

        full_path = f"{path}/{filename}"

        with open(full_path, 'w') as f:
            json.dump([dict(d) for d in dados], f, indent=4)

        try: 
            s3 = boto3.client('s3')
            res = s3.upload_file(full_path, bucket_raw, filename)
        except Exception as e:
            print("\t[😞] Erro ao enviar arquivo para o S3:", e)
        
        print("\t[😃] Sucesso!")
