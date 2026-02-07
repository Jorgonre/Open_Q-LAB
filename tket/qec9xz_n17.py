from pytket import Circuit, OpType
from pytket.extensions.qiskit import AerBackend
import time
import psutil
import os

process = psutil.Process(os.getpid())

process.cpu_percent(interval=None)  # Establece línea base

start_time = time.time()
# Medir tiempo de construcción
start_build = time.time()

n_qubits = 17
n_bits = 8
circ = Circuit(n_qubits, n_bits)

q0 = list(range(0, 9))
q1 = list(range(9, 17))

circ.H(q0[0])
circ.CX(q0[0], q0[3])
circ.CX(q0[0], q0[6])
circ.H(q0[0])
circ.H(q0[3])
circ.H(q0[6])
circ.CX(q0[0], q0[1])
circ.CX(q0[0], q0[2])
circ.CX(q0[3], q0[4])
circ.CX(q0[3], q0[5])
circ.CX(q0[6], q0[7])
circ.CX(q0[6], q0[8])
circ.CX(q0[0], q1[0])
circ.CX(q0[1], q1[0])
circ.CX(q0[1], q1[1])
circ.CX(q0[2], q1[1])
circ.CX(q0[3], q1[2])
circ.CX(q0[4], q1[2])
circ.CX(q0[4], q1[3])
circ.CX(q0[5], q1[3])
circ.CX(q0[6], q1[4])
circ.CX(q0[7], q1[4])
circ.CX(q0[7], q1[5])
circ.CX(q0[8], q1[5])
circ.H(q0[0])
circ.H(q0[1])
circ.H(q0[2])
circ.H(q0[3])
circ.H(q0[4])
circ.H(q0[5])
circ.H(q0[6])
circ.H(q0[7])
circ.H(q0[8])
circ.CX(q0[0], q1[6])
circ.CX(q0[3], q1[7])
circ.CX(q0[1], q1[6])
circ.CX(q0[4], q1[7])
circ.CX(q0[2], q1[6])
circ.CX(q0[5], q1[7])
circ.CX(q0[3], q1[6])
circ.CX(q0[6], q1[7])
circ.CX(q0[4], q1[6])
circ.CX(q0[7], q1[7])
circ.CX(q0[5], q1[6])
circ.CX(q0[8], q1[7])
circ.H(q0[0])
circ.H(q0[1])
circ.H(q0[2])
circ.H(q0[3])
circ.H(q0[4])
circ.H(q0[5])
circ.H(q0[6])
circ.H(q0[7])

circ.add_c_register("bits_resultado", 8)

for i in range(8):
    circ.Measure(9 + i, i) 

build_time = time.time() - start_build

start_transpile = time.time()

print("Circuito:")
print(circ)

backend = AerBackend()
compiled = backend.get_compiled_circuit(circ) #Momento de la transpilación.
result = backend.run_circuit(compiled, n_shots=1024)

transpile_time = time.time() - start_transpile

# Medir uso de recursos
cpu_usage = process.cpu_percent(None)
ram_usage_mb = process.memory_info().rss / (1024 * 1024)

print("\nResultados:")
print(result.get_counts())

total_time = time.time() - start_time

# --- Contar operaciones sin Counter ---
num_1q = 0
num_2q = 0

for cmd in circ.get_commands():
    optype = cmd.op.type
    if optype in [OpType.X, OpType.H, OpType.T, OpType.S, OpType.U3, OpType.Rx, OpType.Ry, OpType.Rz, OpType.Z]:
        num_1q += 1
    elif optype in [OpType.CX,OpType.CZ]:
        num_2q += 1

# Número de qubits
num_qubits = circ.n_qubits

total_gates = num_1q + num_2q

# Profundidad
depth = circ.depth()

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
