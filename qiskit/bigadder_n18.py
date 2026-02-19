from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
from numpy import pi
import time
from qiskit import transpile
import psutil
import os

process = psutil.Process(os.getpid())

process.cpu_percent(interval=None)  # Establece línea base

start_time = time.time()
# Medir tiempo de construcción
start_build = time.time()

def majority(qc, a, b, c):
    """Puerta Majority: calcula el acarreo (carry)"""
    qc.cx(c, b)
    qc.cx(c, a)
    qc.ccx(a, b, c)

def unmaj(qc, a, b, c):
    """Puerta Unmajority: deshace el cálculo (uncomputation)"""
    qc.ccx(a, b, c)
    qc.cx(c, a)
    qc.cx(a, b)

def add4(qc, a, b, cin, cout):
    """
    Suma dos registros de 4 qubits (a y b).
    El resultado se guarda en b.
    cin: qubit de acarreo de entrada
    cout: qubit de acarreo de salida
    """
    # Majority steps (calculando acarreos hacia adelante)
    majority(qc, cin, b[0], a[0])
    majority(qc, a[0], b[1], a[1])
    majority(qc, a[1], b[2], a[2])
    majority(qc, a[2], b[3], a[3])
    
    # Escribir el resultado en el acarreo de salida
    qc.cx(a[3], cout)
    
    # Unmajority steps (deshaciendo cambios intermedios y calculando suma)
    unmaj(qc, a[2], b[3], a[3])
    unmaj(qc, a[1], b[2], a[2])
    unmaj(qc, a[0], b[1], a[1])
    unmaj(qc, cin, b[0], a[0])

qreg_carry = QuantumRegister(2, 'carry')
qreg_a = QuantumRegister(8, 'a')
qreg_b = QuantumRegister(8, 'b')
creg_ans = ClassicalRegister(8, 'ans')
creg_carryout = ClassicalRegister(1, 'carryout')

circuit = QuantumCircuit(qreg_carry, qreg_a, qreg_b, creg_ans, creg_carryout)
 
circuit.x(qreg_a)

circuit.x(qreg_b) #Todas las b a 1
#circuit.x(qreg_b[6]) #Invierte b[6]

add4(circuit, qreg_a[0:4], qreg_b[0:4], qreg_carry[0], qreg_carry[1])

add4(circuit, qreg_a[4:8], qreg_b[4:8], qreg_carry[1], qreg_carry[0])

circuit.measure(qreg_b, creg_ans)

circuit.measure(qreg_carry[0], creg_carryout)

build_time = time.time() - start_build

start_transpile = time.time()

sim = AerSimulator()
#transpiled = transpile(circuit, backend=sim)
transpiled = transpile(circuit, backend=sim, optimization_level = 0)

job = sim.run(transpiled, shots=1024)  
result = job.result()

transpile_time = time.time() - start_transpile
total_time = time.time() - start_time

# Medir uso de recursos
cpu_usage = process.cpu_percent(None)
ram_usage_mb = process.memory_info().rss / (1024 * 1024)

counts = result.get_counts()

print(counts)
 
plot_histogram(counts)

# Inicializamos contadores
num_1q = 0
num_2q = 0
num_3q = 0

# Iteramos sobre cada instrucción del circuito 
for instruction in circuit.data:
    operation = instruction.operation
    
    # Ignoramos lo que no sea puerta lógica
    if operation.name in ['measure']:
        continue
    
    # Clasificamos según el número de qubits que toca la puerta
    if operation.num_qubits == 1:
        num_1q += 1
    elif operation.num_qubits == 2:
        num_2q += 1
    elif operation.num_qubits == 3:
        num_3q += 1

total_gates = num_1q + num_2q + num_3q
num_qubits = circuit.num_qubits
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