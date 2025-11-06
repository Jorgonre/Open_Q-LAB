import pennylane as qml
from jax import numpy as np
import jax
from collections import Counter

dev = qml.device("default.qubit", wires=4, shots=1024)

@qml.qnode(dev)
def circuit():
    qml.PauliX(wires=0)
    qml.PauliX(wires=1)
    qml.Hadamard(wires=3)

    qml.CNOT(wires=[2,3])

    qml.T(wires=0)
    qml.T(wires=1)
    qml.T(wires=2)
    qml.S(wires=3) #Tdagger
    qml.S(wires=3) #Tdagger
    qml.S(wires=3) #Tdagger
    qml.T(wires=3) #Tdagger

    qml.CNOT(wires=[0,1])
    qml.CNOT(wires=[2,3])

    qml.CNOT(wires=[3,0])

    qml.CNOT(wires=[1,2])

    qml.CNOT(wires=[0,1])
    qml.CNOT(wires=[2,3])

    qml.S(wires=0) #Tdagger
    qml.S(wires=0) #Tdagger
    qml.S(wires=0) #Tdagger
    qml.T(wires=0) #Tdagger
    qml.S(wires=1) #Tdagger
    qml.S(wires=1) #Tdagger
    qml.S(wires=1) #Tdagger
    qml.T(wires=1) #Tdagger
    qml.S(wires=2) #Tdagger
    qml.S(wires=2) #Tdagger
    qml.S(wires=2) #Tdagger
    qml.T(wires=2) #Tdagger
    qml.T(wires=3)

    qml.CNOT(wires=[0,1])
    qml.CNOT(wires=[2,3])

    qml.S(wires=3)

    qml.CNOT(wires=[3,0])

    qml.Hadamard(wires=3)

    return qml.sample(wires=range(4))

samples = circuit()
samples = np.array(samples)
if samples.ndim == 1 and num_wires > 1:
    samples = samples.reshape((1024, 4))

for wire in range(4):
    col = samples[:, wire]
    counts = Counter(col.tolist())
    total = sum(counts.values())
    p0 = counts.get(0, 0) / total
    p1 = counts.get(1, 0) / total
    print(f"q{wire}: {p0:.3f} |0>  +  {p1:.3f} |1>")

print("\nCircuito (texto):")
drawer = qml.draw(circuit)
print(drawer())