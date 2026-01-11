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

def majority(qc, a, b, c):
    """Puerta Majority: calcula el acarreo (carry)"""
    qc.append(cirq.CNOT(c, b))
    qc.append(cirq.CNOT(c, a))
    qc.append(cirq.CCNOT(a, b, c))

def unmajority(qc, a, b, c):
    """Puerta Unmajority: deshace el cálculo (uncomputation)"""
    qc.append(cirq.CCNOT(a, b, c))
    qc.append(cirq.CNOT(c, a))
    qc.append(cirq.CNOT(a, b))

def add4(qc, a, b, cin, cout):
    """
    Suma dos registros de 4 qubits (a y b).
    El resultado se guarda en b.
    cin: qubit de acarreo de entrada
    cout: qubit de acarreo de salida
    """
    majority(qc, cin, b[0], a[0])
    majority(qc, a[0], b[1], a[1])
    majority(qc, a[1], b[2], a[2])
    majority(qc, a[2], b[3], a[3])

    #acarreo de salida
    qc.append(cirq.CNOT(a[3], cout))

    unmajority(qc, a[2], b[3], a[3])
    unmajority(qc, a[1], b[2], a[2])
    unmajority(qc, a[0], b[1], a[1])
    unmajority(qc, cin, b[0], a[0])

# prefix='carry' generará: carry0, carry1
qreg_carry = cirq.NamedQubit.range(2, prefix='carry') 

# prefix='a' generará: a0, a1, ... a7
qreg_a = cirq.NamedQubit.range(8, prefix='a')     

# prefix='b' generará: b0, b1, ... b7
qreg_b = cirq.NamedQubit.range(8, prefix='b')

circuit = cirq.Circuit()

circuit.append(cirq.X.on_each(*qreg_a))

circuit.append(cirq.X.on_each(*qreg_b))

add4(circuit, qreg_a[0:4], qreg_b[0:4], qreg_carry[0], qreg_carry[1])

add4(circuit, qreg_a[4:8], qreg_b[4:8], qreg_carry[1], qreg_carry[0])

circuit.append(cirq.measure(qreg_b[0], key="m0"))
circuit.append(cirq.measure(qreg_b[1], key="m1"))
circuit.append(cirq.measure(qreg_b[2], key="m2"))
circuit.append(cirq.measure(qreg_b[3], key="m3"))
circuit.append(cirq.measure(qreg_b[4], key="m4"))
circuit.append(cirq.measure(qreg_b[5], key="m5"))
circuit.append(cirq.measure(qreg_b[6], key="m6"))
circuit.append(cirq.measure(qreg_b[7], key="m7"))

# Medimos el acarreo final
circuit.append(cirq.measure(qreg_carry[0], key="m8"))

build_time = time.time() - start_build

start_transpile = time.time()

context = cirq.TransformerContext(logger=cirq.TransformerLogger())
#optimized_circuit = optimize_circuit(circuit, context)

# El tiempo de transpilación es el tiempo que toma esta optimización

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

for i in range(9):
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

# 2. Construimos la lista de cadenas (ej: "1010") disparo a disparo
bitstrings = []
for i in range(1024):
    # Ordenamos como q3 q2 q1 q0 (Big Endian) para que se lea natural
    # str(int(...)) asegura que sea "0" o "1" limpio
    s = str(int(m0[i])) + str(int(m1[i])) + str(int(m2[i])) + str(int(m3[i])) + str(int(m4[i])) + str(int(m5[i])) + str(int(m6[i])) + str(int(m7[i])) + str(int(m8[i]))
    bitstrings.append(s)

# 3. Contamos cuántas veces sale cada una
counts = Counter(bitstrings)

# 4. Imprimimos con print normal y corriente
for estado, cantidad in counts.items():
    probabilidad = cantidad / 1024
    print(f"|{estado}> {probabilidad}")

# --- CONTAR PUERTAS EN CIRQ  ---

num_1q = -9 #No contamos las measurements gates
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