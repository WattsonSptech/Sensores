import awscrt.mqtt
from awsiot import mqtt_connection_builder
from awscrt import mqtt
import os
import traceback
import json
import requests

class AwsHelper:

    device = awscrt.mqtt.Connection
    topic = None
    base_path = "./io_cursors/aws_config_files"
    ROOT_CA1_URL = "https://www.amazontrust.com/repository/AmazonRootCA1.pem"

    def __init__(self):
        self.topic = os.getenv('TOPIC')
        self.base_path = os.path.abspath(self.base_path)

        self._baixar_arquivo_root()
        self.device = self._criar_device()

    def _baixar_arquivo_root(self):
        if not os.path.exists(self.base_path):
            os.makedirs(self.base_path)

        full_filepath = f'{self.base_path}/AmazonRootCA1.pem'
        if not os.path.exists(full_filepath):
            try:
                response = requests.get(self.ROOT_CA1_URL)
                response.raise_for_status()
                with open(full_filepath,'wb') as file:
                    file.write(response.content)
                    print('\tArquivo ROOT CA1 da Amazon baixado com sucesso!')
            except requests.exceptions.RequestException as e:
                print(f'\tOcorreu um erro na chamada:{e}')

    def _criar_device(self) -> awscrt.mqtt.Connection:
        ca_filepath = os.path.abspath(f"{self.base_path}/AmazonRootCA1.pem")

        iot_config_files_path = os.getenv('IOT_CONFIG_FILES_PATH', None)
        if iot_config_files_path is None or not os.path.exists(iot_config_files_path):
            raise EnvironmentError(
                f"O parâmetro .env com o caminho para os arquivos de configuração do IoT não foi configurado ou está "
                f"inválido: \"{iot_config_files_path}\""
            )

        cert_filepath = os.path.abspath(f"{iot_config_files_path}/iot-certificate.pem.crt")
        pri_key_filepath = os.path.abspath(f"{iot_config_files_path}/iot-private-key.pem.crt")
        if not os.path.exists(cert_filepath) or not os.path.exists(pri_key_filepath):
            raise FileNotFoundError(f"Ou o iot-certificate ou a iot-private-key não existem em \"{cert_filepath}\".")

        device = mqtt_connection_builder.mtls_from_path(
            cert_filepath=cert_filepath, pri_key_filepath=pri_key_filepath, ca_filepath=ca_filepath,
            endpoint=os.getenv("ENDPOINT"), client_id=os.getenv("CLIENT_ID"), keep_alive_secs = 30
        )
        device.connect().result()
        print("Conexão bem estabelecida!")
        return device
        
    def send_data(self, dados: list[dict]):
        print("\n\tEnviando dados para Iot Core...")
        try:
            self.device.publish(topic=self.topic,payload= json.dumps(dados),qos=mqtt.QoS.AT_LEAST_ONCE)
            print(f'Publicado no topico {self.topic}')
        except Exception as e:
            print(f"\n[!] Falha ao enviar dados: {e}")
            traceback.print_exc()
