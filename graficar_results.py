import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# --- CONFIGURACIÓN ---
RESULTS_DIR = os.path.join(os.getcwd(), "results")
OUTPUT_IMAGE_TIME = "grafica_tiempo.png"
OUTPUT_IMAGE_RAM = "grafica_RAM.png"
OUTPUT_IMAGE_CPU = "grafica_CPU.png"
OUTPUT_IMAGE_BOXPLOT_TIME = "grafica_boxplot_tiempo.png"
OUTPUT_IMAGE_BOXPLOT_RAM = "grafica_boxplot_RAM.png"
OUTPUT_IMAGE_BOXPLOT_CPU = "grafica_boxplot_CPU.png"

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
    """carga de datos de RAM"""
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

def get_latest_data_CPU(root_dir):
    """carga de datos de CPU"""
    all_data = []
    if not os.path.exists(root_dir): return pd.DataFrame()

    for root, dirs, files in os.walk(root_dir):
        csv_files = [f for f in files if f.endswith(".csv")]
        if csv_files:
            full_paths = [os.path.join(root, f) for f in csv_files]
            latest_file = max(full_paths, key=os.path.getmtime)
            try:
                df = pd.read_csv(latest_file)
                
                if "CPU(%)" in df.columns:
                    df["CPU_MEAN"] = df["CPU(%)"]
                
                if "CPU_MEAN" in df.columns:
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
    print(f"\nGráfica de RAM guardada en: {os.path.abspath(OUTPUT_IMAGE_RAM)}")

def plot_CPU(df):
    if df.empty: return

    sns.set_theme(style="whitegrid")
    fig, ax = plt.subplots(figsize=(14, 8))

    # --- CREAR GRÁFICO ---
    chart = sns.barplot(
        data=df,
        x="CIRCUIT",
        y="CPU_MEAN",
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
    plt.title("Comparativa de Rendimiento (uso CPU)", fontsize=18, fontweight='bold', pad=20)
    plt.xlabel("Circuito", fontsize=14)
    plt.ylabel("CPU Promedio (%) - Log", fontsize=14)
    
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
    plt.savefig(OUTPUT_IMAGE_CPU, dpi=300)
    print(f"\nGráfica de CPU guardada en: {os.path.abspath(OUTPUT_IMAGE_CPU)}")

def plot_boxplot_time(df):
    """
    Genera un diagrama de caja y bigotes para la distribución del tiempo.
    """
    if df.empty:
        print("No hay datos para graficar el boxplot de tiempo.")
        return

    sns.set_theme(style="whitegrid")
    fig, ax = plt.subplots(figsize=(14, 8))

    # --- CREAR DIAGRAMA DE CAJA Y BIGOTES ---
    # Esto mostrará automáticamente la mediana, cuartiles y valores atípicos (outliers).
    chart = sns.boxplot(
        data=df,
        x="CIRCUIT",       # Eje X: Circuitos
        y="TIME_MEAN",     # Eje Y: Distribución del tiempo de las 10 iteraciones
        hue="FRAMEWORK",   # Agrupación por color para cada framework
        palette="Paired",  # Misma paleta de colores
        linewidth=1.5,     # Grosor de las líneas de la caja y bigotes
        fliersize=4,       # Tamaño de los puntos para los outliers
        ax=ax
    )

    # --- ESCALA LOGARÍTMICA ---
    # Mantenemos la escala logarítmica para visualizar mejor las diferencias
    chart.set_yscale("log")

    # Títulos y Etiquetas
    plt.title("Distribución del Tiempo de Ejecución (Escala Logarítmica)", fontsize=18, fontweight='bold', pad=20)
    plt.xlabel("Circuito", fontsize=14)
    plt.ylabel("Tiempo (segundos) - Log", fontsize=14)
    
    # Leyenda
    plt.legend(title="Framework", title_fontsize='12', fontsize='11', loc='upper left', bbox_to_anchor=(1, 1))

    # Ajuste de márgenes
    plt.margins(y=0.1)
    
    plt.tight_layout()
    # Guardar la imagen con el nuevo nombre
    plt.savefig(OUTPUT_IMAGE_BOXPLOT_TIME, dpi=300)
    print(f"\nGráfica de boxplot de tiempo guardada en: {os.path.abspath(OUTPUT_IMAGE_BOXPLOT_TIME)}")

def plot_boxplot_RAM(df):
    """
    Genera un diagrama de caja y bigotes para la distribución de RAM.
    """
    if df.empty:
        print("No hay datos para graficar el boxplot de tiempo.")
        return

    sns.set_theme(style="whitegrid")
    fig, ax = plt.subplots(figsize=(14, 8))

    # --- CREAR DIAGRAMA DE CAJA Y BIGOTES ---
    # Esto mostrará automáticamente la mediana, cuartiles y valores atípicos (outliers).
    chart = sns.boxplot(
        data=df,
        x="CIRCUIT",       # Eje X: Circuitos
        y="RAM_MEAN",     # Eje Y: Distribución del tiempo de las 10 iteraciones
        hue="FRAMEWORK",   # Agrupación por color para cada framework
        palette="Paired",  # Misma paleta de colores
        linewidth=1.5,     # Grosor de las líneas de la caja y bigotes
        fliersize=4,       # Tamaño de los puntos para los outliers
        ax=ax
    )

    # --- ESCALA LOGARÍTMICA ---
    # Mantenemos la escala logarítmica para visualizar mejor las diferencias
    chart.set_yscale("log")

    # Títulos y Etiquetas
    plt.title("Distribución de RAM de Ejecución (Escala Logarítmica)", fontsize=18, fontweight='bold', pad=20)
    plt.xlabel("Circuito", fontsize=14)
    plt.ylabel("RAM (MB) - Log", fontsize=14)
    
    # Leyenda
    plt.legend(title="Framework", title_fontsize='12', fontsize='11', loc='upper left', bbox_to_anchor=(1, 1))

    # Ajuste de márgenes
    plt.margins(y=0.1)
    
    plt.tight_layout()
    # Guardar la imagen con el nuevo nombre
    plt.savefig(OUTPUT_IMAGE_BOXPLOT_RAM, dpi=300)
    print(f"\nGráfica de boxplot de RAM guardada en: {os.path.abspath(OUTPUT_IMAGE_BOXPLOT_RAM)}")

def plot_boxplot_CPU(df):
    """
    Genera un diagrama de caja y bigotes para la distribución de CPU.
    """
    if df.empty:
        print("No hay datos para graficar el boxplot de CPU.")
        return

    sns.set_theme(style="whitegrid")
    fig, ax = plt.subplots(figsize=(14, 8))

    # --- CREAR DIAGRAMA DE CAJA Y BIGOTES ---
    # Esto mostrará automáticamente la mediana, cuartiles y valores atípicos (outliers).
    chart = sns.boxplot(
        data=df,
        x="CIRCUIT",       # Eje X: Circuitos
        y="CPU_MEAN",     # Eje Y: Distribución del tiempo de las 10 iteraciones
        hue="FRAMEWORK",   # Agrupación por color para cada framework
        palette="Paired",  # Misma paleta de colores
        linewidth=1.5,     # Grosor de las líneas de la caja y bigotes
        fliersize=4,       # Tamaño de los puntos para los outliers
        ax=ax
    )

    # --- ESCALA LOGARÍTMICA ---
    # Mantenemos la escala logarítmica para visualizar mejor las diferencias
    chart.set_yscale("log")

    # Títulos y Etiquetas
    plt.title("Distribución de CPU de Ejecución (Escala Logarítmica)", fontsize=18, fontweight='bold', pad=20)
    plt.xlabel("Circuito", fontsize=14)
    plt.ylabel("CPU (%) - Log", fontsize=14)
    
    # Leyenda
    plt.legend(title="Framework", title_fontsize='12', fontsize='11', loc='upper left', bbox_to_anchor=(1, 1))

    # Ajuste de márgenes
    plt.margins(y=0.1)
    
    plt.tight_layout()
    # Guardar la imagen con el nuevo nombre
    plt.savefig(OUTPUT_IMAGE_BOXPLOT_CPU, dpi=300)
    print(f"\nGráfica de boxplot de CPU guardada en: {os.path.abspath(OUTPUT_IMAGE_BOXPLOT_CPU)}")

if __name__ == "__main__":
    print("--- 1. CARGANDO DATOS COMPLETOS ---")
    df_full_time = get_latest_data_time(RESULTS_DIR)
    df_full_ram = get_latest_data_RAM(RESULTS_DIR)
    df_full_cpu = get_latest_data_CPU(RESULTS_DIR)

    if df_full_time.empty:
        print("Error: No se han encontrado datos.")
        exit()

    # Muestra qué circuitos hay disponibles para que puedas copiar y pegar
    circuitos_disponibles = df_full_time["CIRCUIT"].unique()
    print(f"\nCircuitos encontrados en los CSVs:\n{circuitos_disponibles}\n")

    # --- 2. CONFIGURACIÓN DE LISTAS ---
    # Rellena estas listas con los nombres exactos que te han salido arriba
    
    LISTA_SMALL = [
        
        "toffoli_n3", "adder_n4", "bell_n4", "qft_n4"
    ]

    LISTA_MEDIUM = [
        "seca_n11", "dnn_n16", "qec9xz_n17" , "bigadder_n18"
    ]

    # Diccionario para iterar automáticamente, comentar si solo se quiere 1
    configuraciones = {
        #"SMALL": LISTA_SMALL,
        "MEDIUM": LISTA_MEDIUM
    }

    for categoria, lista_nombres in configuraciones.items():
        print(f"\n--- PROCESANDO CATEGORÍA: {categoria} ---")
        
        if not lista_nombres:
            print(f"Saltando {categoria} (Lista vacía).")
            continue

        # Filtramos los DataFrames
        df_time_filtro = df_full_time[df_full_time["CIRCUIT"].isin(lista_nombres)]
        df_ram_filtro = df_full_ram[df_full_ram["CIRCUIT"].isin(lista_nombres)]
        df_cpu_filtro = df_full_cpu[df_full_cpu["CIRCUIT"].isin(lista_nombres)]

        if df_time_filtro.empty:
            print(f"No hay datos para la lista {categoria}. Revisa los nombres.")
            continue

        # Actualizamos Nombres de Archivo Globales para esta iteración
        OUTPUT_IMAGE_TIME = f"grafica_tiempo_{categoria}.png"
        OUTPUT_IMAGE_RAM = f"grafica_RAM_{categoria}.png"
        OUTPUT_IMAGE_CPU = f"grafica_CPU_{categoria}.png"
        OUTPUT_IMAGE_BOXPLOT_TIME = f"grafica_boxplot_tiempo_{categoria}.png"
        OUTPUT_IMAGE_BOXPLOT_RAM = f"grafica_boxplot_RAM_{categoria}.png"
        OUTPUT_IMAGE_BOXPLOT_CPU = f"grafica_boxplot_CPU_{categoria}.png"

        # Graficamos (Barras)
        plot_time(df_time_filtro)
        plot_RAM(df_ram_filtro)
        plot_CPU(df_cpu_filtro)

        # Graficamos (Boxplots)
        plot_boxplot_time(df_time_filtro)
        plot_boxplot_RAM(df_ram_filtro)
        plot_boxplot_CPU(df_cpu_filtro)