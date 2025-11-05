import cirq
import numpy as np
from collections import Counter

# Crear 4 qubits q0, q1, q2, q3
q = cirq.LineQubit.range(4)

circuit = cirq.Circuit()

#Inicialización

circuit.append(cirq.X(q[0]))
circuit.append(cirq.X(q[1]))
circuit.append(cirq.H(q[3]))

circuit.append(cirq.CNOT(q[2],q[3]))

circuit.append(cirq.T(q[0]))
circuit.append(cirq.T(q[1]))
circuit.append(cirq.T(q[2]))
circuit.append(cirq.S(q[3])) #Tdagger
circuit.append(cirq.S(q[3])) #Tdagger
circuit.append(cirq.S(q[3])) #Tdagger
circuit.append(cirq.T(q[3])) #Tdagger

circuit.append(cirq.CNOT(q[0],q[1]))
circuit.append(cirq.CNOT(q[2],q[3]))

circuit.append(cirq.CNOT(q[3],q[0]))

circuit.append(cirq.CNOT(q[1],q[2]))

circuit.append(cirq.CNOT(q[0],q[1]))
circuit.append(cirq.CNOT(q[2],q[3]))

circuit.append(cirq.S(q[0])) #Tdagger
circuit.append(cirq.S(q[0])) #Tdagger
circuit.append(cirq.S(q[0])) #Tdagger
circuit.append(cirq.T(q[0])) #Tdagger
circuit.append(cirq.S(q[1])) #Tdagger
circuit.append(cirq.S(q[1])) #Tdagger
circuit.append(cirq.S(q[1])) #Tdagger
circuit.append(cirq.T(q[1])) #Tdagger
circuit.append(cirq.S(q[2])) #Tdagger
circuit.append(cirq.S(q[2])) #Tdagger
circuit.append(cirq.S(q[2])) #Tdagger
circuit.append(cirq.T(q[2])) #Tdagger
circuit.append(cirq.T(q[3]))

circuit.append(cirq.CNOT(q[0],q[1]))
circuit.append(cirq.CNOT(q[2],q[3]))

circuit.append(cirq.S(q[3]))

circuit.append(cirq.CNOT(q[3],q[0]))

circuit.append(cirq.H(q[3]))

# Medidas
circuit.append(cirq.measure(q[0], key="m0"))
circuit.append(cirq.measure(q[1], key="m1"))
circuit.append(cirq.measure(q[2], key="m2"))
circuit.append(cirq.measure(q[3], key="m3"))

# Resultados
sim = cirq.Simulator()
result = sim.run(circuit, repetitions=1024)

#print("Resultados:")
#print(result)

for i in range(4):
    data = result.measurements[f"m{i}"].flatten()
    counts = Counter(data)
    total = sum(counts.values())
    p0 = counts.get(0, 0) / total
    p1 = counts.get(1, 0) / total
    print(f"q{i}: {p0:.3f} |0⟩  +  {p1:.3f} |1⟩")

print("\nCircuito traducido:")
print(circuit)