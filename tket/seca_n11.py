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

circ = Circuit(11)

circ.Z(0)
circ.H(0)

circ.add_barrier([0,1,2,3,4,5,6,7,8,9,10])

circ.CX(0,3)
circ.CX(0,6)
circ.CZ(0,3)
circ.CZ(0,6)

circ.H(0)
circ.H(3)
circ.H(6)
circ.Z(0)
circ.Z(3)
circ.Z(6)

circ.CX(0,1)
circ.CX(0,2)
circ.CX(3,4)
circ.CX(3,5)
circ.CX(6,7)
circ.CX(6,8)
circ.CZ(0,1)
circ.CZ(0,2)
circ.CZ(3,4)
circ.CZ(3,5)
circ.CZ(6,7)
circ.CZ(6,8)

circ.add_barrier([0,1,2,3,4,5,6,7,8,9,10])

circ.H(9)
circ.CX(9,10)

circ.add_barrier([0,1,2,3,4,5,6,7,8,9,10])

circ.CX(0,9)

circ.H(0)
circ.CX(9,10)

circ.CZ(0,10)

circ.add_barrier([0,1,2,3,4,5,6,7,8,9,10])

circ.CX(10,1)
circ.CX(10,2)
circ.CX(3,4)
circ.CX(3,5)
circ.CX(6,7)
circ.CX(6,8)
circ.CZ(10,1)
circ.CZ(10,2)
circ.CZ(3,4)
circ.CZ(3,5)
circ.CZ(6,7)
circ.CZ(6,8)

circ.add_gate(OpType.CCX,[1,2,10])
circ.add_gate(OpType.CCX,[5,4,3])
circ.add_gate(OpType.CCX,[8,7,6])

circ.add_barrier([0,1,2,3,4,5,6,7,8,9,10])

circ.H(10)
circ.add_gate(OpType.CCX,[1,2,10])
circ.H(10)
circ.H(3)
circ.add_gate(OpType.CCX,[5,4,3])
circ.H(3)
circ.H(6)
circ.add_gate(OpType.CCX,[8,7,6])
circ.H(6)

circ.add_barrier([0,1,2,3,4,5,6,7,8,9,10])

circ.H(10)
circ.H(3)
circ.H(6)
circ.Z(10)
circ.Z(3)
circ.Z(6)
circ.CX(10,3)
circ.CX(10,6)
circ.CZ(10,3)
circ.CZ(10,6)
circ.add_gate(OpType.CCX,[3,6,10])
circ.H(10)
circ.add_gate(OpType.CCX,[1,2,10])
circ.H(10)

circ.add_barrier([0,1,2,3,4,5,6,7,8,9,10])

circ.H(10)
circ.Z(10)

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
num_3q = 0

for cmd in circ.get_commands():
    optype = cmd.op.type
    if optype in [OpType.X, OpType.H, OpType.T, OpType.S, OpType.U3, OpType.Rx, OpType.Ry, OpType.Rz, OpType.Z]:
        num_1q += 1
    elif optype in [OpType.CX,OpType.CZ]:
        num_2q += 1
    elif optype in [OpType.CCX]:
        num_3q += 1

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
print(f"Gate_3q:{num_3q}")
print(f"Total_gates:{total_gates}")
print(f"Build_time:{build_time:.4f}")
print(f"Transpile_execution_time:{transpile_time:.4f}")
print(f"Total_time:{total_time:.4f}")
print(f"CPU_usage:{cpu_usage:.2f}")
print(f"RAM_usage_MB:{ram_usage_mb:.2f}")
print("# --- END_METRICS ---")
