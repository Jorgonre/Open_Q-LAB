from qat.lang.AQASM import Program, H, CNOT, X, T, S, AbstractGate, PH
from qat.qpus import PyLinalg
from qat.core import Job
import psutil
import os
import time
import numpy as np

process = psutil.Process(os.getpid())

process.cpu_percent(interval=None)  # Establece línea base

start_time = time.time()
# Medir tiempo de construcción
start_build = time.time()

BARRIER = AbstractGate("BARRIER", [], arity=1)

prog = Program()
qbits = prog.qalloc(4)

prog.apply(X, qbits[0])
prog.apply(X, qbits[2])

prog.apply(BARRIER(), qbits[0])
prog.apply(BARRIER(), qbits[1])
prog.apply(BARRIER(), qbits[2])
prog.apply(BARRIER(), qbits[3])

prog.apply(H, qbits[0])

prog.apply(PH(np.pi / 2).ctrl(), qbits[1], qbits[0]) #control phase

prog.apply(H, qbits[1])

prog.apply(PH(np.pi / 4).ctrl(), qbits[2], qbits[0]) #control phase

prog.apply(PH(np.pi / 2).ctrl(), qbits[2], qbits[1]) #control phase

prog.apply(H, qbits[2])

prog.apply(PH(np.pi / 8).ctrl(), qbits[3], qbits[0])

prog.apply(PH(np.pi / 4).ctrl(), qbits[3], qbits[1])

prog.apply(PH(np.pi / 2).ctrl(), qbits[3], qbits[2])

prog.apply(H, qbits[3])

build_time = time.time() - start_build

for i in range(4):
    prog.measure(qbits[i])

start_transpile = time.time()

circuit = prog.to_circ()
qpu = PyLinalg()
job = Job(circuit=circuit, nbshots=1024)
result = qpu.submit(job)

cpu_usage = process.cpu_percent(None)
ram_usage_mb = process.memory_info().rss / (1024 * 1024)

transpile_time = time.time() - start_transpile
total_time = time.time() - start_time

num_qubits = circuit.nbqbits

# Calcula depth estilo Qiskit
last_layer_for_qubit = {}
depth = 0

for op in circuit.ops:
    qubits = op.qbits
    
    # capa mínima donde puede ir esta operación
    min_layer = 0
    for q in qubits:
        if q in last_layer_for_qubit:
            min_layer = max(min_layer, last_layer_for_qubit[q] + 1)

    # asignar operación a la capa min_layer
    depth = max(depth, min_layer)
    
    # actualizar última capa donde se usa cada qubit
    for q in qubits:
        last_layer_for_qubit[q] = min_layer

depth = depth + 1  # capas empiezan en 0

gate_counts = circuit.ops
num_1q = sum(1 for g in gate_counts if len(g.qbits) == 1) - 4  #Resta por measure gates
num_2q = sum(1 for g in gate_counts if len(g.qbits) == 2)
total_gates = num_1q + num_2q

print(result[0].state)

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