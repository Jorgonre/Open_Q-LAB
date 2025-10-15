import pennylane as qml
from jax import numpy as np
import jax

dev1 = qml.device("lightning.qubit", wires=1)

@qml.qnode(dev1)
def circuit(params):
    qml.RX(params[0], wires=0)
    qml.RY(params[1], wires=0)
    return qml.expval(qml.PauliZ(0))

params = np.array([0.54, 0.12])
print(circuit(params))