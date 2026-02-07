import pennylane as qml
from jax import numpy as np
import jax
from collections import Counter
import time
import psutil
import os

process = psutil.Process(os.getpid())

process.cpu_percent(interval=None)  # Establece línea base

start_time = time.time()
# Medir tiempo de construcción
start_build = time.time()

wires_q0 = list(range(0, 9))
wires_q1 = list(range(9, 17))
all_wires = wires_q0 + wires_q1

dev = qml.device("default.qubit", wires = all_wires, shots=1024)

@qml.qnode(dev)
def circuit():

    qml.Hadamard(wires = 0)
    qml.CNOT(wires = [0, 3])
    qml.CNOT(wires = [0, 6])
    qml.Hadamard(wires = 0)
    qml.Hadamard(wires = 3)
    qml.Hadamard(wires = 6)
    qml.CNOT(wires = [0, 1])
    qml.CNOT(wires = [0, 2])
    qml.CNOT(wires = [3, 4])
    qml.CNOT(wires = [3, 5])
    qml.CNOT(wires = [6, 7])
    qml.CNOT(wires = [6, 8])
    qml.CNOT(wires = [0, 9])
    qml.CNOT(wires = [1, 9])
    qml.CNOT(wires = [1, 10])
    qml.CNOT(wires = [2, 10])
    qml.CNOT(wires = [3, 11])
    qml.CNOT(wires = [4, 11])
    qml.CNOT(wires = [4, 12])
    qml.CNOT(wires = [5, 12])
    qml.CNOT(wires = [6, 13])
    qml.CNOT(wires = [7, 13])
    qml.CNOT(wires = [7, 14])
    qml.CNOT(wires = [8, 14])
    qml.Hadamard(wires = 0)
    qml.Hadamard(wires = 1)
    qml.Hadamard(wires = 2)
    qml.Hadamard(wires = 3)
    qml.Hadamard(wires = 4)
    qml.Hadamard(wires = 5)
    qml.Hadamard(wires = 6)
    qml.Hadamard(wires = 7)
    qml.Hadamard(wires = 8)
    qml.CNOT(wires = [0, 15])
    qml.CNOT(wires = [3, 16])
    qml.CNOT(wires = [1, 15])
    qml.CNOT(wires = [4, 16])
    qml.CNOT(wires = [2, 15])
    qml.CNOT(wires = [5, 16])
    qml.CNOT(wires = [3, 15])
    qml.CNOT(wires = [6, 16])
    qml.CNOT(wires = [4, 15])
    qml.CNOT(wires = [7, 16])
    qml.CNOT(wires = [5, 15])
    qml.CNOT(wires = [8, 16])
    qml.Hadamard(wires = 0)
    qml.Hadamard(wires = 1)
    qml.Hadamard(wires = 2)
    qml.Hadamard(wires = 3)
    qml.Hadamard(wires = 4)
    qml.Hadamard(wires = 5)
    qml.Hadamard(wires = 6)
    qml.Hadamard(wires = 7)


    wires_to_measure = wires_q1
    
    return qml.sample(wires=wires_to_measure)

samples = circuit()

build_time = time.time() - start_build

start_transpile = time.time()

samples = np.array(samples)
if samples.ndim == 1 and num_wires > 1:
    samples = samples.reshape((1024, 17))

transpile_time = time.time() - start_transpile

total_time = time.time() - start_time

bitstrings = []
for row in samples:
    # Convertimos a string y unimos: [1, 0] -> "10"
    bitstring = "".join(str(int(bit)) for bit in row)
    bitstrings.append(bitstring)

# 2. Contamos las repeticiones (Histograma)
counts = Counter(bitstrings)
total_shots = len(samples) # Debería ser 1024

for state, count in counts.items():
    prob = count / total_shots
    print(f"|{state}> {prob}")

# Medir uso de recursos
cpu_usage = process.cpu_percent(None)
ram_usage_mb = process.memory_info().rss / (1024 * 1024)

for wire in range(17):
    col = samples[:, wire]
    counts = Counter(col.tolist())
    total = sum(counts.values())
    p0 = counts.get(0, 0) / total
    p1 = counts.get(1, 0) / total
    print(f"q{wire}: {p0:.3f} |0>  +  {p1:.3f} |1>")

# Obtener especificaciones del circuito
specs = qml.specs(circuit)()

# Número de qubits
num_qubits = specs["num_tape_wires"]

# Profundidad
depth = specs["resources"].depth

# Conteo de operaciones por tipo
ops = specs["resources"].gate_types

# Clasificar puertas
one_qubit_gates = ["PauliX", "Hadamard", "T", "S", "RX", "RY", "RZ", "U3", "PauliZ"]
two_qubit_gates = ["CNOT", "CZ"]
three_qubit_gates = ["Toffoli"]

num_1q = sum(ops.get(g, 0) for g in one_qubit_gates)
num_2q = sum(ops.get(g, 0) for g in two_qubit_gates)
total_gates = num_1q + num_2q

print("\nCircuito (texto):")
drawer = qml.draw(circuit)
print(drawer())

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