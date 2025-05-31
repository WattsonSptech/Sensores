import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd
from glob import glob
from interfaces.EnumZonas import EnumZonas

def executar():

    # == Carregamento e formatação do arquivo
    print("Lendo log...\n")
    logs = glob("../../logs/*")
    logs.sort()
    filename = logs[-1]

    zones = pd.Categorical(sorted([z.name for z in EnumZonas]))

    df = pd.read_json(filename).sort_values("instant")[["value", "zone"]]

    df = df.groupby("zone").agg(zone_value=("value", "mean")).reset_index().sort_values("zone")
    df['zone'] = pd.Categorical(df['zone'], categories=zones, ordered=True)

    ibge = pd.DataFrame([{"zone": z.name, "population (millions)": z.value} for z in EnumZonas]).sort_values("zone")
    ibge['zone'] = pd.Categorical(ibge['zone'], categories=zones, ordered=True)

    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(10, 4))

    axes[0].plot(df['zone'], df['zone_value'], marker='o')
    axes[0].tick_params(axis='x', rotation=45)
    axes[0].set_title("Média")

    axes[1].bar(ibge['zone'], ibge['population (millions)'])
    axes[1].set_ylim(1, 5)
    axes[1].set_title("População SP")
    axes[1].tick_params(axis='x', rotation=45)

    print("Salvando como imagem...")
    plt.tight_layout(pad=2.0)
    plt.savefig('./graphs/teste.png', dpi=300, bbox_inches='tight')
    print("[!] Sucesso!")

if __name__ == "__main__":
    executar()