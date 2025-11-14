import subprocess
import os
import csv
from datetime import datetime

# Lista de frameworks
FRAMEWORKS = ["qiskit", "cirq", "pennylane", "myqlm", "tket"]

# Carpeta principal de resultados
RESULTS_DIR = os.path.join(os.path.dirname(os.getcwd()), "results")

def extract_metrics_from_txt(path_txt):
    """Extrae las métricas entre los delimitadores METRICS del archivo de salida."""
    metrics = {
        "qubits": None,
        "depth": None,
        "gate_1q": None,
        "gate_2q": None,
        "total_gates": None
    }

    inside = False

    with open(path_txt, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            if line == "# --- METRICS ---":
                inside = True
                continue
            if line == "# --- END_METRICS ---":
                break

            if inside:
                if "Qubits:" in line:
                    metrics["qubits"] = int(line.split(":")[1])
                elif "Depth:" in line:
                    metrics["depth"] = int(line.split(":")[1])
                elif "Gate_1q:" in line:
                    metrics["gate_1q"] = int(line.split(":")[1])
                elif "Gate_2q:" in line:
                    metrics["gate_2q"] = int(line.split(":")[1])
                elif "Total_gates:" in line:
                    metrics["total_gates"] = int(line.split(":")[1])

    return metrics

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
        txt_path = os.path.join(RESULTS_DIR, fw, circuito_base, f"{fw}_{circuito_base}.txt")

        # Extraer métricas del archivo .txt
        metrics = extract_metrics_from_txt(txt_path)

        csv_dir = os.path.join(RESULTS_DIR, fw, circuito_base)
        os.makedirs(csv_dir, exist_ok=True)

        fecha = datetime.now().strftime("%Y%m%d")
        hora = datetime.now().strftime("%H%M%S")

        # Nombre del archivo CSV
        csv_filename = f"{fecha}_{hora}_{fw}_{circuito_base}_{metrics['qubits']}_{0}.csv"
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
                fw, fecha, hora, circuito_base, metrics["qubits"],
                metrics["gate_1q"], metrics["gate_2q"], metrics["total_gates"],
                "N/A", "N/A",
                "N/A", "N/A", f"{dur:.2f}"
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
