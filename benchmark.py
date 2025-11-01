import subprocess
import os
from datetime import datetime

# Lista de frameworks que vamos a probar
FRAMEWORKS = ["qiskit", "cirq", "pennylane", "myqlm"]

# Carpeta donde se guardarán los resultados
RESULTS_DIR = "results"

def ensure_results_dir():
    """Crea la carpeta 'results' si no existe."""
    os.makedirs(RESULTS_DIR, exist_ok=True)

def run_framework(framework):
    """Ejecuta el benchmark de un framework y guarda su salida."""
    print(f"\nEjecutando benchmark para {framework}...\n")
    start_time = datetime.now()

    # Ruta del script dentro de cada carpeta
    script_path = os.path.join(framework, "adder_n4.py")

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
        print(f"{framework} completado en {duration:.2f}s\n")

        # Guardamos la salida en un archivo dentro de /results
        result_file = os.path.join(RESULTS_DIR, f"{framework}_result.txt")
        with open(result_file, "w") as f:
            f.write(f"Benchmark de {framework}\n")
            f.write(f"Duración: {duration:.2f}s\n\n")
            f.write(result.stdout)

        return duration

    except subprocess.CalledProcessError as e:
        print(f"Error ejecutando {framework}:\n{e.stderr}")
        return None


def main():
    print("=== BENCHMARK DE FRAMEWORKS CUÁNTICOS ===")
    ensure_results_dir()

    resultados = {}

    for fw in FRAMEWORKS:
        duracion = run_framework(fw)
        if duracion is not None:
            resultados[fw] = duracion

    print("\n=== RESUMEN FINAL ===")
    for fw, dur in resultados.items():
        print(f"{fw}: {dur:.2f} segundos")

    print(f"\nResultados guardados en: {os.path.abspath(RESULTS_DIR)}")


if __name__ == "__main__":
    main()
