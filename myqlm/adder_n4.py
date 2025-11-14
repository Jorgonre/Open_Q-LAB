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
qbits = prog.qalloc(4)

prog.apply(X, qbits[0])
prog.apply(X, qbits[1])
prog.apply(H, qbits[3])
prog.apply(CNOT, qbits[2], qbits[3])
prog.apply(T, qbits[0])
prog.apply(T, qbits[1])
prog.apply(T, qbits[2])
prog.apply(S, qbits[3]) #Tdagger
prog.apply(S, qbits[3]) #Tdagger
prog.apply(S, qbits[3]) #Tdagger
prog.apply(T, qbits[3]) #Tdagger
prog.apply(CNOT, qbits[0], qbits[1])
prog.apply(CNOT, qbits[2], qbits[3])
prog.apply(CNOT, qbits[3], qbits[0])
prog.apply(CNOT, qbits[1], qbits[2])
prog.apply(CNOT, qbits[0], qbits[1])
prog.apply(CNOT, qbits[2], qbits[3])
prog.apply(S, qbits[0]) #Tdagger
prog.apply(S, qbits[0]) #Tdagger
prog.apply(S, qbits[0]) #Tdagger
prog.apply(T, qbits[0]) #Tdagger
prog.apply(S, qbits[1]) #Tdagger
prog.apply(S, qbits[1]) #Tdagger
prog.apply(S, qbits[1]) #Tdagger
prog.apply(T, qbits[1]) #Tdagger
prog.apply(S, qbits[2]) #Tdagger
prog.apply(S, qbits[2]) #Tdagger
prog.apply(S, qbits[2]) #Tdagger
prog.apply(T, qbits[2]) #Tdagger
prog.apply(T, qbits[3])
prog.apply(CNOT, qbits[0], qbits[1])
prog.apply(CNOT, qbits[2], qbits[3])
prog.apply(S, qbits[3])
prog.apply(CNOT, qbits[3], qbits[0])
prog.apply(H, qbits[3])

build_time = time.time() - start_build

for i in range(4):
    prog.measure(qbits[i])

start_transpile = time.time()

circuit = prog.to_circ()
qpu = PyLinalg()
job = Job(circuit=circuit, nbshots=1024)
result = qpu.submit(job)

cpu_usage = process.cpu_percent(interval=0.2)
ram_usage_mb = process.memory_info().rss / (1024 * 1024)

transpile_time = time.time() - start_transpile
total_time = time.time() - start_time

num_qubits = circuit.nbqbits
layers = []
for op in circuit.ops:
    # Verifica si op puede ir en una capa existente
    colocado = False
    for layer in layers:
        if not any(q in layer for q in op.qbits):
            layer.update(op.qbits)
            colocado = True
            break
    if not colocado:
        layers.append(set(op.qbits))
depth = len(layers)
gate_counts = circuit.ops
num_1q = sum(1 for g in gate_counts if len(g.qbits) == 1)
num_2q = sum(1 for g in gate_counts if len(g.qbits) == 2)
total_gates = len(gate_counts)

print(result[0].state)

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