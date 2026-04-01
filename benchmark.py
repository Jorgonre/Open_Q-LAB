import subprocess
import os
import csv
from datetime import datetime
import psutil

# --- CONFIGURACIÓN ---
FRAMEWORKS = ["qiskit", "cirq", "pennylane", "myqlm", "tket"]
NUM_ITERATIONS = 10
# ---------------------

# Carpeta principal de resultados
RESULTS_DIR = os.path.join(os.path.dirname(os.getcwd()), "results")

def extract_metrics_from_txt(path_txt):
    """Extrae las métricas entre los delimitadores METRICS del archivo de salida."""
    metrics = {
        "qubits": None, "depth": None, "gate_1q": None, "gate_2q": None, "gate_3q": 0,
        "total_gates": None, "build_time": None, "transpile_execution_time": None,
        "total_time": None, "cpu_usage": None, "ram_usage_mb": None
    }

    inside = False
    if not os.path.exists(path_txt):
        return metrics

    with open(path_txt, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line == "# --- METRICS ---":
                inside = True
                continue
            if line == "# --- END_METRICS ---":
                break
            
            if inside:
                try:
                    parts = line.split(":")
                    if len(parts) < 2: continue
                    val = parts[1].strip()
                    
                    if "Qubits" in line: metrics["qubits"] = int(val)
                    elif "Depth" in line: metrics["depth"] = int(val)
                    elif "Gate_1q" in line: metrics["gate_1q"] = int(val)
                    elif "Gate_2q" in line: metrics["gate_2q"] = int(val)
                    elif "Gate_3q" in line: metrics["gate_3q"] = int(val)
                    elif "Total_gates" in line: metrics["total_gates"] = int(val)
                    elif "Build_time" in line: metrics["build_time"] = float(val)
                    elif "Transpile_execution_time" in line: metrics["transpile_execution_time"] = float(val)
                    elif "Total_time" in line: metrics["total_time"] = float(val)
                    elif "CPU_usage" in line: metrics["cpu_usage"] = float(val)
                    elif "RAM_usage_MB" in line: metrics["ram_usage_mb"] = float(val)
                except ValueError:
                    continue
    return metrics

def ensure_results_dir():
    """Crea la carpeta 'results' si no existe."""
    os.makedirs(RESULTS_DIR, exist_ok=True)

def run_framework(circuito_nombre, iteration_idx):
    """Ejecuta el benchmark y guarda la salida en un txt temporal (que se sobrescribe)."""
    print(f"   > Ejecutando iteración {iteration_idx + 1}/{NUM_ITERATIONS}...")
    start_time = datetime.now()

    script_path = os.path.join(circuito_nombre)
    if not os.path.exists(script_path):
        print(f"No se encontró {script_path}, saltando...")
        return None

    try:
        # Ejecutar script
        result = subprocess.run(
            ["python", script_path],
            capture_output=True,
            text=True,
            check=True
        )

        duration = (datetime.now() - start_time).total_seconds()

        framework_name = os.path.basename(os.getcwd())
        circuito_base = os.path.splitext(circuito_nombre)[0]
        framework_result_dir = os.path.join(RESULTS_DIR, framework_name, circuito_base)
        os.makedirs(framework_result_dir, exist_ok=True)

        # Guardar salida completa (se sobrescribe en cada iteración para ahorrar espacio o tener el último log)
        result_file = os.path.join(framework_result_dir, f"{framework_name}_{circuito_base}_last_run.txt")
        with open(result_file, "w") as f:
            f.write(f"Benchmark {framework_name} - {circuito_nombre} - Iteration {iteration_idx+1}\n")
            f.write(f"Duración script python: {duration:.2f}s\n\n")
            f.write(result.stdout)

        return result_file

    except subprocess.CalledProcessError as e:
        print(f"Error ejecutando {script_path}:\n{e.stderr}")
        return None

def save_batch_to_csv(lista_metricas, framework_name, circuito_nombre):
    """
    Recibe una lista de diccionarios (uno por iteración) y guarda todo en un solo CSV.
    """
    if not lista_metricas:
        return

    circuito_base = os.path.splitext(circuito_nombre)[0]
    csv_dir = os.path.join(RESULTS_DIR, framework_name, circuito_base)
    os.makedirs(csv_dir, exist_ok=True)

    # Fecha y hora del inicio del batch para el nombre del archivo
    fecha = datetime.now().strftime("%Y%m%d")
    hora = datetime.now().strftime("%H%M%S")
    
    # Tomamos los qubits de la primera iteración válida para el nombre del archivo
    qubits_val = lista_metricas[0]["qubits"] if lista_metricas[0]["qubits"] is not None else 0

    # Nombre del archivo CSV
    csv_filename = f"{fecha}_{hora}_{framework_name}_{circuito_base}_{qubits_val}_{NUM_ITERATIONS}iter.csv"
    csv_path = os.path.join(csv_dir, csv_filename)

    # Definir nombre de columna dinámica
    if framework_name.lower() in ["qiskit", "myqlm", "tket"]:
        transpile_col_name = "TRANSPILE+EXECUTION-TIME(s)"
    else:
        transpile_col_name = "EXECUTION-TIME(s)"

    with open(csv_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)

        # Escribir Encabezado UNA SOLA VEZ
        writer.writerow([
            "FRAMEWORK", "DATE(Y-M-D)", "HOUR", "CIRCUIT", "ITERATION", "QUBITS",
            "1-GATE", "2-GATES", "3-GATES", "TOTAL-GATES",
            "RAM(MB)", "CPU(%)",
            "BUILD-TIME(s)", transpile_col_name, "TOTAL-TIME(s)"
        ])

        # Escribir todas las filas (una por iteración)
        for idx, metrics in enumerate(lista_metricas):
            # Recalcular hora para cada fila si quieres precisión de milisegundos, 
            # o usar la misma del archivo. Aquí uso la actual de escritura.
            current_time = datetime.now().strftime("%H:%M:%S")
            
            writer.writerow([
                framework_name, 
                fecha, 
                current_time, 
                circuito_base, 
                idx + 1,  # Número de iteración
                metrics["qubits"],
                metrics["gate_1q"], 
                metrics["gate_2q"],
                metrics["gate_3q"],  
                metrics["total_gates"],
                metrics["ram_usage_mb"],
                metrics["cpu_usage"],
                metrics["build_time"], 
                metrics["transpile_execution_time"], 
                metrics["total_time"]
            ])

    print(f"--> CSV guardado con {len(lista_metricas)} iteraciones en: {csv_filename}")

def main():
    print("=== BENCHMARK DE FRAMEWORKS CUÁNTICOS (MULTI-ITERACIÓN) ===")
    ensure_results_dir()
    
    # Obtener nombre del framework basado en la carpeta actual
    framework_name = os.path.basename(os.getcwd())

    circuitos = ["adder_n4.py","toffoli_n3.py","qft_n4.py", "bell_n4.py"] # Circuitos pequeños
    #circuitos = ["seca_n11.py", "bigadder_n18.py", "dnn_n16.py", "qec9xz_n17.py"] #Circuitos medianos
    #circuitos = ["vqe_uccsd_n28.py", "bigadder_n28.py"] # Circuitos grandes
    #circuitos = ["bigadder_n28.py"] # Descomentar para pruebas rápidas

    for circuito in circuitos:
        print(f"\nProcesando circuito: {circuito}")
        
        batch_metrics = [] # Lista para acumular las métricas de las iteraciones

        for i in range(NUM_ITERATIONS):
            # 1. Ejecutar y generar el txt temporal
            txt_path = run_framework(circuito, i)
            
            if txt_path:
                # 2. Leer las métricas de ese txt inmediatamente
                metrics = extract_metrics_from_txt(txt_path)
                
                # Si falló la lectura de métricas (diccionario con Nones), advertir
                if metrics["total_time"] is None:
                    print(f"   [!] Advertencia: No se extrajeron métricas en iteración {i+1}")
                
                batch_metrics.append(metrics)
            else:
                print(f"   [!] Error en la ejecución de la iteración {i+1}")

        # 3. Al terminar las iteraciones, guardar todo en un único CSV
        if batch_metrics:
            save_batch_to_csv(batch_metrics, framework_name, circuito)

    print(f"\nTodos los resultados guardados en: {os.path.abspath(RESULTS_DIR)}")

if __name__ == "__main__":
    main()