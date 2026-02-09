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

circuit = Circuit(28)

circuit.X(1)
circuit.X(2)
circuit.X(3)
circuit.X(4)
circuit.X(5)
circuit.X(6)
circuit.X(7)
circuit.X(8)
circuit.X(9)
circuit.X(10)
circuit.X(11)
circuit.X(12)
circuit.X(24)
circuit.CX(0,12)
circuit.CX(0,24)
circuit.CCX(24,12,0)
circuit.CX(1,13)
circuit.CX(1,0)
circuit.CCX(0,13,1)
circuit.CX(2,14)
circuit.CX(2,1)
circuit.CCX(1,14,2)
circuit.CX(3,15)
circuit.CX(3,2)
circuit.CCX(2,15,3)
circuit.CX(3,25)
circuit.CCX(2,15,3)
circuit.CX(3,2)
circuit.CX(2,15)
circuit.CCX(1,14,2)
circuit.CX(2,1)
circuit.CX(1,14)
circuit.CCX(0,13,1)
circuit.CX(1,0)
circuit.CX(0,13)
circuit.CCX(24,12,0)
circuit.CX(0,24)
circuit.CX(24,12)
circuit.CX(4,16)
circuit.CX(4,25)
circuit.CCX(25,16,4)
circuit.CX(5,17)
circuit.CX(5,4)
circuit.CCX(4,17,5)
circuit.CX(6,18)
circuit.CX(6,5)
circuit.CCX(5,18,6)
circuit.CX(7,19)
circuit.CX(7,6)
circuit.CCX(6,19,7)
circuit.CX(7,26)
circuit.CCX(6,19,7)
circuit.CX(7,6)
circuit.CX(6,19)
circuit.CCX(5,18,6)
circuit.CX(6,5)
circuit.CX(5,18)
circuit.CCX(4,17,5)
circuit.CX(5,4)
circuit.CX(4,17)
circuit.CCX(25,16,4)
circuit.CX(4,25)
circuit.CX(25,16)
circuit.CX(8,20)
circuit.CX(8,26)
circuit.CCX(26,20,8)
circuit.CX(9,21)
circuit.CX(9,8)
circuit.CCX(8,21,9)
circuit.CX(10,22)
circuit.CX(10,9)
circuit.CCX(9,22,10)
circuit.CX(11,23)
circuit.CX(11,10)
circuit.CCX(10,23,11)
circuit.CX(11,27)
circuit.CCX(10,23,11)
circuit.CX(11,10)
circuit.CX(10,23)
circuit.CCX(9,22,10)
circuit.CX(10,9)
circuit.CX(9,22)
circuit.CCX(8,21,9)
circuit.CX(9,8)
circuit.CX(8,21)
circuit.CCX(26,20,8)
circuit.CX(8,26)
circuit.CX(26,20)
circuit.add_barrier([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27])

circuit.measure_all()

build_time = time.time() - start_build

start_transpile = time.time()

print("Circuito:")
print(circuit)

backend = AerBackend()
compiled = backend.get_compiled_circuit(circuit) #Momento de la transpilación.
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

for cmd in circuit.get_commands():
    optype = cmd.op.type
    if optype in [OpType.X, OpType.H, OpType.T, OpType.S, OpType.U3, OpType.Rx, OpType.Ry, OpType.Rz, OpType.Z]:
        num_1q += 1
    elif optype in [OpType.CX,OpType.CZ]:
        num_2q += 1
    elif optype in [OpType.CCX]:
        num_3q += 1

# Número de qubits
num_qubits = circuit.n_qubits

total_gates = num_1q + num_2q

# Profundidad
depth = circuit.depth()

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
