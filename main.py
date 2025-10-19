import os
from datetime import datetime, timedelta

import dotenv
from time import sleep
from tqdm import tqdm
from io_cursors.aws_helper import AwsHelper
from interfaces.EnumZonas import EnumZonas
from generators.GeradorTensao import GeradorTensao
from io_cursors.LocalFiles import LocalFiles

class OrquestradorDadosSensores:

    gerador: GeradorTensao
    gen_timeout: int
    ts_atual: datetime
    save_locally: bool
    aws_helper: AwsHelper|None

    def __init__(self):
        dotenv.load_dotenv()
        self.gerador = GeradorTensao([ez.name for ez in EnumZonas])
        self.gen_timeout = int(os.getenv("GENERATION_TIMEOUT"))
        self.ts_atual = datetime.now()
        self.save_locally = os.getenv("RECORD_LOGS", "0") == "1"

        self.aws_helper = None
        if os.getenv("SENT_TO_AWS", "0") == "1":
            self.aws_helper = AwsHelper()

    def setup_inicial(self):
        dados_st_inicial = self.gerador.setup_inicial(14)
        self.gravar_dados(dados_st_inicial)

    def geracao_continua(self):
        while True:
            print("\n\tGerando dados...")
            inicio = self.ts_atual
            fim = inicio + timedelta(days=1)

            dados = self.gerador.gerar_dados_zonas(inicio, fim)
            self.ts_atual = fim

            self.gravar_dados(dados)
            for _ in tqdm(range(0, self.gen_timeout), desc="\tSegundos para a próxima geração"):
                sleep(1)

    def gravar_dados(self, dados: list[dict]):
        if self.aws_helper is not None:
            self.aws_helper.send_data(dados)

        if self.save_locally:
            LocalFiles.salvar_local(dados)

if __name__ == "__main__":
    print("GERADOR DE DADOS ALGAS")
    print("Versão 4.0\n")
    orq = OrquestradorDadosSensores()
    orq.setup_inicial()
    orq.geracao_continua()
