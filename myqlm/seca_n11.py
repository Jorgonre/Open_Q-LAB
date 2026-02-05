from qat.lang import Program, H, CNOT, X, T, S, AbstractGate, PH, qrout, CSIGN, Z, CCNOT
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

BARRIER = AbstractGate("BARRIER", [], arity=1)

BARRIER.set_matrix_generator(lambda: np.eye(2))

prog = Program()
qbits = prog.qalloc(11)

@qrout
def seca():
    """
    Corrección de errores y teleportación
    """
    
    Z(0)
    H(0)
    
    for i in range (11):
        BARRIER()(i)

    CNOT(0,3)
    CNOT(0,6)
    CSIGN(0,3)
    CSIGN(0,6)

    H(0)
    H(3)
    H(6)
    Z(0)
    Z(3)
    Z(6)

    CNOT(0,1)
    CNOT(0,2)
    CNOT(3,4)
    CNOT(3,5)
    CNOT(6,7)
    CNOT(6,8)
    CSIGN(0,1)
    CSIGN(0,2)
    CSIGN(3,4)
    CSIGN(3,5)
    CSIGN(6,7)
    CSIGN(6,8)

    for i in range (11):
        BARRIER()(i)
    
    H(9)
    CNOT(9,10)

    for i in range (11):
        BARRIER()(i)
    
    CNOT(0,9)

    H(0)
    CNOT(9,10)

    CSIGN(0,10)

    for i in range (11):
        BARRIER()(i)
    
    CNOT(10, 1)
    CNOT(10, 2)
    CNOT(3, 4)
    CNOT(3, 5)
    CNOT(6, 7)
    CNOT(6, 8)
    CSIGN(10, 1)
    CSIGN(10, 2)
    CSIGN(3, 4)
    CSIGN(3, 5)
    CSIGN(6, 7)
    CSIGN(6, 8)

    CCNOT(1, 2, 10)
    CCNOT(5, 4, 3)
    CCNOT(8, 7, 6)

    for i in range (11):
        BARRIER()(i)
    
    H(10)
    CCNOT(1, 2, 10)
    H(10)
    H(3)
    CCNOT(5, 4, 3)
    H(3)
    H(6)
    CCNOT(8, 7, 6)
    H(6)

    for i in range (11):
        BARRIER()(i)
    
    H(10)
    H(3)
    H(6)
    Z(10)
    Z(3)
    Z(6)
    CNOT(10, 3)
    CNOT(10, 6)
    CSIGN(10, 3)
    CSIGN(10, 6)
    CCNOT(3, 6, 10)
    H(10)
    CCNOT(3, 6, 10)
    H(10)

    for i in range (11):
        BARRIER()(i)
    
    H(10)
    Z(10)

build_time = time.time() - start_build

#for i in range(4):
#    prog.measure(qbits[i])

start_transpile = time.time()

job = seca.to_job(nbshots=1024)
result = get_default_qpu().submit(job)

cpu_usage = process.cpu_percent(None)
ram_usage_mb = process.memory_info().rss / (1024 * 1024)

transpile_time = time.time() - start_transpile
total_time = time.time() - start_time

num_qubits = seca.nbqbits

# Calcula depth estilo Qiskit
last_layer_for_qubit = {}
depth = 0

for op in seca.ops:
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

gate_counts = seca.ops
num_1q = sum(1 for g in gate_counts if len(g.qbits) == 1) - 77 #Resta barriers
num_2q = sum(1 for g in gate_counts if len(g.qbits) == 2)
num_3q = sum(1 for g in gate_counts if len(g.qbits) == 3)
total_gates = num_1q + num_2q + num_3q

for sample in result:
    print(sample.state, sample.probability)

print(seca)

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