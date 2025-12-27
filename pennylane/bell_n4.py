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

dev = qml.device("default.qubit", wires=4, shots=1024)

@qml.qnode(dev)
def circuit():
    qml.Hadamard(wires=0)
    qml.Hadamard(wires=1)
    qml.Hadamard(wires=3)

    qml.CNOT(wires=[0,2])
    qml.U3(np.pi * 0.5, np.pi * 0.0, np.pi * 0.75,wires=3)

    qml.RX(np.pi * (-0.25),wires=0)
    qml.U3(np.pi * 0.5, np.pi * 0.0, np.pi * 0.75,wires=1)
    qml.RY(np.pi * (-0.5),wires=2)
    qml.RX(np.pi * (0.5),wires=3)

    qml.RY(np.pi * (-0.5),wires=0)
    qml.RX(np.pi * (0.5),wires=1)
    qml.U3(np.pi * 0.5, np.pi * 0.0, np.pi * 0.25,wires=2)

    qml.U3(np.pi * 0.5, np.pi * 0.0, np.pi * 0.25,wires=0)
    qml.CNOT(wires=[3,2])

    qml.CNOT(wires=[1,0])
    qml.RY(np.pi * (0.5),wires=2)
    qml.RX(np.pi * (0.25),wires=3)

    qml.RY(np.pi * (0.5),wires=0)
    qml.RX(np.pi * (0.25),wires=1)
    qml.CNOT(wires=[2,3])

    qml.CNOT(wires=[0,1])
    qml.RX(np.pi * (-0.5),wires=2)

    qml.RX(np.pi * (-0.5),wires=0)
    qml.RZ(np.pi * (0.5),wires=2)

    qml.RZ(np.pi * (0.5),wires=0)
    qml.CNOT(wires=[3,2])

    qml.CNOT(wires=[1,0])
    qml.U3(np.pi * 0.5, np.pi * 1.0, np.pi * 1.0,wires=2)
    qml.U3(np.pi * 0.5, np.pi * 0.5, np.pi * 1.0,wires=3)

    qml.U3(np.pi * 0.5, np.pi * 1.0, np.pi * 1.0,wires=0)
    qml.U3(np.pi * 0.5, np.pi * 0.5, np.pi * 1.0,wires=1)
    qml.RY(np.pi * (0.5),wires=2)

    qml.RY(np.pi * (0.5),wires=0)

    return qml.sample(wires=range(4))

samples = circuit()

build_time = time.time() - start_build

start_transpile = time.time()

samples = np.array(samples)
if samples.ndim == 1 and num_wires > 1:
    samples = samples.reshape((1024, 4))

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

for wire in range(4):
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
one_qubit_gates = ["PauliX", "Hadamard", "T", "S", "RX", "RY", "RZ", "U3"]
two_qubit_gates = ["CNOT"]

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