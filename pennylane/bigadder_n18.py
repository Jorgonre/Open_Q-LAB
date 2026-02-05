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

wires_carry = list(range(0, 2))
wires_a = list(range(2, 10))
wires_b = list(range(10, 18))
all_wires = wires_a + wires_b + wires_carry # Total 18

dev = qml.device("default.qubit", wires = all_wires, shots=1024)

def majority(a, b, c):
    """Puerta Majority"""
    qml.CNOT(wires=[c, b])
    qml.CNOT(wires=[c, a])
    qml.Toffoli(wires=[a, b, c])

def unmajority(a, b, c):
    """Puerta Unmajority"""
    qml.Toffoli(wires=[a, b, c])
    qml.CNOT(wires=[c, a])
    qml.CNOT(wires=[a, b])

def add4(a_wires, b_wires, cin, cout):
    """Bloque sumador de 4 bits"""
    # Majority steps
    majority(cin, b_wires[0], a_wires[0])
    majority(a_wires[0], b_wires[1], a_wires[1])
    majority(a_wires[1], b_wires[2], a_wires[2])
    majority(a_wires[2], b_wires[3], a_wires[3])
    
    # Escribir en acarreo de salida
    qml.CNOT(wires=[a_wires[3], cout])
    
    # Unmajority steps
    unmajority(a_wires[2], b_wires[3], a_wires[3])
    unmajority(a_wires[1], b_wires[2], a_wires[2])
    unmajority(a_wires[0], b_wires[1], a_wires[1])
    unmajority(cin, b_wires[0], a_wires[0])


@qml.qnode(dev)
def circuit():
    
    for w in wires_a:
        qml.PauliX(wires=w)
    for w in wires_b:
        qml.PauliX(wires=w)
    

    add4(wires_a[0:4], wires_b[0:4], wires_carry[0], wires_carry[1])
    
    add4(wires_a[4:8], wires_b[4:8], wires_carry[1], wires_carry[0])

    wires_to_measure = wires_b + [wires_carry[0]]
    
    return qml.sample(wires=wires_to_measure)

samples = circuit()

build_time = time.time() - start_build

start_transpile = time.time()

samples = np.array(samples)
if samples.ndim == 1 and num_wires > 1:
    samples = samples.reshape((1024, 18))

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

for wire in range(18):
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