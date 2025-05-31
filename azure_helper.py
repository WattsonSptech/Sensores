import asyncio
import json
import os
import traceback
from math import ceil

from azure.iot.device import IoTHubDeviceClient
from tqdm import tqdm


class AzureHelper:

    client = IoTHubDeviceClient

    def __init__(self):
        conn_str = os.getenv("AZURE_CREDENTIALS")
        if conn_str is None or conn_str == "":
            raise ValueError("Variável de ambiente \"AZURE_CREDENTIALS\" indefinida ou inválida.")

        self.client = IoTHubDeviceClient.create_from_connection_string(conn_str)
        try:
            print("Tentando se conectar com a Azure...")
            self.client.connect()
            print("\tSucesso!")
        except Exception as e:
            print(f"\n[!] Falha ao conectar: {e}")
            traceback.print_exc()

    def send_data(self, dados: list[dict]):
        asyncio.run(self.__send_data__(self.client, dados))

    @staticmethod
    async def __send_data__(client: IoTHubDeviceClient, dados: list[dict]):
        try:
            json_strs = [json.dumps(d) for d in dados]
            total_size_in_kb = sum([len(j) / 1024 for j in json_strs])
            qtt_messages = ceil(total_size_in_kb / 256)

            slice_size = int(len(json_strs) / qtt_messages)
            start_idx = 0
            end_idx = slice_size

            print(f"\tIniciando o envio dos dados em {qtt_messages} fatia{"s" if qtt_messages > 1 else ""}...")
            for _ in tqdm(range(qtt_messages)):
                client.send_message(json.dumps(dados[start_idx:end_idx]))

                start_idx += slice_size
                end_idx += slice_size

            print("\t[😃] Sucesso!")

        except Exception as e:
            print(f"\n[!] Falha ao enviar dados: {e}")
            traceback.print_exc()