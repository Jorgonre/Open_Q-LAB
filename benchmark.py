import subprocess
import os
import csv
from datetime import datetime

# Lista de frameworks que vamos a probar
FRAMEWORKS = ["qiskit", "cirq", "pennylane", "myqlm"]

# Carpeta donde se guardarán los resultados
RESULTS_DIR = os.path.join(os.path.dirname(os.getcwd()), "results")

def ensure_results_dir():
    """Crea la carpeta 'results' si no existe."""
    os.makedirs(RESULTS_DIR, exist_ok=True)

def run_framework():
    """Ejecuta el benchmark de un framework y guarda su salida."""
    print(f"\nEjecutando benchmark...\n")
    start_time = datetime.now()

    # Ruta del script dentro de cada carpeta
    script_path = os.path.join("circuito_prueba.py")

    if not os.path.exists(script_path):
        print(f"No se encontró {script_path}, saltando...")
        return None

    try:
        # Ejecuta el script y captura la salida
        result = subprocess.run(
            ["python", script_path],
            capture_output=True,
            text=True,
            check=True
        )

        duration = (datetime.now() - start_time).total_seconds()
        print(f"Completado en {duration:.2f}s\n")

        # Guardamos la salida en un archivo dentro de /results
        result_file = os.path.join(RESULTS_DIR, f"{os.path.basename(os.getcwd())}_result.txt")
        with open(result_file, "w") as f:
            f.write(f"Benchmark\n")
            f.write(f"Duración: {duration:.2f}s\n\n")
            f.write(result.stdout)

        return duration

    except subprocess.CalledProcessError as e:
        print(f"Error ejecutando {script_path}:\n{e.stderr}")
        return None

def save_to_csv(resultados):
    """Guarda los resultados en un archivo CSV dentro de /results."""
    csv_file = os.path.join(RESULTS_DIR, "benchmark_results.csv")
    file_exists = os.path.exists(csv_file)

    with open(csv_file, "a", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)

        # Si el archivo no existía, escribir encabezados
        if not file_exists:
            writer.writerow(["Framework", "Duración (s)", "Fecha y hora"])

        for fw, dur in resultados.items():
            writer.writerow([fw, f"{dur:.2f}", datetime.now().strftime("%Y-%m-%d %H:%M:%S")])

    print(f"\nResultados guardados en CSV: {csv_file}")

def main():
    print("=== BENCHMARK DE FRAMEWORKS CUÁNTICOS ===")
    ensure_results_dir()

    resultados = {}

    #for fw in FRAMEWORKS:
    duracion = run_framework()
    if duracion is not None:
        framework_name = os.path.basename(os.getcwd())
        resultados[framework_name] = duracion

    print("\n=== RESUMEN FINAL ===")
    for fw, dur in resultados.items():
        print(f"{fw}: {dur:.2f} segundos")

    print(f"\nResultados guardados en: {os.path.abspath(RESULTS_DIR)}")
    
    save_to_csv(resultados)


if __name__ == "__main__":
    main()
