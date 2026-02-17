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
OUTPUT_IMAGE_GATES = "grafica_gates.png"

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

def get_latest_data_gates(root_dir):
    """carga de datos de conteo de puertas"""
    all_data = []
    if not os.path.exists(root_dir): return pd.DataFrame()

    for root, dirs, files in os.walk(root_dir):
        csv_files = [f for f in files if f.endswith(".csv")]
        if csv_files:
            full_paths = [os.path.join(root, f) for f in csv_files]
            latest_file = max(full_paths, key=os.path.getmtime)
            try:
                df = pd.read_csv(latest_file)
                
                # Buscamos columnas de puertas.
                cols_to_check = ["1-GATE", "2-GATES", "3-GATES"]
                
                # Verificar si al menos una columna de interés existe
                if any(col in df.columns for col in cols_to_check):
                    # Rellenar con 0 las que falten para evitar errores
                    for col in cols_to_check:
                        if col not in df.columns:
                            df[col] = 0
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

    # --- LÍNEAS DISCONTINUAS SEPARADORAS ---
    num_circuitos = len(df["CIRCUIT"].unique())
    for i in range(num_circuitos - 1):
        ax.axvline(x=i + 0.5, color='gray', linestyle='--', alpha=0.5)

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
        print("No hay datos para graficar el boxplot de RAM.")
        return

    sns.set_theme(style="whitegrid")
    fig, ax = plt.subplots(figsize=(14, 8))

    # --- ORDENAR Y CREAR EJE X COMBINADO ---
    df_sorted = df.sort_values(by=["CIRCUIT", "FRAMEWORK"])
    
    df_sorted["COMBINED"] = df_sorted["CIRCUIT"] + "|" + df_sorted["FRAMEWORK"]

    # --- CREAR DIAGRAMA DE CAJA Y BIGOTES ---
    chart = sns.boxplot(
        data=df_sorted,
        x="COMBINED",
        y="RAM_MEAN",
        hue="FRAMEWORK",
        palette="Paired",
        dodge=False,
        linewidth=1.5,
        fliersize=4,
        ax=ax
    )

    # --- ESCALA LOGARÍTMICA ---
    chart.set_yscale("log")

    # --- ETIQUETAS DE FRAMEWORKS (Eje X) ---
    unique_combined = df_sorted["COMBINED"].unique()
    # Separamos por el símbolo "|" y cogemos la parte derecha (el framework)
    labels = [val.split("|")[1] for val in unique_combined]
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels, rotation=45, ha='center', fontsize=10)

    # --- ETIQUETAS DE CIRCUITOS Y LÍNEAS SEPARADORAS ---
    unique_circuits = df_sorted["CIRCUIT"].unique()
    start = 0
    for circuit in unique_circuits:
        count = len(df_sorted[df_sorted["CIRCUIT"] == circuit]["COMBINED"].unique())
        end = start + count
        center = (start + (end - 1)) / 2
        
        ax.text(center, -0.15, circuit, ha='center', va='top', 
                transform=ax.get_xaxis_transform(), 
                fontsize=12, fontweight='bold', color='#222222')
        
        if end < len(unique_combined):
            ax.axvline(x=end - 0.5, color='gray', linestyle='--', alpha=0.5)
            
        start = end

    # Títulos y Ejes
    plt.title("Distribución de RAM de Ejecución (Escala Logarítmica)", fontsize=18, fontweight='bold', pad=20)
    plt.xlabel("")
    plt.ylabel("RAM (MB) - Log", fontsize=14)
    
    # Leyenda
    plt.legend(title="Framework", title_fontsize='12', fontsize='11', loc='upper left', bbox_to_anchor=(1, 1))

    # Ajuste de márgenes
    plt.subplots_adjust(bottom=0.20)
    
    plt.tight_layout()
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

    # --- LÍNEAS DISCONTINUAS SEPARADORAS ---
    num_circuitos = len(df["CIRCUIT"].unique())
    for i in range(num_circuitos - 1):
        ax.axvline(x=i + 0.5, color='gray', linestyle='--', alpha=0.5)

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

def plot_gate_composition(df):
    """
    Genera un histograma apilado (Stacked Bar Chart) optimizado:
    - Escala LOGARÍTMICA ajustada para que se vean valores bajos.
    """
    if df.empty:
        print("No hay datos para graficar la composición de puertas.")
        return

    sns.set_theme(style="whitegrid")
    
    # Nombres de columnas en tu CSV
    cols = ["1-GATE", "2-GATES", "3-GATES"]
    
    # Asegurarnos de que existen en el DF filtrado
    for col in cols:
        if col not in df.columns:
            df[col] = 0

    # 1. Agrupar datos reales
    df_grouped = df.groupby(["CIRCUIT", "FRAMEWORK"])[cols].mean().reset_index()
    
    # Obtenemos todos los circuitos únicos y todos los frameworks únicos
    todos_circuitos = df_grouped["CIRCUIT"].unique()
    todos_frameworks = ["qiskit", "cirq", "pennylane", "myqlm", "tket"] 

    # Creamos un DataFrame con todas las combinaciones posibles
    idx = pd.MultiIndex.from_product([todos_circuitos, todos_frameworks], names=["CIRCUIT", "FRAMEWORK"])
    df_completo = pd.DataFrame(index=idx).reset_index()

    # Hacemos un "merge" (unión) con los datos reales. 
    # Lo que no existía se rellenará con NaN, y luego lo cambiamos a 0.
    df_grouped = pd.merge(df_completo, df_grouped, on=["CIRCUIT", "FRAMEWORK"], how="left").fillna(0)

    # Ordenamos para que los frameworks del mismo circuito estén juntos
    df_grouped = df_grouped.sort_values(by=["CIRCUIT", "FRAMEWORK"])

    # Necesitamos un índice numérico para manipular la posición de los textos
    x_pos = np.arange(len(df_grouped))
    data_plot = df_grouped[cols]
    
    # Crear la figura (20 de ancho para que quepan todos con los frameworks vacíos)
    fig, ax = plt.subplots(figsize=(20, 7)) 
    
    data_plot.plot(kind='bar', stacked=True, ax=ax, width=0.8, 
                   edgecolor="black", linewidth=0.8, alpha=0.95, 
                   colormap="Paired", log=True)

    ax.set_ylim(bottom=1)
    
    # Etiquetas de Frameworks
    ax.set_xticks(x_pos)
    ax.set_xticklabels(df_grouped["FRAMEWORK"], rotation=45, ha='center', fontsize=9)

    # Etiquetas de Circuitos (Agrupadas debajo)
    start = 0
    for circuit in todos_circuitos:
        count = len(df_grouped[df_grouped["CIRCUIT"] == circuit])
        end = start + count
        center = (start + (end - 1)) / 2
        
        ax.text(center, -0.18, circuit, ha='center', va='top', 
                transform=ax.get_xaxis_transform(), 
                fontsize=11, fontweight='bold', color='#222222')
        
        # Línea separadora vertical sutil
        if end < len(df_grouped):
            ax.axvline(x=end - 0.5, color='gray', alpha=0.6)
            
        start = end

    # Títulos y Ejes
    plt.title("Composición de Puertas Cuánticas (Escala Logarítmica)", fontsize=16, fontweight='bold', pad=15)
    plt.ylabel("Número de Puertas (Log)", fontsize=12)
    plt.xlabel("") # Sin etiqueta X genérica
    
    # Leyenda
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles, ["1 Qubit", "2 Qubits", "3 Qubits"], 
              title="Tipo de Puerta", title_fontsize='10', fontsize='9', loc='upper left')

    # Añadir valores numéricos dentro de las barras
    for c in ax.containers:
        labels = [int(v) if v > 0 else "" for v in c.datavalues]
        
        texts = ax.bar_label(c, labels=labels, label_type='center', fontsize=7, color='black', weight='bold')
        
        for text in texts:
            val_str = text.get_text()
            if val_str: # Si hay número
                valor = int(val_str)
                
                if valor == 384:
                    text.set_rotation(0) # En horizontal
                else:
                    text.set_rotation(90) # Todos los demás en vertical

    # Ajuste de márgenes inferior
    plt.subplots_adjust(bottom=0.15) # He subido esto a 0.15 para asegurar que no se corta el texto
    
    plt.tight_layout()
    plt.savefig(OUTPUT_IMAGE_GATES, dpi=300)
    print(f"\nGráfica de composición de puertas guardada en: {os.path.abspath(OUTPUT_IMAGE_GATES)}")

if __name__ == "__main__":
    print("--- 1. CARGANDO DATOS COMPLETOS ---")
    df_full_time = get_latest_data_time(RESULTS_DIR)
    df_full_ram = get_latest_data_RAM(RESULTS_DIR)
    df_full_cpu = get_latest_data_CPU(RESULTS_DIR)
    df_full_gates = get_latest_data_gates(RESULTS_DIR)

    if df_full_time.empty:
        print("Error: No se han encontrado datos.")
        exit()

    circuitos_disponibles = df_full_time["CIRCUIT"].unique()
    print(f"\nCircuitos encontrados en los CSVs:\n{circuitos_disponibles}\n")

    if not df_full_gates.empty:
        print("\n--- GENERANDO GRÁFICA DE PUERTAS (TODOS LOS CIRCUITOS) ---")
        OUTPUT_IMAGE_GATES = "grafica_gates_todas.png" # Nombre del archivo global
        plot_gate_composition(df_full_gates) # Le pasamos TODOS los datos sin filtrar

    # --- 2. CONFIGURACIÓN DE LISTAS PARA LAS DEMÁS GRÁFICAS ---
    
    LISTA_SMALL = [
        "toffoli_n3", "adder_n4", "bell_n4", "qft_n4"
    ]

    LISTA_MEDIUM = [
        "seca_n11", "dnn_n16", "qec9xz_n17" , "bigadder_n18"
    ]

    LISTA_BIG = [
        "bigadder_n28"
    ]

    # Diccionario para iterar automáticamente, comentar si solo se quiere 1
    configuraciones = {
        "SMALL": LISTA_SMALL,
        "MEDIUM": LISTA_MEDIUM,
        "BIG": LISTA_BIG
    }

    for categoria, lista_nombres in configuraciones.items():
        print(f"\n--- PROCESANDO CATEGORÍA: {categoria} (Tiempo, RAM, CPU) ---")
        
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