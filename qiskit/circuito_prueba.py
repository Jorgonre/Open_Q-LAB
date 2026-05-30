#Librerías a importar
from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp
from qiskit.transpiler import generate_preset_pass_manager
from qiskit_ibm_runtime import EstimatorV2 as Estimator
import matplotlib.pyplot as plt
 
#Inicialización del circuito
qc = QuantumCircuit(2)
 
#Desarrollo del circuito
qc.h(0)
qc.cx(0, 1)
qc.measure_all()

#Ejecución del circuito
sim = AerSimulator()
transpiled = transpile(qc, backend=sim, optimization_level = 0)
job = sim.run(transpiled, shots=1024)  
result = job.result()


qc.draw("mpl")
plt.show()
