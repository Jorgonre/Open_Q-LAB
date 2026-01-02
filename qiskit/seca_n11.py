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

qreg_q = QuantumRegister(11, 'q')
creg_c = ClassicalRegister(11, 'c')
circuit = QuantumCircuit(qreg_q, creg_c)

circuit.z(qreg_q[0])
circuit.h(qreg_q[0])
# secret unitary: hz
circuit.barrier(qreg_q)
# Shor's error correction algorithm
circuit.cx(qreg_q[0], qreg_q[3])
circuit.cx(qreg_q[0], qreg_q[6])
circuit.cz(qreg_q[0], qreg_q[3])
circuit.cz(qreg_q[0], qreg_q[6])
circuit.h(qreg_q[0])
circuit.h(qreg_q[3])
circuit.h(qreg_q[6])
circuit.z(qreg_q[0])
circuit.z(qreg_q[3])
circuit.z(qreg_q[6])
circuit.cx(qreg_q[0], qreg_q[1])
circuit.cx(qreg_q[0], qreg_q[2])
circuit.cx(qreg_q[3], qreg_q[4])
circuit.cx(qreg_q[3], qreg_q[5])
circuit.cx(qreg_q[6], qreg_q[7])
circuit.cx(qreg_q[6], qreg_q[8])
circuit.cz(qreg_q[0], qreg_q[1])
circuit.cz(qreg_q[0], qreg_q[2])
circuit.cz(qreg_q[3], qreg_q[4])
circuit.cz(qreg_q[3], qreg_q[5])
circuit.cz(qreg_q[6], qreg_q[7])
circuit.cz(qreg_q[6], qreg_q[8])
# Alice starts with qubit 9.
# Bob starts with qubit 10.
# Alice is given qubit 0.
# Bob is given error-correcting qubits 1-8.
# Alice and Bob do not know what has been done to qubit 0.
circuit.barrier(qreg_q)
# Alice and Bob entangle their starting qubits.
circuit.h(qreg_q[9])
circuit.cx(qreg_q[9], qreg_q[10])
# Alice keeps qubits 0 and 9.
# Bob leaves with qubits 1-8 and 10.
circuit.barrier(qreg_q)
# Alice teleports the quantum state of qubit 0 to Bob's qubit.
circuit.cx(qreg_q[0], qreg_q[9])
circuit.measure(qreg_q[9], creg_c[9])
circuit.h(qreg_q[0])
circuit.cx(qreg_q[9], qreg_q[10])
circuit.measure(qreg_q[0], creg_c[0])
circuit.cz(qreg_q[0], qreg_q[10])
circuit.barrier(qreg_q)
# Bob corrects for bit flips and sign flips
circuit.cx(qreg_q[10], qreg_q[1])
circuit.cx(qreg_q[10], qreg_q[2])
circuit.cx(qreg_q[3], qreg_q[4])
circuit.cx(qreg_q[3], qreg_q[5])
circuit.cx(qreg_q[6], qreg_q[7])
circuit.cx(qreg_q[6], qreg_q[8])
circuit.cz(qreg_q[10], qreg_q[1])
circuit.cz(qreg_q[10], qreg_q[2])
circuit.cz(qreg_q[3], qreg_q[4])
circuit.cz(qreg_q[3], qreg_q[5])
circuit.cz(qreg_q[6], qreg_q[7])
circuit.cz(qreg_q[6], qreg_q[8])
circuit.ccx(qreg_q[1], qreg_q[2], qreg_q[10])
circuit.ccx(qreg_q[5], qreg_q[4], qreg_q[3])
circuit.ccx(qreg_q[8], qreg_q[7], qreg_q[6])
circuit.barrier(qreg_q)
# start CCZ gates
circuit.h(qreg_q[10])
circuit.ccx(qreg_q[1], qreg_q[2], qreg_q[10])
circuit.h(qreg_q[10])
circuit.h(qreg_q[3])
circuit.ccx(qreg_q[5], qreg_q[4], qreg_q[3])
circuit.h(qreg_q[3])
circuit.h(qreg_q[6])
circuit.ccx(qreg_q[8], qreg_q[7], qreg_q[6])
circuit.h(qreg_q[6])
circuit.barrier(qreg_q)
# end CCZ gates
circuit.h(qreg_q[10])
circuit.h(qreg_q[3])
circuit.h(qreg_q[6])
circuit.z(qreg_q[10])
circuit.z(qreg_q[3])
circuit.z(qreg_q[6])
circuit.cx(qreg_q[10], qreg_q[3])
circuit.cx(qreg_q[10], qreg_q[6])
circuit.cz(qreg_q[10], qreg_q[3])
circuit.cz(qreg_q[10], qreg_q[6])
circuit.ccx(qreg_q[3], qreg_q[6], qreg_q[10])
circuit.h(qreg_q[10])
circuit.ccx(qreg_q[3], qreg_q[6], qreg_q[10])
circuit.h(qreg_q[10])
circuit.barrier(qreg_q)
# Based on Alice's measurements, Bob reverses the secret unitary.
# 00 do nothing
# 01 apply X
# 10 apply Z
# 11 apply ZX
circuit.h(qreg_q[10]) #COMENTAR SI QUIERO 8 RESULTADOS COMO EN EL BENCHMARK DE BASE
circuit.z(qreg_q[10])
circuit.measure(qreg_q[10], creg_c[10])

build_time = time.time() - start_build

start_transpile = time.time()

sim = AerSimulator()
transpiled = transpile(circuit, backend=sim)

job = sim.run(transpiled, shots=1024)  
result = job.result()

transpile_time = time.time() - start_transpile
total_time = time.time() - start_time

# Medir uso de recursos
cpu_usage = process.cpu_percent(None)
ram_usage_mb = process.memory_info().rss / (1024 * 1024)

counts = result.get_counts()

print(counts)
 
plot_histogram(counts)

# --- INICIO DEL NUEVO BLOQUE DE CONTEO ---

# Inicializamos contadores
num_1q = 0
num_2q = 0
num_multi_q = 0

# Iteramos sobre cada instrucción del circuito TRANSPILED (el físico real)
for instruction in transpiled.data:
    operation = instruction.operation
    
    # Ignoramos lo que no sea puerta lógica
    if operation.name in ['barrier', 'measure']:
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