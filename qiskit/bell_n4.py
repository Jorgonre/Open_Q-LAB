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

qreg_q = QuantumRegister(4, 'q')
creg_m_b = ClassicalRegister(1, 'm_b')
creg_m_y = ClassicalRegister(1, 'm_y')
creg_m_a = ClassicalRegister(1, 'm_a')
creg_m_x = ClassicalRegister(1, 'm_x')
circuit = QuantumCircuit(qreg_q, creg_m_b, creg_m_y, creg_m_a, creg_m_x)

# Generated from Cirq v0.8.0
# Qubits: [(0, 0), (0, 1), (1, 0), (1, 1)]
circuit.h(qreg_q[0])
circuit.h(qreg_q[1])
circuit.h(qreg_q[3])
circuit.cx(qreg_q[0], qreg_q[2])
circuit.rx(pi * -0.25, qreg_q[0])
# Gate: CNOT**0.5
circuit.ry(pi * -0.5, qreg_q[2])
circuit.u(pi * 0.5, 0, pi * 0.75, qreg_q[3])
circuit.u(pi * 0.5, 0, pi * 0.25, qreg_q[2])
circuit.rx(pi * 0.5, qreg_q[3])
circuit.cx(qreg_q[3], qreg_q[2])
circuit.rx(pi * 0.25, qreg_q[3])
circuit.ry(pi * 0.5, qreg_q[2])
circuit.cx(qreg_q[2], qreg_q[3])
circuit.rx(pi * -0.5, qreg_q[2])
circuit.rz(pi * 0.5, qreg_q[2])
circuit.cx(qreg_q[3], qreg_q[2])
circuit.u(pi * 0.5, pi * 0.5, pi * 1.0, qreg_q[3])
circuit.u(pi * 0.5, pi * 1.0, pi * 1.0, qreg_q[2])
circuit.ry(pi * 0.5, qreg_q[2])
# Gate: CNOT**0.5
circuit.ry(pi * -0.5, qreg_q[0])
circuit.u(pi * 0.5, 0, pi * 0.75, qreg_q[1])
circuit.u(pi * 0.5, 0, pi * 0.25, qreg_q[0])
circuit.rx(pi * 0.5, qreg_q[1])
circuit.cx(qreg_q[1], qreg_q[0])
circuit.rx(pi * 0.25, qreg_q[1])
circuit.ry(pi * 0.5, qreg_q[0])
circuit.cx(qreg_q[0], qreg_q[1])
circuit.rx(pi * -0.5, qreg_q[0])
circuit.rz(pi * 0.5, qreg_q[0])
circuit.cx(qreg_q[1], qreg_q[0])
circuit.u(pi * 0.5, pi * 0.5, pi * 1.0, qreg_q[1])
circuit.u(pi * 0.5, pi * 1.0, pi * 1.0, qreg_q[0])
circuit.ry(pi * 0.5, qreg_q[0])
circuit.measure(qreg_q[2], creg_m_b[0])
circuit.measure(qreg_q[3], creg_m_y[0])
circuit.measure(qreg_q[0], creg_m_a[0])
circuit.measure(qreg_q[1], creg_m_x[0])

build_time = time.time() - start_build

start_transpile = time.time()

sim = AerSimulator()
transpiled = transpile(circuit, backend=sim)

job = sim.run(transpiled, shots=1024)  
result = job.result()

transpile_time = time.time() - start_transpile

# Medir uso de recursos
cpu_usage = process.cpu_percent(None)
ram_usage_mb = process.memory_info().rss / (1024 * 1024)

counts = result.get_counts()

total_time = time.time() - start_time

print(counts)
 
plot_histogram(counts)

# Contar operaciones
ops = circuit.count_ops()

# Clasificar puertas
one_qubit_gates = ['x', 'h', 't', 'tdg', 's','rx','ry','u','rz']
two_qubit_gates = ['cx']

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