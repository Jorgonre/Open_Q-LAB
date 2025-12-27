import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# --- CONFIGURACIÓN ---
RESULTS_DIR = os.path.join(os.getcwd(),"results")
OUTPUT_IMAGE = "grafica_tiempo.png"

def get_latest_data(root_dir):
    """
    Recorre las carpetas, coge solo el último CSV de cada una
    y unifica los datos en un solo DataFrame.
    """
    all_data = []

    if not os.path.exists(root_dir):
        print(f"Error: No se encuentra la carpeta '{root_dir}'")
        return pd.DataFrame()

    print(f"Leyendo datos desde: {root_dir}...")

    # Recorremos recursivamente
    for root, dirs, files in os.walk(root_dir):
        csv_files = [f for f in files if f.endswith(".csv")]
        
        if csv_files:
            # Construimos rutas completas
            full_paths = [os.path.join(root, f) for f in csv_files]
            
            # --- SELECCIÓN DEL ÚLTIMO ARCHIVO ---
            latest_file = max(full_paths, key=os.path.getmtime)
            
            try:
                df = pd.read_csv(latest_file)

                if "TOTAL-TIME(s)" in df.columns:
                    df["TIME_MEAN"] = df["TOTAL-TIME(s)"]
                
                # Solo añadimos si encontramos la columna de tiempo válida
                if "TIME_MEAN" in df.columns:
                    all_data.append(df)
                    print(f"  -> Leído: {os.path.basename(latest_file)}")
                    
            except Exception as e:
                print(f"  [!] Error leyendo {latest_file}: {e}")

    if not all_data:
        return pd.DataFrame()

    return pd.concat(all_data, ignore_index=True)

def plot_bars(df):
    """Genera la gráfica de barras con la media."""
    if df.empty:
        print("No hay datos para graficar.")
        return

    # Estilo limpio
    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(12, 6))

    # --- CREACIÓN DEL GRÁFICO ---
    # Seaborn calcula la MEDIA automáticamente al agrupar los datos de las 10 iteraciones.
    chart = sns.barplot(
        data=df,
        x="CIRCUIT",       # Eje X: Circuitos
        y="TIME_MEAN",     # Eje Y: Tiempo (se calcula el promedio automáticamente)
        hue="FRAMEWORK",   # Agrupación por color
        errorbar=None,     # <--- IMPORTANTE: Quita las líneas de error, deja solo la barra
        palette="viridis", # Colores
        edgecolor="black", # Borde negro para que se vea mejor
        alpha=0.9
    )

    # Etiquetas y Títulos
    plt.title("Tiempo de Ejecución Promedio (Media de 10 iteraciones)", fontsize=16, fontweight='bold', pad=15)
    plt.xlabel("Circuito", fontsize=12)
    plt.ylabel("Tiempo (segundos)", fontsize=12)
    plt.legend(title="Framework", loc='upper left', bbox_to_anchor=(1, 1))

    # Ajuste para que no se corte la leyenda
    plt.tight_layout()

    # Guardar
    plt.savefig(OUTPUT_IMAGE, dpi=300)
    print(f"\nGráfica guardada exitosamente en: {os.path.abspath(OUTPUT_IMAGE)}")

if __name__ == "__main__":
    # 1. Obtener datos
    df_results = get_latest_data(RESULTS_DIR)
    
    # 2. Verificar y Graficar
    if not df_results.empty:
        # Imprimir en consola los valores numéricos de la media para comprobar
        print("\n--- Valores Promedio Calculados ---")
        print(df_results.groupby(["FRAMEWORK", "CIRCUIT"])["TIME_MEAN"].mean())
        print("-----------------------------------")
        
        plot_bars(df_results)
    else:
        print("No se encontraron archivos CSV válidos.")