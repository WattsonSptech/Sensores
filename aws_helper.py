from awsiot import mqtt_connection_builder
from awscrt import mqtt
import os
import traceback
import json

class AwsHelper:
    device = mqtt_connection_builder
    topic = None
    isConnected = False
    def __init__(self):
        ENDPOINT = os.getenv("ENDPOINT")
        PATH_TO_CERTIFICATE  = os.getenv("PATH_TO_CERTIFICATE")
        PATH_TO_PRIVATE_KEY  = os.getenv("PATH_TO_PRIVATE_KEY")
        PATH_TO_AMAZON_ROOT_CA_1  = os.getenv("PATH_TO_AMAZON_ROOT_CA_1")
        CLIENT_ID = os.getenv("CLIENT_ID")

        self.topic = os.getenv('TOPIC')
        self.isConnected = True
        self.device = mqtt_connection_builder.mtls_from_path(
            endpoint=ENDPOINT,
            cert_filepath=PATH_TO_CERTIFICATE,
            pri_key_filepath=PATH_TO_PRIVATE_KEY,
            ca_filepath=PATH_TO_AMAZON_ROOT_CA_1,
            client_id=CLIENT_ID,
            keep_alive_secs = 30
        )
        print("Conectado com sucesso!")
        try:
            self.device.connect().result()
            print(f"Conexão bem estabelecida!")
        except Exception as e:
            print(f"\n[!] Falha ao conectar: {e}")
            traceback.print_exc()
        
    def send_data(self, dados: list[dict]):
        try:
            self.device.publish(topic=self.topic,payload= json.dumps(dados),qos=mqtt.QoS.AT_LEAST_ONCE)
            print(f'Publicado no topico {self.topic}')
            #self.device.disconnect().result()        
        except Exception as e:
            print(f"\n[!] Falha ao enviar dados: {e}")
            traceback.print_exc()
            
            

    