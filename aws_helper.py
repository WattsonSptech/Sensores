from awsiot import mqtt_connection_builder
from awscrt import mqtt
import os,traceback,time,json

class AwsHelper:
    topic = ''
    client = ''
    def __init__(self):
        ENDPOINT = os.getenv("ENDPOINT")
        PATH_TO_CERTIFICATE  = "iot-certificate.pem.crt"
        PATH_TO_PRIVATE_KEY  = "iot-private-key.pem.crt"
        PATH_TO_AMAZON_ROOT_CA_1  = "AmazonRootCA1.pem"
        CLIENT_ID = os.getenv("CLIENT_ID")
    
        self.topic = 'telemetria/teste'

        self.client = mqtt_connection_builder.mtls_from_path(
            endpoint=ENDPOINT,
            cert_filepath=PATH_TO_CERTIFICATE,
            pri_key_filepath=PATH_TO_PRIVATE_KEY,
            ca_filepath=PATH_TO_AMAZON_ROOT_CA_1,
            client_id=CLIENT_ID,
        )
        print("Conectado!")
        try:
            self.client.connect().result()
            print(f"Conexão bem sucedida!")
        except Exception as e:
            print(f"\n[!] Falha ao conectar: {e}")
            traceback.print_exc()
        
    def send_data(self, dados: list[dict]):
        try:
          self.client.publish(topic=self.topic,payload= json.dumps(dados),qos=mqtt.QoS.AT_LEAST_ONCE )
          print(f'Publicado no topico {self.topic}')
          time.sleep(1)
          self.client.disconnect().result()
        except Exception as e:
            print(f"\n[!] Falha ao enviar dados: {e}")
            traceback.print_exc()

        