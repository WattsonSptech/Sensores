from awsiot import mqtt_connection_builder
from awscrt import mqtt
import os
import traceback
import json
import requests

class AwsHelper:

    device = mqtt_connection_builder
    topic = None
    BASE_PATH = "./io_cursors/aws_config_files"

    def __init__(self):
        self.gerenciar_arquivo_root()

        self.topic = os.getenv('TOPIC')
        self.device = mqtt_connection_builder.mtls_from_path(
            endpoint=os.getenv("ENDPOINT"),
            cert_filepath=f"{self.BASE_PATH}/iot-certificate.pem.crt",
            pri_key_filepath=f"{self.BASE_PATH}/iot-private-key.pem.crt",
            ca_filepath=f"{self.BASE_PATH}/AmazonRootCA1.pem",
            client_id=os.getenv("CLIENT_ID"),
            keep_alive_secs = 30
        )
        self.device.connect().result()
        print("Conexão bem estabelecida!")

    def gerenciar_arquivo_root(self):
        if not os.path.exists(self.BASE_PATH):
            os.makedirs(self.BASE_PATH)

        if not os.path.exists(f'{self.BASE_PATH}/AmazonRootCA1.pem'):
            try:
                root_ca1_url = "https://www.amazontrust.com/repository/AmazonRootCA1.pem"
                response = requests.get(root_ca1_url)
                response.raise_for_status()
                with open('archives/AmazonRootCA1.pem','wb') as file:
                    file.write(response.content)
                    print('Arquivo ROOT CA1 da Amazon baixado com sucesso!')
            except requests.exceptions.RequestException as e:
                print(f'Ocorreu um erro na chamada:{e}')
        
    def send_data(self, dados: list[dict]):
        print("\n\tEnviando dados para Iot Core...")
        try:
            self.device.publish(topic=self.topic,payload= json.dumps(dados),qos=mqtt.QoS.AT_LEAST_ONCE)
            print(f'Publicado no topico {self.topic}')
        except Exception as e:
            print(f"\n[!] Falha ao enviar dados: {e}")
            traceback.print_exc()
