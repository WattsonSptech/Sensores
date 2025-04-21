import asyncio
import json
import os

import dotenv
from tqdm import tqdm

from interfaces.Registro import Registro
from sensores.Corrente import Corrente
from sensores.Frequencia import Frequencia
from sensores.Harmonica import Harmonica
from sensores.Potencia import Potencia
from sensores.Temperatura import Temperatura
from sensores.Tensao import Tensao
from azure.iot.device.aio import IoTHubDeviceClient

def obter_dados(quantidade):
    dados = []
    sensores = (Corrente, Frequencia, Harmonica, Potencia, Tensao, Temperatura)

    for s in sensores:
        dados.extend(s().gerar_dados(quantidade))

    return dados

async def enviar_para_azure(dados: list[Registro]):
    conn_str = os.getenv("AZURE_CREDENTIALS")
    if conn_str is None or conn_str == "":
        raise ValueError("Variável de ambiente \"AZURE_CREDENTIALS\" indefinida ou inválida.")

    device_client = IoTHubDeviceClient.create_from_connection_string(conn_str)

    await device_client.connect()
    print("Conectado com sucesso!")

    print("\nEnviando dados...")
    try:
        for dado in tqdm(dados):
            await device_client.send_message(json.dumps(dado))
        print("\nSucesso!")
    except Exception as e:
        print("Falha:")
        raise e
    finally:
        await device_client.shutdown()

if __name__ == "__main__":
    dotenv.load_dotenv()
    dados = obter_dados(100)
    asyncio.run(enviar_para_azure(dados))