from pytket import Circuit

circ = Circuit(3)
q = circ.add_q_register("q", 4)

circ.X(q[0])
circ.X(q[1])
circ.H(q[3])

circ.CX(q[2],q[3])

circ.T(q[0])
circ.T(q[1])
circ.T(q[2])
circ.S(q[3]) #Tdagger
circ.S(q[3]) #Tdagger
circ.S(q[3]) #Tdagger
circ.T(q[3]) #Tdagger

circ.CX(q[0],q[1])
circ.CX(q[2],q[3])

circ.CX(q[3],q[0])

circ.CX(q[1],q[2])

circ.CX(q[0],q[1])
circ.CX(q[2],q[3])

circ.S(q[0]) #Tdagger
circ.S(q[0]) #Tdagger
circ.S(q[0]) #Tdagger
circ.T(q[0]) #Tdagger
circ.S(q[1]) #Tdagger
circ.S(q[1]) #Tdagger
circ.S(q[1]) #Tdagger
circ.T(q[1]) #Tdagger
circ.S(q[2]) #Tdagger
circ.S(q[2]) #Tdagger
circ.S(q[2]) #Tdagger
circ.T(q[2]) #Tdagger
circ.T(q[3])

circ.CX(q[0],q[1])
circ.CX(q[2],q[3])

circ.S(q[3])

circ.CX(q[3],q[0])

circ.H(q[3])