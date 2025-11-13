from pytket import Circuit

ghz_circ = Circuit(3)
ghz_circ.H(0)
ghz_circ.CX(0, 1)
ghz_circ.CX(1, 2)
ghz_circ.add_barrier(ghz_circ.qubits)
ghz_circ.measure_all()