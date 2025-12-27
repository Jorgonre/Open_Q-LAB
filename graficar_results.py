import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# --- CONFIGURACIÓN ---
RESULTS_DIR = os.path.join(os.getcwd(), "results")
OUTPUT_IMAGE_TIME = "grafica_tiempo.png"
OUTPUT_IMAGE_RAM = "grafica_RAM.png"

def get_latest_data_time(root_dir):
    """carga de datos de total time"""
    all_data = []
    if not os.path.exists(root_dir): return pd.DataFrame()

    for root, dirs, files in os.walk(root_dir):
        csv_files = [f for f in files if f.endswith(".csv")]
        if csv_files:
            full_paths = [os.path.join(root, f) for f in csv_files]
            latest_file = max(full_paths, key=os.path.getmtime)
            try:
                df = pd.read_csv(latest_file)
                
                if "TOTAL-TIME(s)" in df.columns:
                    df["TIME_MEAN"] = df["TOTAL-TIME(s)"]
                
                if "TIME_MEAN" in df.columns:
                    all_data.append(df)
            except Exception: pass

    if not all_data: return pd.DataFrame()
    return pd.concat(all_data, ignore_index=True)

def get_latest_data_RAM(root_dir):
    """carga de datos de total time"""
    all_data = []
    if not os.path.exists(root_dir): return pd.DataFrame()

    for root, dirs, files in os.walk(root_dir):
        csv_files = [f for f in files if f.endswith(".csv")]
        if csv_files:
            full_paths = [os.path.join(root, f) for f in csv_files]
            latest_file = max(full_paths, key=os.path.getmtime)
            try:
                df = pd.read_csv(latest_file)
                
                if "RAM(MB)" in df.columns:
                    df["RAM_MEAN"] = df["RAM(MB)"]
                
                if "RAM_MEAN" in df.columns:
                    all_data.append(df)
            except Exception: pass

    if not all_data: return pd.DataFrame()
    return pd.concat(all_data, ignore_index=True)

def plot_time(df):
    if df.empty: return

    sns.set_theme(style="whitegrid")
    fig, ax = plt.subplots(figsize=(14, 8))

    # --- CREAR GRÁFICO ---
    chart = sns.barplot(
        data=df,
        x="CIRCUIT",
        y="TIME_MEAN",
        hue="FRAMEWORK",
        errorbar=None,
        palette="Paired",
        edgecolor="black",
        alpha=0.9,
        ax=ax
    )

    # --- ESCALA LOGARÍTMICA ---
    chart.set_yscale("log")

    # Títulos
    plt.title("Comparativa de Rendimiento (Tiempo total)", fontsize=18, fontweight='bold', pad=20)
    plt.xlabel("Circuito", fontsize=14)
    plt.ylabel("Tiempo Promedio (segundos) - Log", fontsize=14)
    
    # Leyenda
    plt.legend(title="Framework", title_fontsize='12', fontsize='11', loc='upper left', bbox_to_anchor=(1, 1))

    # --- ETIQUETAS DE DATOS ---
    # Ponemos el número exacto encima de cada barra
    for container in chart.containers:
        # Formateamos el número: si es < 0.1 usamos 3 decimales, si no 2.
        labels = [f'{v:.3f}' if v < 0.1 else f'{v:.2f}' for v in container.datavalues]
        chart.bar_label(container, labels=labels, padding=3, fontsize=9, rotation=45)

    # Añadir un margen extra arriba para que los números no se corten
    plt.margins(y=0.1)
    
    plt.tight_layout()
    plt.savefig(OUTPUT_IMAGE_TIME, dpi=300)
    print(f"\nGráfica de tiempo guardada en: {os.path.abspath(OUTPUT_IMAGE_TIME)}")

def plot_RAM(df):
    if df.empty: return

    sns.set_theme(style="whitegrid")
    fig, ax = plt.subplots(figsize=(14, 8))

    # --- CREAR GRÁFICO ---
    chart = sns.barplot(
        data=df,
        x="CIRCUIT",
        y="RAM_MEAN",
        hue="FRAMEWORK",
        errorbar=None,
        palette="Paired",
        edgecolor="black",
        alpha=0.9,
        ax=ax
    )

    # --- ESCALA LOGARÍTMICA ---
    chart.set_yscale("log")

    # Títulos
    plt.title("Comparativa de Rendimiento (uso RAM)", fontsize=18, fontweight='bold', pad=20)
    plt.xlabel("Circuito", fontsize=14)
    plt.ylabel("RAM Promedio (MB) - Log", fontsize=14)
    
    # Leyenda
    plt.legend(title="Framework", title_fontsize='12', fontsize='11', loc='upper left', bbox_to_anchor=(1, 1))

    # --- ETIQUETAS DE DATOS ---
    # Ponemos el número exacto encima de cada barra
    for container in chart.containers:
        # Formateamos el número: si es < 0.1 usamos 3 decimales, si no 2.
        labels = [f'{v:.3f}' if v < 0.1 else f'{v:.2f}' for v in container.datavalues]
        chart.bar_label(container, labels=labels, padding=3, fontsize=9, rotation=45)

    # Añadir un margen extra arriba para que los números no se corten
    plt.margins(y=0.1)
    
    plt.tight_layout()
    plt.savefig(OUTPUT_IMAGE_RAM, dpi=300)
    print(f"\nGráfica de tiempo guardada en: {os.path.abspath(OUTPUT_IMAGE_RAM)}")

if __name__ == "__main__":
    df_results_time = get_latest_data_time(RESULTS_DIR)
    df_results_RAM = get_latest_data_RAM(RESULTS_DIR)
    if not df_results_time.empty:
        plot_time(df_results_time)
    else:
        print("No hay datos.")
    if not df_results_RAM.empty:
        plot_RAM(df_results_RAM)
    else:
        print("No hay datos.")