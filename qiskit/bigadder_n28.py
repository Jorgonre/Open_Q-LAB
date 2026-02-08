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

qreg_q = QuantumRegister(28, 'q')
creg_c = ClassicalRegister(28, 'c')
creg_meas = ClassicalRegister(28, 'meas')
circuit = QuantumCircuit(qreg_q, creg_c, creg_meas)

circuit.x(qreg_q[1])
circuit.x(qreg_q[2])
circuit.x(qreg_q[3])
circuit.x(qreg_q[4])
circuit.x(qreg_q[5])
circuit.x(qreg_q[6])
circuit.x(qreg_q[7])
circuit.x(qreg_q[8])
circuit.x(qreg_q[9])
circuit.x(qreg_q[10])
circuit.x(qreg_q[11])
circuit.x(qreg_q[12])
circuit.x(qreg_q[24])
circuit.cx(qreg_q[0], qreg_q[12])
circuit.cx(qreg_q[0], qreg_q[24])
circuit.ccx(qreg_q[24], qreg_q[12], qreg_q[0])
circuit.cx(qreg_q[1], qreg_q[13])
circuit.cx(qreg_q[1], qreg_q[0])
circuit.ccx(qreg_q[0], qreg_q[13], qreg_q[1])
circuit.cx(qreg_q[2], qreg_q[14])
circuit.cx(qreg_q[2], qreg_q[1])
circuit.ccx(qreg_q[1], qreg_q[14], qreg_q[2])
circuit.cx(qreg_q[3], qreg_q[15])
circuit.cx(qreg_q[3], qreg_q[2])
circuit.ccx(qreg_q[2], qreg_q[15], qreg_q[3])
circuit.cx(qreg_q[3], qreg_q[25])
circuit.ccx(qreg_q[2], qreg_q[15], qreg_q[3])
circuit.cx(qreg_q[3], qreg_q[2])
circuit.cx(qreg_q[2], qreg_q[15])
circuit.ccx(qreg_q[1], qreg_q[14], qreg_q[2])
circuit.cx(qreg_q[2], qreg_q[1])
circuit.cx(qreg_q[1], qreg_q[14])
circuit.ccx(qreg_q[0], qreg_q[13], qreg_q[1])
circuit.cx(qreg_q[1], qreg_q[0])
circuit.cx(qreg_q[0], qreg_q[13])
circuit.ccx(qreg_q[24], qreg_q[12], qreg_q[0])
circuit.cx(qreg_q[0], qreg_q[24])
circuit.cx(qreg_q[24], qreg_q[12])
circuit.cx(qreg_q[4], qreg_q[16])
circuit.cx(qreg_q[4], qreg_q[25])
circuit.ccx(qreg_q[25], qreg_q[16], qreg_q[4])
circuit.cx(qreg_q[5], qreg_q[17])
circuit.cx(qreg_q[5], qreg_q[4])
circuit.ccx(qreg_q[4], qreg_q[17], qreg_q[5])
circuit.cx(qreg_q[6], qreg_q[18])
circuit.cx(qreg_q[6], qreg_q[5])
circuit.ccx(qreg_q[5], qreg_q[18], qreg_q[6])
circuit.cx(qreg_q[7], qreg_q[19])
circuit.cx(qreg_q[7], qreg_q[6])
circuit.ccx(qreg_q[6], qreg_q[19], qreg_q[7])
circuit.cx(qreg_q[7], qreg_q[26])
circuit.ccx(qreg_q[6], qreg_q[19], qreg_q[7])
circuit.cx(qreg_q[7], qreg_q[6])
circuit.cx(qreg_q[6], qreg_q[19])
circuit.ccx(qreg_q[5], qreg_q[18], qreg_q[6])
circuit.cx(qreg_q[6], qreg_q[5])
circuit.cx(qreg_q[5], qreg_q[18])
circuit.ccx(qreg_q[4], qreg_q[17], qreg_q[5])
circuit.cx(qreg_q[5], qreg_q[4])
circuit.cx(qreg_q[4], qreg_q[17])
circuit.ccx(qreg_q[25], qreg_q[16], qreg_q[4])
circuit.cx(qreg_q[4], qreg_q[25])
circuit.cx(qreg_q[25], qreg_q[16])
circuit.cx(qreg_q[8], qreg_q[20])
circuit.cx(qreg_q[8], qreg_q[26])
circuit.ccx(qreg_q[26], qreg_q[20], qreg_q[8])
circuit.cx(qreg_q[9], qreg_q[21])
circuit.cx(qreg_q[9], qreg_q[8])
circuit.ccx(qreg_q[8], qreg_q[21], qreg_q[9])
circuit.cx(qreg_q[10], qreg_q[22])
circuit.cx(qreg_q[10], qreg_q[9])
circuit.ccx(qreg_q[9], qreg_q[22], qreg_q[10])
circuit.cx(qreg_q[11], qreg_q[23])
circuit.cx(qreg_q[11], qreg_q[10])
circuit.ccx(qreg_q[10], qreg_q[23], qreg_q[11])
circuit.cx(qreg_q[11], qreg_q[27])
circuit.ccx(qreg_q[10], qreg_q[23], qreg_q[11])
circuit.cx(qreg_q[11], qreg_q[10])
circuit.cx(qreg_q[10], qreg_q[23])
circuit.ccx(qreg_q[9], qreg_q[22], qreg_q[10])
circuit.cx(qreg_q[10], qreg_q[9])
circuit.cx(qreg_q[9], qreg_q[22])
circuit.ccx(qreg_q[8], qreg_q[21], qreg_q[9])
circuit.cx(qreg_q[9], qreg_q[8])
circuit.cx(qreg_q[8], qreg_q[21])
circuit.ccx(qreg_q[26], qreg_q[20], qreg_q[8])
circuit.cx(qreg_q[8], qreg_q[26])
circuit.cx(qreg_q[26], qreg_q[20])
circuit.barrier(qreg_q[0], qreg_q[1], qreg_q[2], qreg_q[3], qreg_q[4], qreg_q[5], qreg_q[6], qreg_q[7], qreg_q[8], qreg_q[9], qreg_q[10], qreg_q[11], qreg_q[12], qreg_q[13], qreg_q[14], qreg_q[15], qreg_q[16], qreg_q[17], qreg_q[18], qreg_q[19], qreg_q[20], qreg_q[21], qreg_q[22], qreg_q[23], qreg_q[24], qreg_q[25], qreg_q[26], qreg_q[27])
circuit.measure(qreg_q[0], creg_meas[0])
circuit.measure(qreg_q[1], creg_meas[1])
circuit.measure(qreg_q[2], creg_meas[2])
circuit.measure(qreg_q[3], creg_meas[3])
circuit.measure(qreg_q[4], creg_meas[4])
circuit.measure(qreg_q[5], creg_meas[5])
circuit.measure(qreg_q[6], creg_meas[6])
circuit.measure(qreg_q[7], creg_meas[7])
circuit.measure(qreg_q[8], creg_meas[8])
circuit.measure(qreg_q[9], creg_meas[9])
circuit.measure(qreg_q[10], creg_meas[10])
circuit.measure(qreg_q[11], creg_meas[11])
circuit.measure(qreg_q[12], creg_meas[12])
circuit.measure(qreg_q[13], creg_meas[13])
circuit.measure(qreg_q[14], creg_meas[14])
circuit.measure(qreg_q[15], creg_meas[15])
circuit.measure(qreg_q[16], creg_meas[16])
circuit.measure(qreg_q[17], creg_meas[17])
circuit.measure(qreg_q[18], creg_meas[18])
circuit.measure(qreg_q[19], creg_meas[19])
circuit.measure(qreg_q[20], creg_meas[20])
circuit.measure(qreg_q[21], creg_meas[21])
circuit.measure(qreg_q[22], creg_meas[22])
circuit.measure(qreg_q[23], creg_meas[23])
circuit.measure(qreg_q[24], creg_meas[24])
circuit.measure(qreg_q[25], creg_meas[25])
circuit.measure(qreg_q[26], creg_meas[26])
circuit.measure(qreg_q[27], creg_meas[27])

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

# --- INICIO DEL BLOQUE DE CONTEO ---

# Inicializamos contadores
num_1q = 0
num_2q = 0
num_3q = 0

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
    elif operation.num_qubits == 3:
        num_3q += 1

total_gates = num_1q + num_2q + num_3q
num_qubits = circuit.num_qubits # Qubits lógicos originales
depth = circuit.depth()      # Profundidad del circuito físico


print("# --- METRICS ---")
print(f"Qubits:{num_qubits}")
print(f"Depth:{depth}")
print(f"Gate_1q:{num_1q}")
print(f"Gate_2q:{num_2q}")
print(f"Gate_3q:{num_3q}")
print(f"Total_gates:{total_gates}")
print(f"Build_time:{build_time:.4f}")
print(f"Transpile_execution_time:{transpile_time:.4f}")
print(f"Total_time:{total_time:.4f}")
print(f"CPU_usage:{cpu_usage:.2f}")
print(f"RAM_usage_MB:{ram_usage_mb:.2f}")
print("# --- END_METRICS ---")