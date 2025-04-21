import asyncio
import os

from interfaces.Registro import Registro
from sensores.Corrente import Corrente
from sensores.Frequencia import Frequencia
from sensores.Harmonica import Harmonica
from sensores.Potencia import Potencia
from sensores.Tensao import Tensao
from azure.iot.device.aio import IoTHubDeviceClient

def obter_dados(quantidade):
    dados = []
    sensores = (Corrente, Frequencia, Harmonica, Potencia, Tensao)

    for s in sensores:
        dados.append(s().gerar_dados(quantidade))

    return dados

async def enviar_para_azure(dados: list[Registro]):
    conn_str = os.getenv("AZURE_CREDENTIALS")
    if conn_str is None:
        raise ValueError("Variável de ambiente \"AZURE_CREDENTIALS\" indefinida ou inválida.")

    device_client = IoTHubDeviceClient.create_from_connection_string(conn_str)

    await device_client.connect()

    print("Enviando dados...")
    try:
        await device_client.send_message(dados)
        print("Sucesso")
    except Exception as e:
        print("Falha:")
        raise e
    finally:
        await device_client.shutdown()

if __name__ == "__main__":
    dados = obter_dados(5)
    asyncio.run(enviar_para_azure(dados))