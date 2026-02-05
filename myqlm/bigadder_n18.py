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

def majority(prog, a, b, c):
    """Puerta Majority: calcula el acarreo (carry)"""
    prog.apply(CNOT,c,b)
    prog.apply(CNOT,c,a)
    prog.apply(CCNOT,a,b,c)

def unmajority(prog, a, b, c):
    """Puerta Majority: calcula el acarreo (carry)"""
    prog.apply(CCNOT,a,b,c)
    prog.apply(CNOT,c,a)
    prog.apply(CNOT,a,b)

def add4(prog, a, b, cin, cout):
    """
    Suma dos registros de 4 qubits (a y b).
    El resultado se guarda en b.
    cin: qubit de acarreo de entrada
    cout: qubit de acarreo de salida
    """
    majority(prog, cin, b[0], a[0])
    majority(prog, a[0], b[1], a[1])
    majority(prog, a[1], b[2], a[2])
    majority(prog, a[2], b[3], a[3])

    #acarreo de salida
    prog.apply(CNOT,a[3], cout)

    unmajority(prog, a[2], b[3], a[3])
    unmajority(prog, a[1], b[2], a[2])
    unmajority(prog, a[0], b[1], a[1])
    unmajority(prog, cin, b[0], a[0])

prog = Program()

q_carry = prog.qalloc(2)
q_a = prog.qalloc(8)
q_b = prog.qalloc(8)

for i in range(8):
    prog.apply(X, q_a[i])
    prog.apply(X, q_b[i])

add4(prog, q_a[0:4], q_b[0:4], q_carry[0], q_carry[1])
    
add4(prog, q_a[4:8], q_b[4:8], q_carry[1], q_carry[0])

build_time = time.time() - start_build

c_carry = prog.calloc(1)
c_b = prog.calloc(8)

for i in range(8):
    prog.measure(q_b[i], c_b[i])

prog.measure(q_carry[0], c_carry[0])

start_transpile = time.time()

circuit = prog.to_circ()
qpu = get_default_qpu()
qubits_medidos = list(range(10, 18)) + [0] 
job = Job(circuit=circuit, nbshots=1024, qubits=qubits_medidos)
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
num_1q = sum(1 for g in gate_counts if len(g.qbits) == 1) - 9  #Resta por measure gates
num_2q = sum(1 for g in gate_counts if len(g.qbits) == 2)
num_3q = sum(1 for g in gate_counts if len(g.qbits) == 3)
total_gates = num_1q + num_2q + num_3q

print(f"{result[0].state}: {result[0].probability}")

#print(circuit)

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