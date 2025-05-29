import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd
from glob import glob

def executar():

    # == Carregamento e formatação do arquivo
    print("Lendo log...\n")
    logs = glob("../../logs/*")
    logs.sort()
    filename = logs[-1]

    df = pd.read_json(filename).sort_values("instant")
    df['instant'] = pd.to_datetime(df['instant'], format='ISO8601')

    df = df[df["sensor"] == "LV25-P"].copy()
    df["hour"] = df["instant"].dt.hour

    fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(5, 18))
    fig.suptitle('Voltagem ao passar do tempo', fontsize=16, y=1.05)

    cenarios = ["TERRIVEL", "NORMAL", "EXCEPCIONAL"]
    for i, c in enumerate(cenarios):
        ALTA_TENSAO = 24000
        BAIXA_TENSAO = 22000

        dataf = df[df["scenery"] == c]

        # == Criação do gráfico
        print(f"Criando gráfico {c}...")
        axes[i].scatter(
            x=dataf['hour'], y=dataf['value'], edgecolors='b',
            alpha=0.7, # Optional: Transparency
            s=60 # Optional: Marker size
        )

        # == Formatação
        print("\tFormatando...")
        axes[i].set_title(f'Cenário {c.lower()}', fontsize=14)

        axes[i].set_xlabel('Horário do dia', fontsize=12)
        axes[i].set_ylabel('Voltagem (volts)', fontsize=12)
        axes[i].set_ylim(20000, 26000)

        axes[i].axhline(y=ALTA_TENSAO, color='red', linestyle='--', linewidth=2, label=f'Alta tensão ({ALTA_TENSAO}v)')
        axes[i].axhline(y=BAIXA_TENSAO, color='#b8a907', linestyle='--', linewidth=2, label=f'Baixa tensão ({BAIXA_TENSAO}v)')

        axes[i].grid(True, linestyle='--', alpha=0.5)  # Optional: Grid
        axes[i].tick_params(axis='x', rotation=45) # Rotate x-axis labels for better readablity


        # == Legenda
        qtd_alta_tens = dataf[dataf["value"] > ALTA_TENSAO]["value"].count()
        patch_alta_tens = mpatches.Patch(
            color='red', alpha=0.3, label=f'Alta tensão ({ALTA_TENSAO}V)\nOcorrências: {qtd_alta_tens}'
        )

        qtd_baixa_tens = dataf[dataf["value"] < BAIXA_TENSAO]["value"].count()
        patch_baixa_tens = mpatches.Patch(
            color='#b8a907', alpha=0.3, label=f'Baixa tensão ({BAIXA_TENSAO}V)\nOcorrências: {qtd_baixa_tens}'
        )

        axes[i].legend(handles=[patch_alta_tens, patch_baixa_tens], loc='upper left', framealpha=1)
        print("\t[!]Feito!\n")

    print("Salvando como imagem...")
    plt.tight_layout()
    plt.savefig('./graphs/grafico.png', dpi=300, bbox_inches='tight')
    print("[!] Sucesso!")

if __name__ == "__main__":
    executar()