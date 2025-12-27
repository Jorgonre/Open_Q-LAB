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

qreg_q = QuantumRegister(4, 'q')
creg_c = ClassicalRegister(4, 'c')
circuit = QuantumCircuit(qreg_q, creg_c)

# quantum Fourier transform
circuit.x(qreg_q[0])
circuit.x(qreg_q[2])

circuit.barrier(qreg_q)

circuit.h(qreg_q[0])

circuit.cp(pi / 2, qreg_q[1], qreg_q[0])

circuit.h(qreg_q[1])

circuit.cp(pi / 4, qreg_q[2], qreg_q[0])

circuit.cp(pi / 2, qreg_q[2], qreg_q[1])

circuit.h(qreg_q[2])

circuit.cp(pi / 8, qreg_q[3], qreg_q[0])

circuit.cp(pi / 4, qreg_q[3], qreg_q[1])

circuit.cp(pi / 2, qreg_q[3], qreg_q[2])

circuit.h(qreg_q[3])

circuit.measure(qreg_q, creg_c)

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

# Contar operaciones
ops = circuit.count_ops()

# Clasificar puertas
one_qubit_gates = ['x', 'h', 't', 'tdg', 's']
two_qubit_gates = ['cx','cp']

num_1q = sum(ops.get(gate, 0) for gate in one_qubit_gates)
num_2q = sum(ops.get(gate, 0) for gate in two_qubit_gates)
total_gates = num_1q + num_2q
num_qubits = circuit.num_qubits
depth = circuit.depth()


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