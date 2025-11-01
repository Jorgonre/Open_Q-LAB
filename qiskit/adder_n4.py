from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
from numpy import pi
 
qreg_q = QuantumRegister(4, 'q')
creg_c = ClassicalRegister(4, 'c')
circuit = QuantumCircuit(qreg_q, creg_c)
 
circuit.h(qreg_q[3])
circuit.x(qreg_q[1])
circuit.x(qreg_q[0])
circuit.t(qreg_q[1])
circuit.t(qreg_q[0])
circuit.cx(qreg_q[2], qreg_q[3])
circuit.cx(qreg_q[0], qreg_q[1])
circuit.t(qreg_q[2])
circuit.tdg(qreg_q[3])
circuit.cx(qreg_q[2], qreg_q[3])
circuit.cx(qreg_q[3], qreg_q[0])
circuit.cx(qreg_q[1], qreg_q[2])
circuit.cx(qreg_q[0], qreg_q[1])
circuit.cx(qreg_q[2], qreg_q[3])
circuit.tdg(qreg_q[1])
circuit.tdg(qreg_q[2])
circuit.t(qreg_q[3])
circuit.s(qreg_q[0])
circuit.s(qreg_q[0])
circuit.s(qreg_q[0])
circuit.cx(qreg_q[2], qreg_q[3])
circuit.t(qreg_q[0])
circuit.cx(qreg_q[0], qreg_q[1])
circuit.measure(qreg_q[2], creg_c[2])
circuit.s(qreg_q[3])
circuit.cx(qreg_q[3], qreg_q[0])
circuit.h(qreg_q[3])
circuit.measure(qreg_q[0], creg_c[0])
circuit.measure(qreg_q[1], creg_c[1])
circuit.measure(qreg_q[3], creg_c[3])

sim = AerSimulator()
 
job = sim.run(circuit, shots=1024)  
result = job.result()
 
counts = result.get_counts()
print(counts)
 
plot_histogram(counts)