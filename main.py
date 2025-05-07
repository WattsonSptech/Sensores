import asyncio
from datetime import datetime
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
    sensores = [Corrente, Frequencia, Harmonica, Potencia, Tensao, Temperatura]

    print(f"Gerando dados de {", ".join([s.__name__ for s in sensores])}")
    print(f"{quantidade} valores de cada, no cenário {cenario.name}\n")
    for s in sensores:
        print(s.__name__)
        dados.extend(s().gerar_dados(quantidade, cenario))

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

def salvar_local(dados: list[Registro]):
    print("Gravando dados localmente...")

    path = "./logs"
    filename = f"generation-{datetime.now().strftime("%d-%m-%Y_%H-%M-%S")}.json"

    if not os.path.exists(path):
        os.mkdir(path)

    with open(f"{path}/{filename}", 'w') as f:
        json.dump([dict(d) for d in tqdm(dados)], f, indent=4)
    print("\n[😃] Sucesso!")

if __name__ == "__main__":
    dotenv.load_dotenv()

    send_to_azure = os.getenv("SENT_TO_AZURE", "0")
    record_logs = os.getenv("RECORD_LOGS", "0")
    QTD_DADOS = 1000000
    cenarios = [EnumCenarios.TERRIVEL, EnumCenarios.NORMAL, EnumCenarios.EXCEPCIONAL]
    dados_simulados = []

    for c in cenarios:
        print("\n================================")
        print(f"Executando cenário: {c.name}\n")
        dados_simulados.extend(obter_dados(QTD_DADOS, c))

    if send_to_azure == "1":
        asyncio.run(enviar_para_azure(dados_simulados))

    if record_logs == "1":
        salvar_local(dados_simulados)