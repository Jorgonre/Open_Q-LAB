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
def majority(circ, a, b, c):
    """Puerta Majority"""
    circ.CX(c, b)
    circ.CX(c, a)
    circ.add_gate(OpType.CCX, [a, b, c])

def unmajority(circ, a, b, c):
    """Puerta Unmajority"""
    circ.add_gate(OpType.CCX, [a, b, c])
    circ.CX(c, a)
    circ.CX(a, b)

def add4(circ, a_idxs, b_idxs, cin, cout):
    """
    Bloque sumador de 4 bits.
    """
    majority(circ, cin, b_idxs[0], a_idxs[0])
    majority(circ, a_idxs[0], b_idxs[1], a_idxs[1])
    majority(circ, a_idxs[1], b_idxs[2], a_idxs[2])
    majority(circ, a_idxs[2], b_idxs[3], a_idxs[3])
    
    circ.CX(a_idxs[3], cout)
    
    unmajority(circ, a_idxs[2], b_idxs[3], a_idxs[3])
    unmajority(circ, a_idxs[1], b_idxs[2], a_idxs[2])
    unmajority(circ, a_idxs[0], b_idxs[1], a_idxs[1])
    unmajority(circ, cin, b_idxs[0], a_idxs[0])

n_qubits = 18
n_bits = 9
circ = Circuit(n_qubits, n_bits)

q_a = list(range(2, 10))
q_b = list(range(10, 18))
q_carry = list(range(0, 2))

for i in range(16):
    circ.X(i+2)

add4(circ, q_a[0:4], q_b[0:4], q_carry[0], q_carry[1])

add4(circ, q_a[4:8], q_b[4:8], q_carry[1], q_carry[0])

circ.add_c_register("bits_resultado", 9)

for i in range(8):
    circ.Measure(10 + i, i) 

circ.Measure(0, 8)

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

total_gates = num_1q + num_2q + num_3q

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
