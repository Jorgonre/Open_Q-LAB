from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
from numpy import pi
import time
from qiskit import transpile
import psutil
import os

process = psutil.Process(os.getpid())

process.cpu_percent(interval=None)  # Establece línea base

start_time = time.time()
# Medir tiempo de construcción
start_build = time.time()

qreg_q0 = QuantumRegister(9, 'q0')
qreg_q1 = QuantumRegister(8, 'q1')
creg_c0 = ClassicalRegister(8, 'c0')
circuit = QuantumCircuit(qreg_q0, qreg_q1, creg_c0)

circuit.h(qreg_q0[0])
circuit.cx(qreg_q0[0], qreg_q0[3])
circuit.cx(qreg_q0[0], qreg_q0[6])
circuit.h(qreg_q0[0])
circuit.h(qreg_q0[3])
circuit.h(qreg_q0[6])
circuit.cx(qreg_q0[0], qreg_q0[1])
circuit.cx(qreg_q0[0], qreg_q0[2])
circuit.cx(qreg_q0[3], qreg_q0[4])
circuit.cx(qreg_q0[3], qreg_q0[5])
circuit.cx(qreg_q0[6], qreg_q0[7])
circuit.cx(qreg_q0[6], qreg_q0[8])
circuit.cx(qreg_q0[0], qreg_q1[0])
circuit.cx(qreg_q0[1], qreg_q1[0])
circuit.cx(qreg_q0[1], qreg_q1[1])
circuit.cx(qreg_q0[2], qreg_q1[1])
circuit.cx(qreg_q0[3], qreg_q1[2])
circuit.cx(qreg_q0[4], qreg_q1[2])
circuit.cx(qreg_q0[4], qreg_q1[3])
circuit.cx(qreg_q0[5], qreg_q1[3])
circuit.cx(qreg_q0[6], qreg_q1[4])
circuit.cx(qreg_q0[7], qreg_q1[4])
circuit.cx(qreg_q0[7], qreg_q1[5])
circuit.cx(qreg_q0[8], qreg_q1[5])
circuit.measure(qreg_q1[0], creg_c0[0])
circuit.measure(qreg_q1[1], creg_c0[1])
circuit.measure(qreg_q1[2], creg_c0[2])
circuit.measure(qreg_q1[3], creg_c0[3])
circuit.measure(qreg_q1[4], creg_c0[4])
circuit.measure(qreg_q1[5], creg_c0[5])
circuit.h(qreg_q0[0])
circuit.h(qreg_q0[1])
circuit.h(qreg_q0[2])
circuit.h(qreg_q0[3])
circuit.h(qreg_q0[4])
circuit.h(qreg_q0[5])
circuit.h(qreg_q0[6])
circuit.h(qreg_q0[7])
circuit.h(qreg_q0[8])
circuit.cx(qreg_q0[0], qreg_q1[6])
circuit.cx(qreg_q0[3], qreg_q1[7])
circuit.cx(qreg_q0[1], qreg_q1[6])
circuit.cx(qreg_q0[4], qreg_q1[7])
circuit.cx(qreg_q0[2], qreg_q1[6])
circuit.cx(qreg_q0[5], qreg_q1[7])
circuit.cx(qreg_q0[3], qreg_q1[6])
circuit.cx(qreg_q0[6], qreg_q1[7])
circuit.cx(qreg_q0[4], qreg_q1[6])
circuit.cx(qreg_q0[7], qreg_q1[7])
circuit.cx(qreg_q0[5], qreg_q1[6])
circuit.cx(qreg_q0[8], qreg_q1[7])
circuit.measure(qreg_q1[6], creg_c0[6])
circuit.measure(qreg_q1[7], creg_c0[7])
circuit.h(qreg_q0[0])
circuit.h(qreg_q0[1])
circuit.h(qreg_q0[2])
circuit.h(qreg_q0[3])
circuit.h(qreg_q0[4])
circuit.h(qreg_q0[5])
circuit.h(qreg_q0[6])
circuit.h(qreg_q0[7])

build_time = time.time() - start_build

start_transpile = time.time()

sim = AerSimulator()
#transpiled = transpile(circuit, backend=sim)
transpiled = transpile(circuit, backend=sim, optimization_level = 0)

job = sim.run(transpiled, shots=1024)  
result = job.result()

transpile_time = time.time() - start_transpile
total_time = time.time() - start_time

# Medir uso de recursos
cpu_usage = process.cpu_percent(None)
ram_usage_mb = process.memory_info().rss / (1024 * 1024)

counts = result.get_counts()

print(len(counts))

print(counts)
 
plot_histogram(counts)

# --- INICIO DEL NUEVO BLOQUE DE CONTEO ---

# Inicializamos contadores
num_1q = 0
num_2q = 0
num_multi_q = 0

# Iteramos sobre cada instrucción del circuito 
for instruction in circuit.data:
    operation = instruction.operation
    
    # Ignoramos lo que no sea puerta lógica
    if operation.name in ['measure']:
        continue
    
    # Clasificamos según el número de qubits que toca la puerta
    if operation.num_qubits == 1:
        num_1q += 1
    elif operation.num_qubits == 2:
        num_2q += 1
    else:
        num_multi_q += 1

total_gates = num_1q + num_2q + num_multi_q
num_qubits = circuit.num_qubits # Qubits lógicos originales
depth = circuit.depth()      # Profundidad del circuito físico


print("# --- METRICS ---")
print(f"Qubits:{num_qubits}")
print(f"Depth:{depth}")
print(f"Gate_1q:{num_1q}")
print(f"Gate_2q:{num_2q}")
print(f"Total_gates:{total_gates}")
print(f"Build_time:{build_time:.4f}")
print(f"Transpile_execution_time:{transpile_time:.4f}")
print(f"Total_time:{total_time:.4f}")
print(f"CPU_usage:{cpu_usage:.2f}")
print(f"RAM_usage_MB:{ram_usage_mb:.2f}")
print("# --- END_METRICS ---")