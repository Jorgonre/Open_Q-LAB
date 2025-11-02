from qat.interop.openqasm import OqasmParser
from qat.qpus import Linalg
from qat.core import Job

qasm_code = """
OPENQASM 2.0;
include "qelib1.inc";

qreg q[4];
creg c[4];
x q[0];
x q[1];
h q[3];
cx q[2],q[3];
t q[0];
t q[1];
t q[2];
tdg q[3];
cx q[0],q[1];
cx q[2],q[3];
cx q[3],q[0];
cx q[1],q[2];
cx q[0],q[1];
cx q[2],q[3];
tdg q[0];
tdg q[1];
tdg q[2];
t q[3];
cx q[0],q[1];
cx q[2],q[3];
s q[3];
cx q[3],q[0];
h q[3];
measure q[0] -> c[0];
measure q[1] -> c[1];
measure q[2] -> c[2];
measure q[3] -> c[3];
"""

parser = OqasmParser()
circuit = parser.compile(qasm_code)

qpu = Linalg()
job = Job(circuit=circuit, nbshots=1024)
result = qpu.submit(job)

counts = {}
for sample in result:
    bitstring = "".join(str(b) for b in sample.state)
    counts[bitstring] = int(sample.probability * result.nbshots)

print(counts)
print(circuit)