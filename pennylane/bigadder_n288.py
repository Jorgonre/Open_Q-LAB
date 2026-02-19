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

# Configuración del dispositivo (Sin shots aquí)
dev = qml.device("default.qubit", wires=28)

# Definimos los shots en el decorador (CORRECCIÓN APLICADA)
@qml.qnode(dev, shots=1024)
def circuit():
    qml.PauliX(wires=1)
    qml.PauliX(wires=2)
    qml.PauliX(wires=3)
    qml.PauliX(wires=4)
    qml.PauliX(wires=5)
    qml.PauliX(wires=6)
    qml.PauliX(wires=7)
    qml.PauliX(wires=8)
    qml.PauliX(wires=9)
    qml.PauliX(wires=10)
    qml.PauliX(wires=11)
    qml.PauliX(wires=12)
    qml.PauliX(wires=24)
    qml.CNOT(wires=[0, 12])
    qml.CNOT(wires=[0, 24])
    qml.Toffoli(wires=[24, 12, 0])
    qml.CNOT(wires=[1, 13])
    qml.CNOT(wires=[1, 0])
    qml.Toffoli(wires=[0, 13, 1])
    qml.CNOT(wires=[2, 14])
    qml.CNOT(wires=[2, 1])
    qml.Toffoli(wires=[1, 14, 2])
    qml.CNOT(wires=[3, 15])
    qml.CNOT(wires=[3, 2])
    qml.Toffoli(wires=[2, 15, 3])
    qml.CNOT(wires=[3, 25])
    qml.Toffoli(wires=[2, 15, 3])
    qml.CNOT(wires=[3, 2])
    qml.CNOT(wires=[2, 15])
    qml.Toffoli(wires=[1, 14, 2])
    qml.CNOT(wires=[2, 1])
    qml.CNOT(wires=[1, 14])
    qml.Toffoli(wires=[0, 13, 1])
    qml.CNOT(wires=[1, 0])
    qml.CNOT(wires=[0, 13])
    qml.Toffoli(wires=[24, 12, 0])
    qml.CNOT(wires=[0, 24])
    qml.CNOT(wires=[24, 12])
    qml.CNOT(wires=[4, 16])
    qml.CNOT(wires=[4, 25])
    qml.Toffoli(wires=[25, 16, 4])
    qml.CNOT(wires=[5, 17])
    qml.CNOT(wires=[5, 4])
    qml.Toffoli(wires=[4, 17, 5])
    qml.CNOT(wires=[6, 18])
    qml.CNOT(wires=[6, 5])
    qml.Toffoli(wires=[5, 18, 6])
    qml.CNOT(wires=[7, 19])
    qml.CNOT(wires=[7, 6])
    qml.Toffoli(wires=[6, 19, 7])
    qml.CNOT(wires=[7, 26])
    qml.Toffoli(wires=[6, 19, 7])
    qml.CNOT(wires=[7, 6])
    qml.CNOT(wires=[6, 19])
    qml.Toffoli(wires=[5, 18, 6])
    qml.CNOT(wires=[6, 5])
    qml.CNOT(wires=[5, 18])
    qml.Toffoli(wires=[4, 17, 5])
    qml.CNOT(wires=[5, 4])
    qml.CNOT(wires=[4, 17])
    qml.Toffoli(wires=[25, 16, 4])
    qml.CNOT(wires=[4, 25])
    qml.CNOT(wires=[25, 16])
    qml.CNOT(wires=[8, 20])
    qml.CNOT(wires=[8, 26])
    qml.Toffoli(wires=[26, 20, 8])
    qml.CNOT(wires=[9, 21])
    qml.CNOT(wires=[9, 8])
    qml.Toffoli(wires=[8, 21, 9])
    qml.CNOT(wires=[10, 22])
    qml.CNOT(wires=[10, 9])
    qml.Toffoli(wires=[9, 22, 10])
    qml.CNOT(wires=[11, 23])
    qml.CNOT(wires=[11, 10])
    qml.Toffoli(wires=[10, 23, 11])
    qml.CNOT(wires=[11, 27])
    qml.Toffoli(wires=[10, 23, 11])
    qml.CNOT(wires=[11, 10])
    qml.CNOT(wires=[10, 23])
    qml.Toffoli(wires=[9, 22, 10])
    qml.CNOT(wires=[10, 9])
    qml.CNOT(wires=[9, 22])
    qml.Toffoli(wires=[8, 21, 9])
    qml.CNOT(wires=[9, 8])
    qml.CNOT(wires=[8, 21])
    qml.Toffoli(wires=[26, 20, 8])
    qml.CNOT(wires=[8, 26])
    qml.CNOT(wires=[26, 20])
    qml.Barrier(wires=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27])

    return qml.sample(wires=range(28))

samples = circuit()

build_time = time.time() - start_build

start_transpile = time.time()

samples = np.array(samples)
if samples.ndim == 1 and num_wires > 1:
    samples = samples.reshape((1024, 28))

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

for wire in range(28):
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
num_3q = sum(ops.get(g, 0) for g in three_qubit_gates)
total_gates = num_1q + num_2q + num_3q

print("\nCircuito (texto):")
drawer = qml.draw(circuit)
print(drawer())

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