from qat.lang.AQASM import Program, H, CNOT, X, T, S
from qat.qpus import PyLinalg
from qat.core import Job

prog = Program()
qbits = prog.qalloc(4)

prog.apply(X, qbits[0])
prog.apply(X, qbits[1])
prog.apply(H, qbits[3])
prog.apply(CNOT, qbits[2], qbits[3])
prog.apply(T, qbits[0])
prog.apply(T, qbits[1])
prog.apply(T, qbits[2])
prog.apply(S, qbits[3]) #Tdagger
prog.apply(S, qbits[3]) #Tdagger
prog.apply(S, qbits[3]) #Tdagger
prog.apply(T, qbits[3]) #Tdagger
prog.apply(CNOT, qbits[0], qbits[1])
prog.apply(CNOT, qbits[2], qbits[3])
prog.apply(CNOT, qbits[3], qbits[0])
prog.apply(CNOT, qbits[1], qbits[2])
prog.apply(CNOT, qbits[0], qbits[1])
prog.apply(CNOT, qbits[2], qbits[3])
prog.apply(S, qbits[0]) #Tdagger
prog.apply(S, qbits[0]) #Tdagger
prog.apply(S, qbits[0]) #Tdagger
prog.apply(T, qbits[0]) #Tdagger
prog.apply(S, qbits[1]) #Tdagger
prog.apply(S, qbits[1]) #Tdagger
prog.apply(S, qbits[1]) #Tdagger
prog.apply(T, qbits[1]) #Tdagger
prog.apply(S, qbits[2]) #Tdagger
prog.apply(S, qbits[2]) #Tdagger
prog.apply(S, qbits[2]) #Tdagger
prog.apply(T, qbits[2]) #Tdagger
prog.apply(T, qbits[3])
prog.apply(CNOT, qbits[0], qbits[1])
prog.apply(CNOT, qbits[2], qbits[3])
prog.apply(S, qbits[3])
prog.apply(CNOT, qbits[3], qbits[0])
prog.apply(H, qbits[3])

for i in range(4):
    prog.measure(qbits[i])

circuit = prog.to_circ()
qpu = PyLinalg()
job = Job(circuit=circuit, nbshots=1024)
result = qpu.submit(job)

print(result[0].state)

print(circuit)