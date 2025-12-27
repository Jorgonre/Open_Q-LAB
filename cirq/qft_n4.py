import cirq
import numpy as np
from collections import Counter
import psutil
import time
import os

def optimize_circuit(circuit, context=None, k=2):
    # Merge 2-qubit connected components into circuit operations.
    optimized_circuit = cirq.merge_k_qubit_unitaries(
        circuit, k=k, rewriter=lambda op: op.with_tags("merged"), context=context
    )

    # Drop operations with negligible effect / close to identity.
    optimized_circuit = cirq.drop_negligible_operations(optimized_circuit, context=context)

    # Expand all remaining merged connected components.
    optimized_circuit = cirq.expand_composite(
        optimized_circuit, no_decomp=lambda op: "merged" not in op.tags, context=context
    )

    # Synchronize terminal measurements to be in the same moment.
    optimized_circuit = cirq.synchronize_terminal_measurements(optimized_circuit, context=context)

    # Assert the original and optimized circuit are equivalent.
    cirq.testing.assert_circuits_with_terminal_measurements_are_equivalent(
        circuit, optimized_circuit
    )

    return optimized_circuit

process = psutil.Process(os.getpid())

process.cpu_percent(interval=None)  # Establece línea base

start_time = time.time()
# Medir tiempo de construcción
start_build = time.time()

q = cirq.LineQubit.range(4)

circuit = cirq.Circuit()

circuit.append(cirq.X(q[0]))
circuit.append(cirq.X(q[2]))

circuit.append(cirq.H(q[0]), strategy=cirq.InsertStrategy.NEW) #Para añadir la barrera

circuit.append(cirq.cphase(np.pi / 2).on(q[1], q[0]))

circuit.append(cirq.H(q[1]))

circuit.append(cirq.cphase(np.pi / 4).on(q[2], q[0]))

circuit.append(cirq.cphase(np.pi / 2).on(q[2], q[1]))

circuit.append(cirq.H(q[2]))

circuit.append(cirq.cphase(np.pi / 8).on(q[3], q[0]))

circuit.append(cirq.cphase(np.pi / 4).on(q[3], q[1]))

circuit.append(cirq.cphase(np.pi / 2).on(q[3], q[2]))

circuit.append(cirq.H(q[3]))

circuit.append(cirq.measure(q[0], key="m0"))
circuit.append(cirq.measure(q[1], key="m1"))
circuit.append(cirq.measure(q[2], key="m2"))
circuit.append(cirq.measure(q[3], key="m3"))

build_time = time.time() - start_build

start_transpile = time.time()

context = cirq.TransformerContext(logger=cirq.TransformerLogger())
optimized_circuit = optimize_circuit(circuit, context)

# El tiempo de transpilación es el tiempo que toma esta optimización
transpile_time = time.time() - start_transpile

total_time = time.time() - start_time

# Resultados
sim = cirq.Simulator()
result = sim.run(optimized_circuit, repetitions=1024)

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
print(f"Transpile_execution_time:{transpile_time:.4f}")
print(f"Total_time:{total_time:.4f}")
print(f"CPU_usage:{cpu_usage:.2f}")
print(f"RAM_usage_MB:{ram_usage_mb:.2f}")
print("# --- END_METRICS ---")