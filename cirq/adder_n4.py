import cirq
import numpy as np
from collections import Counter
import psutil
import time
import os

process = psutil.Process(os.getpid())

process.cpu_percent(interval=None)  # Establece línea base

start_time = time.time()
# Medir tiempo de construcción
start_build = time.time()

# Crear 4 qubits q0, q1, q2, q3
q = cirq.LineQubit.range(4)

circuit = cirq.Circuit()

#Inicialización

circuit.append(cirq.X(q[0]))
circuit.append(cirq.X(q[1]))
circuit.append(cirq.H(q[3]))

circuit.append(cirq.CNOT(q[2],q[3]))

circuit.append(cirq.T(q[0]))
circuit.append(cirq.T(q[1]))
circuit.append(cirq.T(q[2]))
circuit.append(cirq.S(q[3])) #Tdagger
circuit.append(cirq.S(q[3])) #Tdagger
circuit.append(cirq.S(q[3])) #Tdagger
circuit.append(cirq.T(q[3])) #Tdagger

circuit.append(cirq.CNOT(q[0],q[1]))
circuit.append(cirq.CNOT(q[2],q[3]))

circuit.append(cirq.CNOT(q[3],q[0]))

circuit.append(cirq.CNOT(q[1],q[2]))

circuit.append(cirq.CNOT(q[0],q[1]))
circuit.append(cirq.CNOT(q[2],q[3]))

circuit.append(cirq.S(q[0])) #Tdagger
circuit.append(cirq.S(q[0])) #Tdagger
circuit.append(cirq.S(q[0])) #Tdagger
circuit.append(cirq.T(q[0])) #Tdagger
circuit.append(cirq.S(q[1])) #Tdagger
circuit.append(cirq.S(q[1])) #Tdagger
circuit.append(cirq.S(q[1])) #Tdagger
circuit.append(cirq.T(q[1])) #Tdagger
circuit.append(cirq.S(q[2])) #Tdagger
circuit.append(cirq.S(q[2])) #Tdagger
circuit.append(cirq.S(q[2])) #Tdagger
circuit.append(cirq.T(q[2])) #Tdagger
circuit.append(cirq.T(q[3]))

circuit.append(cirq.CNOT(q[0],q[1]))
circuit.append(cirq.CNOT(q[2],q[3]))

circuit.append(cirq.S(q[3]))

circuit.append(cirq.CNOT(q[3],q[0]))

circuit.append(cirq.H(q[3]))

# Medidas
circuit.append(cirq.measure(q[0], key="m0"))
circuit.append(cirq.measure(q[1], key="m1"))
circuit.append(cirq.measure(q[2], key="m2"))
circuit.append(cirq.measure(q[3], key="m3"))

build_time = time.time() - start_build

start_transpile = time.time()

# Resultados
sim = cirq.Simulator()
result = sim.run(circuit, repetitions=1024)

transpile_time = time.time() - start_transpile  #Por lo que tengo entendido cirq no transpila, solo simula, por eso este tiempo es tan bajo

#print("Resultados:")
#print(result)

# Medir uso de recursos
cpu_usage = process.cpu_percent(None)
ram_usage_mb = process.memory_info().rss / (1024 * 1024)

for i in range(4):
    data = result.measurements[f"m{i}"].flatten()
    counts = Counter(data)
    total = sum(counts.values())
    p0 = counts.get(0, 0) / total
    p1 = counts.get(1, 0) / total
    print(f"q{i}: {p0:.3f} |0⟩  +  {p1:.3f} |1⟩")

total_time = time.time() - start_time

# --- CONTAR PUERTAS EN CIRQ (VERSIÓN SIMPLE Y CORRECTA) ---

num_1q = -4 #No contamos las measurements gates
num_2q = 0

for moment in circuit:
    for op in moment.operations:
        qubit_count = len(op.qubits)

        if qubit_count == 1:
            num_1q += 1
        elif qubit_count == 2:
            num_2q += 1

total_gates = num_1q + num_2q

# Número de qubits
num_qubits = len(circuit.all_qubits())

# Depth (moments = capas)
depth = len(list(circuit))


print("\nCircuito traducido:")
print(circuit)

print("# --- METRICS ---")
print(f"Qubits:{num_qubits}")
print(f"Depth:{depth}")
print(f"Gate_1q:{num_1q}")
print(f"Gate_2q:{num_2q}")
print(f"Total_gates:{total_gates}")
print(f"Build_time:{build_time:.4f}")
print(f"Transpile_time:{transpile_time:.4f}")
print(f"Total_time:{total_time:.4f}")
print(f"CPU_usage:{cpu_usage:.2f}")
print(f"RAM_usage_MB:{ram_usage_mb:.2f}")
print("# --- END_METRICS ---")