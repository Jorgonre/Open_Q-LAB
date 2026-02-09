from qat.lang.AQASM import Program, H, CNOT, X, T, S
from qat.qpus import PyLinalg
from qat.core import Job
import psutil
import os
import time

process = psutil.Process(os.getpid())

process.cpu_percent(interval=None)  # Establece línea base

start_time = time.time()
# Medir tiempo de construcción
start_build = time.time()

prog = Program()
qbits = prog.qalloc(28)

prog.apply(X, qbits[1])
prog.apply(X, qbits[2])
prog.apply(X, qbits[3])
prog.apply(X, qbits[4])
prog.apply(X, qbits[5])
prog.apply(X, qbits[6])
prog.apply(X, qbits[7])
prog.apply(X, qbits[8])
prog.apply(X, qbits[9])
prog.apply(X, qbits[10])
prog.apply(X, qbits[11])
prog.apply(X, qbits[12])
prog.apply(X, qbits[24])

prog.apply(CNOT, qbits[0], qbits[12])
prog.apply(CNOT, qbits[0], qbits[24])
prog.apply(CCNOT, qbits[24], qbits[12],qbits[0])
prog.apply(CNOT, qbits[1], qbits[13])
prog.apply(CNOT, qbits[1], qbits[0])
prog.apply(CCNOT, qbits[0], qbits[13],qbits[1])
prog.apply(CNOT, qbits[2], qbits[14])
prog.apply(CNOT, qbits[2], qbits[1])
prog.apply(CCNOT, qbits[1], qbits[14],qbits[2])
prog.apply(CNOT, qbits[3], qbits[15])
prog.apply(CNOT, qbits[3], qbits[2])
prog.apply(CCNOT, qbits[2], qbits[15],qbits[3])
prog.apply(CNOT, qbits[3], qbits[25])
prog.apply(CCNOT, qbits[2], qbits[15],qbits[3])
prog.apply(CNOT, qbits[3], qbits[2])
prog.apply(CNOT, qbits[2], qbits[15])
prog.apply(CCNOT, qbits[1], qbits[14],qbits[2])
prog.apply(CNOT, qbits[2], qbits[1])
prog.apply(CNOT, qbits[1], qbits[14])
prog.apply(CCNOT, qbits[0], qbits[13],qbits[1])
prog.apply(CNOT, qbits[1], qbits[0])
prog.apply(CNOT, qbits[0], qbits[13])
prog.apply(CCNOT, qbits[24], qbits[12],qbits[0])
prog.apply(CNOT, qbits[0], qbits[24])
prog.apply(CNOT, qbits[24], qbits[12])
prog.apply(CNOT, qbits[4], qbits[16])
prog.apply(CNOT, qbits[4], qbits[25])
prog.apply(CCNOT, qbits[25], qbits[16],qbits[4])
prog.apply(CNOT, qbits[5], qbits[17])
prog.apply(CNOT, qbits[5], qbits[4])
prog.apply(CCNOT, qbits[4], qbits[17],qbits[5])
prog.apply(CNOT, qbits[6], qbits[18])
prog.apply(CNOT, qbits[6], qbits[5])
prog.apply(CCNOT, qbits[5], qbits[18],qbits[6])
prog.apply(CNOT, qbits[7], qbits[19])
prog.apply(CNOT, qbits[7], qbits[6])
prog.apply(CCNOT, qbits[6], qbits[19],qbits[7])
prog.apply(CNOT, qbits[7], qbits[26])
prog.apply(CCNOT, qbits[6], qbits[19],qbits[7])
prog.apply(CNOT, qbits[7], qbits[6])
prog.apply(CNOT, qbits[6], qbits[19])
prog.apply(CCNOT, qbits[5], qbits[18],qbits[6])
prog.apply(CNOT, qbits[6], qbits[5])
prog.apply(CNOT, qbits[5], qbits[18])
prog.apply(CCNOT, qbits[4], qbits[17],qbits[5])
prog.apply(CNOT, qbits[5], qbits[4])
prog.apply(CNOT, qbits[4], qbits[17])
prog.apply(CCNOT, qbits[25], qbits[16],qbits[4])
prog.apply(CNOT, qbits[4], qbits[25])
prog.apply(CNOT, qbits[25], qbits[16])
prog.apply(CNOT, qbits[8], qbits[20])
prog.apply(CNOT, qbits[8], qbits[26])
prog.apply(CCNOT, qbits[26], qbits[20],qbits[8])
prog.apply(CNOT, qbits[9], qbits[21])
prog.apply(CNOT, qbits[9], qbits[8])
prog.apply(CCNOT, qbits[8], qbits[21],qbits[9])
prog.apply(CNOT, qbits[10], qbits[22])
prog.apply(CNOT, qbits[10], qbits[9])
prog.apply(CCNOT, qbits[9], qbits[22],qbits[10])
prog.apply(CNOT, qbits[11], qbits[23])
prog.apply(CNOT, qbits[11], qbits[10])
prog.apply(CCNOT, qbits[10], qbits[23],qbits[11])
prog.apply(CNOT, qbits[11], qbits[27])
prog.apply(CCNOT, qbits[10], qbits[23],qbits[11])
prog.apply(CNOT, qbits[11], qbits[10])
prog.apply(CNOT, qbits[10], qbits[23])
prog.apply(CCNOT, qbits[9], qbits[22],qbits[10])
prog.apply(CNOT, qbits[10], qbits[9])
prog.apply(CNOT, qbits[9], qbits[22])
prog.apply(CCNOT, qbits[8], qbits[21],qbits[9])
prog.apply(CNOT, qbits[9], qbits[8])
prog.apply(CNOT, qbits[8], qbits[21])
prog.apply(CCNOT, qbits[26], qbits[20],qbits[8])
prog.apply(CNOT, qbits[8], qbits[26])
prog.apply(CNOT, qbits[26], qbits[20])

build_time = time.time() - start_build

for i in range(28):
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
num_1q = sum(1 for g in gate_counts if len(g.qbits) == 1) - 28  #Resta por measure gates
num_2q = sum(1 for g in gate_counts if len(g.qbits) == 2)
num_3q = sum(1 for g in gate_counts if len(g.qbits) == 3)
total_gates = num_1q + num_2q + num_3q

print(result[0].state)

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