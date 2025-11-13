import subprocess
import os
import csv
from datetime import datetime

# Lista de frameworks
FRAMEWORKS = ["qiskit", "cirq", "pennylane", "myqlm", "tket"]

# Carpeta principal de resultados
RESULTS_DIR = os.path.join(os.path.dirname(os.getcwd()), "results")

# === CONFIGURACIÓN ===
NUM_QBITS = 4
NUM_ITERATIONS = 10
# ======================

def ensure_results_dir():
    """Crea la carpeta 'results' si no existe."""
    os.makedirs(RESULTS_DIR, exist_ok=True)

def run_framework(circuito_nombre):
    """Ejecuta el benchmark y guarda la salida."""
    print(f"\nEjecutando benchmark...\n")
    start_time = datetime.now()

    script_path = os.path.join(circuito_nombre)
    if not os.path.exists(script_path):
        print(f"No se encontró {script_path}, saltando...")
        return None

    try:
        result = subprocess.run(
            ["python", script_path],
            capture_output=True,
            text=True,
            check=True
        )

        duration = (datetime.now() - start_time).total_seconds()
        print(f"Completado en {duration:.2f}s\n")

        framework_name = os.path.basename(os.getcwd())
        circuito_base = os.path.splitext(circuito_nombre)[0]
        framework_result_dir = os.path.join(RESULTS_DIR, framework_name, circuito_base)
        os.makedirs(framework_result_dir, exist_ok=True)

        # Guardar salida completa
        result_file = os.path.join(framework_result_dir, f"{framework_name}_{circuito_base}.txt")
        with open(result_file, "w") as f:
            f.write(f"Benchmark {framework_name} - {circuito_nombre}\n")
            f.write(f"Duración: {duration:.2f}s\n\n")
            f.write(result.stdout)

        return duration

    except subprocess.CalledProcessError as e:
        print(f"Error ejecutando {script_path}:\n{e.stderr}")
        return None


def save_to_csv(resultados, circuito_nombre):
    """Guarda resultados con el formato del Excel de referencia."""
    for fw, dur in resultados.items():
        circuito_base = os.path.splitext(circuito_nombre)[0]
        csv_dir = os.path.join(RESULTS_DIR, fw, circuito_base)
        os.makedirs(csv_dir, exist_ok=True)

        # Fecha y hora sin guiones
        fecha = datetime.now().strftime("%Y%m%d")
        hora = datetime.now().strftime("%H%M%S")

        # Nombre del archivo CSV
        csv_filename = f"{fecha}_{hora}_{fw}_{circuito_base}_{NUM_QBITS}_{NUM_ITERATIONS}.csv"
        csv_path = os.path.join(csv_dir, csv_filename)

        # Crear y escribir el CSV con el formato del Excel
        with open(csv_path, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([
                "FRAMEWORK", "DATE", "HOUR", "CIRCUIT", "QUBITS",
                "1-GATE", "2-GATES", "TOTAL-GATES",
                "RAM", "CPU",
                "BUILD-TIME", "TRANSPILE-TIME", "TOTAL-TIME"
            ])

            writer.writerow([
                fw, fecha, hora, circuito_base, NUM_QBITS,
                "N/A", "N/A", "N/A",  # Gates (rellenables después)
                "N/A", "N/A",         # RAM y CPU
                "N/A", "N/A", f"{dur:.2f}"  # Tiempos
            ])

        print(f"Resultado guardado en: {csv_path}")


def main():
    print("=== BENCHMARK DE FRAMEWORKS CUÁNTICOS ===")
    ensure_results_dir()

    resultados = {}
    circuitos = ["circuito_prueba.py", "adder_n4.py"]

    for circuito in circuitos:
        duracion = run_framework(circuito)
        if duracion is not None:
            framework_name = os.path.basename(os.getcwd())
            resultados[framework_name] = duracion

        print("\n=== RESUMEN PARCIAL ===")
        for fw, dur in resultados.items():
            print(f"{fw}: {dur:.2f} segundos")

        save_to_csv(resultados, circuito)

    print(f"\nResultados guardados en: {os.path.abspath(RESULTS_DIR)}")


if __name__ == "__main__":
    main()
