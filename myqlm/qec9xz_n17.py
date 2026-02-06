from qat.lang import Program, H, CNOT, X, T, S, AbstractGate, PH, qrout, CSIGN, Z, CCNOT, RZ, RX, RY
from qat.qpus import PyLinalg, get_default_qpu
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

prog = Program()
q0 = prog.qalloc(9)
q1 = prog.qalloc(8)
c0 = prog.calloc(8)

prog.apply(H,q0[0])
prog.apply(CNOT, q0[0], q0[3])
prog.apply(CNOT, q0[0], q0[6])
prog.apply(H,q0[0])
prog.apply(H,q0[3])
prog.apply(H,q0[6])
prog.apply(CNOT, q0[0], q0[1])
prog.apply(CNOT, q0[0], q0[2])
prog.apply(CNOT, q0[3], q0[4])
prog.apply(CNOT, q0[3], q0[5])
prog.apply(CNOT, q0[6], q0[7])
prog.apply(CNOT, q0[6], q0[8])
prog.apply(CNOT, q0[0], q1[0])
prog.apply(CNOT, q0[1], q1[0])
prog.apply(CNOT, q0[1], q1[1])
prog.apply(CNOT, q0[2], q1[1])
prog.apply(CNOT, q0[3], q1[2])
prog.apply(CNOT, q0[4], q1[2])
prog.apply(CNOT, q0[4], q1[3])
prog.apply(CNOT, q0[5], q1[3])
prog.apply(CNOT, q0[6], q1[4])
prog.apply(CNOT, q0[7], q1[4])
prog.apply(CNOT, q0[7], q1[5])
prog.apply(CNOT, q0[8], q1[5])
prog.measure(q1[0], c0[0])
prog.measure(q1[1], c0[1])
prog.measure(q1[2], c0[2])
prog.measure(q1[3], c0[3])
prog.measure(q1[4], c0[4])
prog.measure(q1[5], c0[5])
prog.apply(H,q0[0])
prog.apply(H,q0[1])
prog.apply(H,q0[2])
prog.apply(H,q0[3])
prog.apply(H,q0[4])
prog.apply(H,q0[5])
prog.apply(H,q0[6])
prog.apply(H,q0[7])
prog.apply(H,q0[8])
prog.apply(CNOT, q0[0], q1[6])
prog.apply(CNOT, q0[3], q1[7])
prog.apply(CNOT, q0[1], q1[6])
prog.apply(CNOT, q0[4], q1[7])
prog.apply(CNOT, q0[2], q1[6])
prog.apply(CNOT, q0[5], q1[7])
prog.apply(CNOT, q0[3], q1[6])
prog.apply(CNOT, q0[6], q1[7])
prog.apply(CNOT, q0[4], q1[6])
prog.apply(CNOT, q0[7], q1[7])
prog.apply(CNOT, q0[5], q1[6])
prog.apply(CNOT, q0[8], q1[7])
prog.measure(q1[6], c0[6])
prog.measure(q1[7], c0[7])
prog.apply(H,q0[0])
prog.apply(H,q0[1])
prog.apply(H,q0[2])
prog.apply(H,q0[3])
prog.apply(H,q0[4])
prog.apply(H,q0[5])
prog.apply(H,q0[6])
prog.apply(H,q0[7])

build_time = time.time() - start_build

circuit = prog.to_circ()

start_transpile = time.time()

qpu = get_default_qpu()
job = circuit.to_job(nbshots=1024)
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
            min_layer = max(min_layer, last_layer_for_qubitq + 1)

    # asignar operación a la capa min_layer
    depth = max(depth, min_layer)
    
    # actualizar última capa donde se usa cada qubit
    for q in qubits:
        last_layer_for_qubitq = min_layer

depth = depth + 1  # capas emnp.piezan en 0

gate_counts = circuit.ops
num_1q = sum(1 for g in gate_counts if len(g.qbits) == 1) - 8 #por measure
num_2q = sum(1 for g in gate_counts if len(g.qbits) == 2)
total_gates = num_1q + num_2q

for sample in result:
    print(sample.state, sample.probability)

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