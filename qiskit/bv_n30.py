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

from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from numpy import pi

qreg_q0 = QuantumRegister(30, 'q0')
creg_c0 = ClassicalRegister(30, 'c0')
circuit = QuantumCircuit(qreg_q0, creg_c0)

circuit.h(qreg_q0[0])
circuit.h(qreg_q0[1])
circuit.h(qreg_q0[2])
circuit.h(qreg_q0[3])
circuit.h(qreg_q0[4])
circuit.h(qreg_q0[5])
circuit.h(qreg_q0[6])
circuit.h(qreg_q0[7])
circuit.h(qreg_q0[8])
circuit.h(qreg_q0[9])
circuit.h(qreg_q0[10])
circuit.h(qreg_q0[11])
circuit.h(qreg_q0[12])
circuit.h(qreg_q0[13])
circuit.h(qreg_q0[14])
circuit.h(qreg_q0[15])
circuit.h(qreg_q0[16])
circuit.h(qreg_q0[17])
circuit.h(qreg_q0[18])
circuit.h(qreg_q0[19])
circuit.h(qreg_q0[20])
circuit.h(qreg_q0[21])
circuit.h(qreg_q0[22])
circuit.h(qreg_q0[23])
circuit.h(qreg_q0[24])
circuit.h(qreg_q0[25])
circuit.h(qreg_q0[26])
circuit.h(qreg_q0[27])
circuit.h(qreg_q0[28])
circuit.x(qreg_q0[29])
circuit.h(qreg_q0[29])
circuit.barrier(qreg_q0[0], qreg_q0[1], qreg_q0[2], qreg_q0[3], qreg_q0[4], qreg_q0[5], qreg_q0[6], qreg_q0[7], qreg_q0[8], qreg_q0[9], qreg_q0[10], qreg_q0[11], qreg_q0[12], qreg_q0[13], qreg_q0[14], qreg_q0[15], qreg_q0[16], qreg_q0[17], qreg_q0[18], qreg_q0[19], qreg_q0[20], qreg_q0[21], qreg_q0[22], qreg_q0[23], qreg_q0[24], qreg_q0[25], qreg_q0[26], qreg_q0[27], qreg_q0[28], qreg_q0[29])
circuit.cx(qreg_q0[0], qreg_q0[29])
circuit.cx(qreg_q0[4], qreg_q0[29])
circuit.cx(qreg_q0[5], qreg_q0[29])
circuit.cx(qreg_q0[7], qreg_q0[29])
circuit.cx(qreg_q0[8], qreg_q0[29])
circuit.cx(qreg_q0[10], qreg_q0[29])
circuit.cx(qreg_q0[11], qreg_q0[29])
circuit.cx(qreg_q0[13], qreg_q0[29])
circuit.cx(qreg_q0[15], qreg_q0[29])
circuit.cx(qreg_q0[17], qreg_q0[29])
circuit.cx(qreg_q0[21], qreg_q0[29])
circuit.cx(qreg_q0[22], qreg_q0[29])
circuit.cx(qreg_q0[23], qreg_q0[29])
circuit.cx(qreg_q0[24], qreg_q0[29])
circuit.cx(qreg_q0[25], qreg_q0[29])
circuit.cx(qreg_q0[26], qreg_q0[29])
circuit.cx(qreg_q0[27], qreg_q0[29])
circuit.cx(qreg_q0[28], qreg_q0[29])
circuit.barrier(qreg_q0[0], qreg_q0[1], qreg_q0[2], qreg_q0[3], qreg_q0[4], qreg_q0[5], qreg_q0[6], qreg_q0[7], qreg_q0[8], qreg_q0[9], qreg_q0[10], qreg_q0[11], qreg_q0[12], qreg_q0[13], qreg_q0[14], qreg_q0[15], qreg_q0[16], qreg_q0[17], qreg_q0[18], qreg_q0[19], qreg_q0[20], qreg_q0[21], qreg_q0[22], qreg_q0[23], qreg_q0[24], qreg_q0[25], qreg_q0[26], qreg_q0[27], qreg_q0[28], qreg_q0[29])
circuit.h(qreg_q0[0])
circuit.h(qreg_q0[1])
circuit.h(qreg_q0[2])
circuit.h(qreg_q0[3])
circuit.h(qreg_q0[4])
circuit.h(qreg_q0[5])
circuit.h(qreg_q0[6])
circuit.h(qreg_q0[7])
circuit.h(qreg_q0[8])
circuit.h(qreg_q0[9])
circuit.h(qreg_q0[10])
circuit.h(qreg_q0[11])
circuit.h(qreg_q0[12])
circuit.h(qreg_q0[13])
circuit.h(qreg_q0[14])
circuit.h(qreg_q0[15])
circuit.h(qreg_q0[16])
circuit.h(qreg_q0[17])
circuit.h(qreg_q0[18])
circuit.h(qreg_q0[19])
circuit.h(qreg_q0[20])
circuit.h(qreg_q0[21])
circuit.h(qreg_q0[22])
circuit.h(qreg_q0[23])
circuit.h(qreg_q0[24])
circuit.h(qreg_q0[25])
circuit.h(qreg_q0[26])
circuit.h(qreg_q0[27])
circuit.h(qreg_q0[28])
circuit.measure(qreg_q0[0], creg_c0[0])
circuit.measure(qreg_q0[1], creg_c0[1])
circuit.measure(qreg_q0[2], creg_c0[2])
circuit.measure(qreg_q0[3], creg_c0[3])
circuit.measure(qreg_q0[4], creg_c0[4])
circuit.measure(qreg_q0[5], creg_c0[5])
circuit.measure(qreg_q0[6], creg_c0[6])
circuit.measure(qreg_q0[7], creg_c0[7])
circuit.measure(qreg_q0[8], creg_c0[8])
circuit.measure(qreg_q0[9], creg_c0[9])
circuit.measure(qreg_q0[10], creg_c0[10])
circuit.measure(qreg_q0[11], creg_c0[11])
circuit.measure(qreg_q0[12], creg_c0[12])
circuit.measure(qreg_q0[13], creg_c0[13])
circuit.measure(qreg_q0[14], creg_c0[14])
circuit.measure(qreg_q0[15], creg_c0[15])
circuit.measure(qreg_q0[16], creg_c0[16])
circuit.measure(qreg_q0[17], creg_c0[17])
circuit.measure(qreg_q0[18], creg_c0[18])
circuit.measure(qreg_q0[19], creg_c0[19])
circuit.measure(qreg_q0[20], creg_c0[20])
circuit.measure(qreg_q0[21], creg_c0[21])
circuit.measure(qreg_q0[22], creg_c0[22])
circuit.measure(qreg_q0[23], creg_c0[23])
circuit.measure(qreg_q0[24], creg_c0[24])
circuit.measure(qreg_q0[25], creg_c0[25])
circuit.measure(qreg_q0[26], creg_c0[26])
circuit.measure(qreg_q0[27], creg_c0[27])
circuit.measure(qreg_q0[28], creg_c0[28])

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

# Inicializamos contadores
num_1q = 0
num_2q = 0

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

total_gates = num_1q + num_2q
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