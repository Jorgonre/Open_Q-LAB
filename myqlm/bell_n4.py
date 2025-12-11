from qat.lang import Program, H, CNOT, X, T, S, AbstractGate, PH, qrout, RZ, RX, RY
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

prog = Program()
qbits = prog.qalloc(4)

@qrout
def bell():
    """
    Esta función devuelve automáticamente una QRoutine
    con la lógica que has definido.
    """
    
    # Nota: Dentro de @qrout se usa: PUERTA(params)(qubits)
    H(0)
    H(1)
    H(3)
    
    CNOT(0,2)
    # 1. Aplicamos la Lambda (3º parámetro de Qiskit) PRIMERO
    RZ(np.pi * 0.75)(3)
    # 2. Aplicamos la Theta (1º parámetro de Qiskit) DESPUÉS
    RY(np.pi * 0.5)(3)
    # 3. Aplicaríamos la Phi (2º parámetro de Qiskit) AL FINAL
    # RZ(0), qbits[3]

    RX(np.pi*(-0.25))(0)
    RZ(np.pi * 0.75)(1) #Equivalencia de la U
    RY(np.pi * 0.5)(1) #Equivalencia de la U
    RZ(0)(1) #Equivalencia de la U
    RY(np.pi*(-0.5))(2)
    RX(np.pi*(0.5))(3)

    RY(np.pi*(-0.5))(0)
    RX(np.pi*(0.5))(1)
    RZ(np.pi * 0.25)(2) #Equivalencia de la U
    RY(np.pi * 0.5)(2) #Equivalencia de la U
    RZ(0)(2) #Equivalencia de la U

    RZ(np.pi * 0.25)(0) #Equivalencia de la U
    RY(np.pi * 0.5)(0) #Equivalencia de la U
    RZ(0)(0) #Equivalencia de la U
    CNOT(3,2)

    CNOT(1,0)
    RY(np.pi * 0.5)(2)
    RX(np.pi * 0.25)(3)

    RY(np.pi * 0.5)(0)
    RX(np.pi * 0.25)(1)
    CNOT(2,3)

    CNOT(0,1)
    RX(np.pi * (-0.5))(2)

    RX(np.pi * (-0.5))(0)
    RZ(np.pi * (0.5))(2)

    RZ(np.pi * (0.5))(0)
    CNOT(3,2)

    CNOT(1,0)

    RZ(np.pi * 1)(2) #Equivalencia de la U
    RY(np.pi * 0.5)(2) #Equivalencia de la U
    RZ(np.pi * 1)(2) #Equivalencia de la U
    RZ(np.pi * 1)(3) #Equivalencia de la U
    RY(np.pi * 0.5)(3) #Equivalencia de la U
    RZ(np.pi * 0.5)(3) #Equivalencia de la U

    RZ(np.pi * 1)(0) #Equivalencia de la U
    RY(np.pi * 0.5)(0) #Equivalencia de la U
    RZ(np.pi * 1)(0) #Equivalencia de la U
    RZ(np.pi * 1)(1) #Equivalencia de la U
    RY(np.pi * 0.5)(1) #Equivalencia de la U
    RZ(np.pi * 0.5)(1) #Equivalencia de la U
    RY(np.pi * 0.5)(2)

    RY(np.pi * 0.5)(0)


build_time = time.time() - start_build

#for i in range(4):
#    prog.measure(qbits[i])

start_transpile = time.time()

job = bell.to_job(nbshots=1024)
result = get_default_qpu().submit(job)

cpu_usage = process.cpu_percent(None)
ram_usage_mb = process.memory_info().rss / (1024 * 1024)

transpile_time = time.time() - start_transpile
total_time = time.time() - start_time

num_qubits = bell.nbqbits

# Calcula depth estilo Qiskit
last_layer_for_qubit = {}
depth = 0

for op in bell.ops:
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

gate_counts = bell.ops
num_1q = sum(1 for g in gate_counts if len(g.qbits) == 1) - 4  #Resta por measure gates
num_2q = sum(1 for g in gate_counts if len(g.qbits) == 2)
total_gates = num_1q + num_2q

for sample in result:
    print(sample.state, sample.probability)

print(bell)

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