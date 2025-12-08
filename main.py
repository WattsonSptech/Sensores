import os
import json
import dotenv
from math import ceil
from tqdm import tqdm
from time import sleep
from datetime import datetime, timedelta
from interfaces.EnumZonas import EnumZonas
from io_cursors.aws_helper import AwsHelper
from io_cursors.LocalFiles import LocalFiles
from generators.GeradorTensao import GeradorTensao

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
        self.save_locally = os.getenv("SAVE_LOCALLY", "0") == "1"

        self.aws_helper = None
        if os.getenv("SENT_TO_AWS", "0") == "1":
            self.aws_helper = AwsHelper()


    def geracao_continua(self):
        while True:
            print("\n\tGerando dados...")
            inicio = self.ts_atual
            fim = inicio + timedelta(days=1)

            dados = self.gerador.gerar_dados_zonas(inicio, fim)
            [self.gravar_dados(p) for p in self.reduzir_tamanho_arquivo(dados)]

            for _ in tqdm(range(0, self.gen_timeout), desc="\tSegundos para a próxima geração"):
                sleep(1)

    def gravar_dados(self, dados: list[dict]):
        if self.aws_helper is not None:
            self.aws_helper.send_data(dados)

        if self.save_locally:
            LocalFiles.salvar_local(dados)

    def reduzir_tamanho_arquivo(self, dados: list[dict]):
        blocos = []
        bloco_atual = []
        tamanho_atual = 0

        for d in dados:
            item_size_kb = ceil(len(json.dumps(d, ensure_ascii=False).encode('utf-8')) / 1024)

            if tamanho_atual + item_size_kb > 128 and bloco_atual:
                blocos.append(bloco_atual)
                bloco_atual = []
                tamanho_atual = 0

            bloco_atual.append(d)
            tamanho_atual += item_size_kb

        if bloco_atual:
            blocos.append(bloco_atual)
        return blocos


if __name__ == "__main__":
    print("GERADOR DE DADOS ALGAS")
    print("Versão 5.0\n")
    orq = OrquestradorDadosSensores()
    orq.geracao_continua()
