import cirq
from cirq.circuits.qasm_output import QasmUGate
import numpy as np
from collections import Counter
import psutil
import time
import os

"""
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
"""

process = psutil.Process(os.getpid())

process.cpu_percent(interval=None)  # Establece línea base

start_time = time.time()
# Medir tiempo de construcción
start_build = time.time()

circuit = cirq.Circuit()

# Registro q
q = [cirq.NamedQubit(str(i)) for i in range(28)]

circuit.append(cirq.X(q[1]))
circuit.append(cirq.X(q[2]))
circuit.append(cirq.X(q[3]))
circuit.append(cirq.X(q[4]))
circuit.append(cirq.X(q[5]))
circuit.append(cirq.X(q[6]))
circuit.append(cirq.X(q[7]))
circuit.append(cirq.X(q[8]))
circuit.append(cirq.X(q[9]))
circuit.append(cirq.X(q[10]))
circuit.append(cirq.X(q[11]))
circuit.append(cirq.X(q[12]))
circuit.append(cirq.X(q[24]))
circuit.append(cirq.CNOT(q[0],q[12]))
circuit.append(cirq.CNOT(q[0],q[24]))
circuit.append(cirq.CCNOT(q[24],q[12],q[0]))
circuit.append(cirq.CNOT(q[1],q[13]))
circuit.append(cirq.CNOT(q[1],q[0]))
circuit.append(cirq.CCNOT(q[0],q[13],q[1]))
circuit.append(cirq.CNOT(q[2],q[14]))
circuit.append(cirq.CNOT(q[2],q[1]))
circuit.append(cirq.CCNOT(q[1],q[14],q[2]))
circuit.append(cirq.CNOT(q[3],q[15]))
circuit.append(cirq.CNOT(q[3],q[2]))
circuit.append(cirq.CCNOT(q[2],q[15],q[3]))
circuit.append(cirq.CNOT(q[3],q[25]))
circuit.append(cirq.CCNOT(q[2],q[15],q[3]))
circuit.append(cirq.CNOT(q[3],q[2]))
circuit.append(cirq.CNOT(q[2],q[15]))
circuit.append(cirq.CCNOT(q[1],q[14],q[2]))
circuit.append(cirq.CNOT(q[2],q[1]))
circuit.append(cirq.CNOT(q[1],q[14]))
circuit.append(cirq.CCNOT(q[0],q[13],q[1]))
circuit.append(cirq.CNOT(q[1],q[0]))
circuit.append(cirq.CNOT(q[0],q[13]))
circuit.append(cirq.CCNOT(q[24],q[12],q[0]))
circuit.append(cirq.CNOT(q[0],q[24]))
circuit.append(cirq.CNOT(q[24],q[12]))
circuit.append(cirq.CNOT(q[4],q[16]))
circuit.append(cirq.CNOT(q[4],q[25]))
circuit.append(cirq.CCNOT(q[25],q[16],q[4]))
circuit.append(cirq.CNOT(q[5],q[17]))
circuit.append(cirq.CNOT(q[5],q[4]))
circuit.append(cirq.CCNOT(q[4],q[17],q[5]))
circuit.append(cirq.CNOT(q[6],q[18]))
circuit.append(cirq.CNOT(q[6],q[5]))
circuit.append(cirq.CCNOT(q[5],q[18],q[6]))
circuit.append(cirq.CNOT(q[7],q[19]))
circuit.append(cirq.CNOT(q[7],q[6]))
circuit.append(cirq.CCNOT(q[6],q[19],q[7]))
circuit.append(cirq.CNOT(q[7],q[26]))
circuit.append(cirq.CCNOT(q[6],q[19],q[7]))
circuit.append(cirq.CNOT(q[7],q[6]))
circuit.append(cirq.CNOT(q[6],q[19]))
circuit.append(cirq.CCNOT(q[5],q[18],q[6]))
circuit.append(cirq.CNOT(q[6],q[5]))
circuit.append(cirq.CNOT(q[5],q[18]))
circuit.append(cirq.CCNOT(q[4],q[17],q[5]))
circuit.append(cirq.CNOT(q[5],q[4]))
circuit.append(cirq.CNOT(q[4],q[17]))
circuit.append(cirq.CCNOT(q[25],q[16],q[4]))
circuit.append(cirq.CNOT(q[4],q[25]))
circuit.append(cirq.CNOT(q[25],q[16]))
circuit.append(cirq.CNOT(q[8],q[20]))
circuit.append(cirq.CNOT(q[8],q[26]))
circuit.append(cirq.CCNOT(q[26],q[20],q[8]))
circuit.append(cirq.CNOT(q[9],q[21]))
circuit.append(cirq.CNOT(q[9],q[8]))
circuit.append(cirq.CCNOT(q[8],q[21],q[9]))
circuit.append(cirq.CNOT(q[10],q[22]))
circuit.append(cirq.CNOT(q[10],q[9]))
circuit.append(cirq.CCNOT(q[9],q[22],q[10]))
circuit.append(cirq.CNOT(q[11],q[23]))
circuit.append(cirq.CNOT(q[11],q[10]))
circuit.append(cirq.CCNOT(q[10],q[23],q[11]))
circuit.append(cirq.CNOT(q[11],q[27]))
circuit.append(cirq.CCNOT(q[10],q[23],q[11]))
circuit.append(cirq.CNOT(q[11],q[10]))
circuit.append(cirq.CNOT(q[10],q[23]))
circuit.append(cirq.CCNOT(q[9],q[22],q[10]))
circuit.append(cirq.CNOT(q[10],q[9]))
circuit.append(cirq.CNOT(q[9],q[22]))
circuit.append(cirq.CCNOT(q[8],q[21],q[9]))
circuit.append(cirq.CNOT(q[9],q[8]))
circuit.append(cirq.CNOT(q[8],q[21]))
circuit.append(cirq.CCNOT(q[26],q[20],q[8]))
circuit.append(cirq.CNOT(q[8],q[26]))
circuit.append(cirq.CNOT(q[26],q[20]))

circuit.append(cirq.measure(q[0], key="m0"))
circuit.append(cirq.measure(q[1], key="m1"))
circuit.append(cirq.measure(q[2], key="m2"))
circuit.append(cirq.measure(q[3], key="m3"))
circuit.append(cirq.measure(q[4], key="m4"))
circuit.append(cirq.measure(q[5], key="m5"))
circuit.append(cirq.measure(q[6], key="m6"))
circuit.append(cirq.measure(q[7], key="m7"))
circuit.append(cirq.measure(q[8], key="m8"))
circuit.append(cirq.measure(q[9], key="m9"))
circuit.append(cirq.measure(q[10], key="m10"))
circuit.append(cirq.measure(q[11], key="m11"))
circuit.append(cirq.measure(q[12], key="m12"))
circuit.append(cirq.measure(q[13], key="m13"))
circuit.append(cirq.measure(q[14], key="m14"))
circuit.append(cirq.measure(q[15], key="m15"))
circuit.append(cirq.measure(q[16], key="m16"))
circuit.append(cirq.measure(q[17], key="m17"))
circuit.append(cirq.measure(q[18], key="m18"))
circuit.append(cirq.measure(q[19], key="m19"))
circuit.append(cirq.measure(q[20], key="m20"))
circuit.append(cirq.measure(q[21], key="m21"))
circuit.append(cirq.measure(q[22], key="m22"))
circuit.append(cirq.measure(q[23], key="m23"))
circuit.append(cirq.measure(q[24], key="m24"))
circuit.append(cirq.measure(q[25], key="m25"))
circuit.append(cirq.measure(q[26], key="m26"))
circuit.append(cirq.measure(q[27], key="m27"))

build_time = time.time() - start_build

start_transpile = time.time()

context = cirq.TransformerContext(logger=cirq.TransformerLogger())
#optimized_circuit = optimize_circuit(circuit, context)

# Resultados
sim = cirq.Simulator()
result = sim.run(circuit, repetitions=1024)

transpile_time = time.time() - start_transpile

total_time = time.time() - start_time

#print("Resultados:")
#print(result)

# Medir uso de recursos
cpu_usage = process.cpu_percent(None)
ram_usage_mb = process.memory_info().rss / (1024 * 1024)

for i in range(28):
    data = result.measurements[f"m{i}"].flatten()
    counts = Counter(data)
    total = sum(counts.values())
    p0 = counts.get(0, 0) / total
    p1 = counts.get(1, 0) / total
    print(f"q{i}: {p0:.3f} |0⟩  +  {p1:.3f} |1⟩")

# 1. Sacamos los arrays crudos de ceros y unos
# .flatten() asegura que sea una lista plana [0, 1, 0...] sin corchetes extra
m0 = result.measurements['m0'].flatten()
m1 = result.measurements['m1'].flatten()
m2 = result.measurements['m2'].flatten()
m3 = result.measurements['m3'].flatten()
m4 = result.measurements['m4'].flatten()
m5 = result.measurements['m5'].flatten()
m6 = result.measurements['m6'].flatten()
m7 = result.measurements['m7'].flatten()
m8 = result.measurements['m8'].flatten()
m9 = result.measurements['m9'].flatten()
m10 = result.measurements['m10'].flatten()
m11 = result.measurements['m11'].flatten()
m12 = result.measurements['m12'].flatten()
m13 = result.measurements['m13'].flatten()
m14 = result.measurements['m14'].flatten()
m15 = result.measurements['m15'].flatten()
m16 = result.measurements['m16'].flatten()
m17 = result.measurements['m17'].flatten()
m18 = result.measurements['m18'].flatten()
m19 = result.measurements['m19'].flatten()
m20 = result.measurements['m20'].flatten()
m21 = result.measurements['m21'].flatten()
m22 = result.measurements['m22'].flatten()
m23 = result.measurements['m23'].flatten()
m24 = result.measurements['m24'].flatten()
m25 = result.measurements['m25'].flatten()
m26 = result.measurements['m26'].flatten()
m27 = result.measurements['m27'].flatten()

# 2. Construimos la lista de cadenas (ej: "1010") disparo a disparo
bitstrings = []
for i in range(1024):
    # Ordenamos como q3 q2 q1 q0 (Big Endian) para que se lea natural
    # str(int(...)) asegura que sea "0" o "1" limpio
    s = str(int(m0[i])) + str(int(m1[i])) + str(int(m2[i])) + str(int(m3[i])) + str(int(m4[i])) + str(int(m5[i])) + str(int(m6[i])) + str(int(m7[i])) + str(int(m8[i])) + str(int(m9[i])) + str(int(m10[i]))
    bitstrings.append(s)

# 3. Contamos cuántas veces sale cada una
counts = Counter(bitstrings)

# 4. Imprimimos con print normal y corriente
for estado, cantidad in counts.items():
    probabilidad = cantidad / 1024
    print(f"|{estado}> {probabilidad}")

# --- CONTAR PUERTAS EN CIRQ (VERSIÓN SIMPLE Y CORRECTA) ---

num_1q = -28 #No contamos las measurements gates
num_2q = 0
num_3q = 0

for moment in circuit:
    for op in moment.operations:
        qubit_count = len(op.qubits)

        if qubit_count == 1:
            num_1q += 1
        elif qubit_count == 2:
            num_2q += 1
        elif qubit_count == 3:
            num_3q += 1

total_gates = num_1q + num_2q + num_3q

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
print(f"Gate_3q:{num_3q}")
print(f"Total_gates:{total_gates}")
print(f"Build_time:{build_time:.4f}")
print(f"Transpile_execution_time:{transpile_time:.4f}")
print(f"Total_time:{total_time:.4f}")
print(f"CPU_usage:{cpu_usage:.2f}")
print(f"RAM_usage_MB:{ram_usage_mb:.2f}")
print("# --- END_METRICS ---")