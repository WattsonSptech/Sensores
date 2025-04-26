import asyncio
import json
import os
import dotenv
from tqdm import tqdm
from interfaces.EnumCenarios import EnumCenarios
from interfaces.Registro import Registro
from sensores.Corrente import Corrente
from sensores.Frequencia import Frequencia
from sensores.Harmonica import Harmonica
from sensores.Potencia import Potencia
from sensores.Temperatura import Temperatura
from sensores.Tensao import Tensao
from azure.iot.device.aio import IoTHubDeviceClient

def obter_dados(quantidade: int, cenario: EnumCenarios):
    dados = []
    memoria = []
    cpu = []
    sensores = [Corrente, Frequencia, Harmonica, Potencia, Tensao, Temperatura]
    
    print(f"Gerando dados de {sensores}")
    print(f"{quantidade} valores de cada, no cenário {cenario.name}\n")
    for s in sensores:
        result = s().gerar_dados(quantidade, cenario)
        dados.extend(result[0])
        cpu.extend(result[1])
        memoria.extend(result[2])

    print('cpu', cpu)
    print('memoria', memoria)

    return dados

async def enviar_para_azure(dados: list[Registro]):
    print("Tentando conexão com a nuvem para enviar os dados...")

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
        print("\n[😃] Sucesso!")
    except Exception as e:
        print("\n[!] Falha:")
        raise e
    finally:
        await device_client.shutdown()

if __name__ == "__main__":
    dotenv.load_dotenv()
    dados_simulados = obter_dados(100, EnumCenarios.NORMAL)
    print(dados_simulados)
    # asyncio.run(enviar_para_azure(dados_simulados))