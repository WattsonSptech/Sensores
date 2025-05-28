import asyncio
import traceback
from datetime import datetime
import json
import os
import dotenv
from tqdm import tqdm
from azure.iot.device.aio import IoTHubDeviceClient
from interfaces.EnumCenarios import EnumCenarios
from sensores import Corrente, Frequencia, Harmonica, Potencia, Temperatura, Tensao

def obter_dados_cenario(quantidade: int, cenario: EnumCenarios):
    print(f"Cenário {cenario.name}")
    dados = []
    sensores = [Corrente, Frequencia, Harmonica, Potencia, Tensao, Temperatura]

    for s in sensores:
        dados.extend(s().gerar_dados(quantidade, cenario))

    return dados

async def enviar_para_azure(dados: list[dict]):
    print("\n[ENVIO DE DADOS PARA A AZURE]\n")

    conn_str = os.getenv("AZURE_CREDENTIALS")
    if conn_str is None or conn_str == "":
        raise ValueError("Variável de ambiente \"AZURE_CREDENTIALS\" indefinida ou inválida.")

    device_client = IoTHubDeviceClient.create_from_connection_string(conn_str)
    try:
        print("Tentando se conectar com a Azure...")
        await device_client.connect()

        print("Enviando dados...")
        await device_client.send_message(json.dumps(dados))
        print("[😃] Sucesso!")
    except Exception as e:
        print(f"\n[!] Falha: {e}")
        traceback.print_exc()

    finally:
        await device_client.shutdown()

def salvar_local(dados: list[dict]):
    print("\n[GRAVAÇÃO DE DADOS LOCAL]\n")

    path = "./logs"
    filename = f"generation-{datetime.now().strftime("%d-%m-%Y_%H-%M-%S")}.json"

    if not os.path.exists(path):
        os.mkdir(path)

    with open(f"{path}/{filename}", 'w') as f:
        json.dump([dict(d) for d in tqdm(dados)], f, indent=4)
    print("[😃] Sucesso!")

if __name__ == "__main__":
    print("GERADOR DE DADOS ALGAS")
    print("Versão 3.0")
    print()
    dotenv.load_dotenv()

    send_to_azure = os.getenv("SENT_TO_AZURE", "0")
    record_logs = os.getenv("RECORD_LOGS", "0")
    QTD_DADOS = int(os.getenv("DATA_LENGTH", "0"))

    cenarios = [EnumCenarios.TERRIVEL, EnumCenarios.NORMAL, EnumCenarios.EXCEPCIONAL]
    dados_simulados = []
    print("\n[GERAÇÃO DE DADOS]\n")
    for c in cenarios:
        dados_simulados.extend(obter_dados_cenario(QTD_DADOS, c))

    if send_to_azure == "1":
        asyncio.run(enviar_para_azure(dados_simulados))

    if record_logs == "1":
        salvar_local(dados_simulados)