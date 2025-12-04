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

circ = Circuit(4)

circ.X(0)
circ.X(2)

circ.add_barrier([0,1,2,3])

circ.H(0)

circ.CU1(0.5,1,0)

circ.H(1)

circ.CU1(0.25,2,0)

circ.CU1(0.5,2,1)

circ.H(2)

circ.CU1(0.125,3,0)

circ.CU1(0.25,3,1)

circ.CU1(0.5,3,2)

circ.H(3)

circ.measure_all()

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
    if optype in [OpType.X, OpType.H, OpType.T, OpType.S]:
        num_1q += 1
    elif optype in [OpType.CX,OpType.CU1]:
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
