import re
import os

def translate_qasm_to_tket(input_file, output_file):
    print(f"Generando script TKET (Índices numéricos) desde {input_file}...")
    
    gate_map = {
        'h': 'H', 'x': 'X', 'y': 'Y', 'z': 'Z',
        's': 'S', 't': 'T', 
        'cx': 'CX', 'ccx': 'CCX', 'cz': 'CZ',
        'rx': 'Rx', 'ry': 'Ry', 'rz': 'Rz',
        'u1': 'U1', 'u2': 'U2', 'u3': 'U3',
    }

    rotation_gates = {'Rx', 'Ry', 'Rz', 'U1', 'U2', 'U3'}

    line_count = 0
    circuit_initialized = False

    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        # Cabecera
        outfile.write("from pytket import Circuit\n")
        outfile.write("from numpy import pi\n\n")
        
        for line in infile:
            line_count += 1
            original_line = line.strip()
            
            if not original_line or original_line.startswith('//') or original_line.startswith('OPENQASM') or original_line.startswith('include'):
                continue
            
            clean_line = original_line.replace(';', '')

            # --- DETECTAR TAMAÑO Y CREAR CIRCUITO ---
            if clean_line.startswith('qreg'):
                match = re.search(r'\[(\d+)\]', clean_line)
                if match and not circuit_initialized:
                    size = match.group(1)
                    outfile.write(f"# Inicialización simple con {size} qubits\n")
                    outfile.write(f"circuit = Circuit({size})\n\n")
                    circuit_initialized = True
                continue
            
            # Ignoramos creg porque usaremos measure_all al final
            if clean_line.startswith('creg'):
                continue

            # Ignoramos medidas explícitas para no duplicar (ya que usaremos measure_all)
            if clean_line.startswith('measure'):
                continue

            # --- TRADUCCIÓN DE PUERTAS ---
            if ' ' in clean_line:
                # Barrier
                if clean_line.startswith('barrier'):
                    indices = re.findall(r'\[(\d+)\]', clean_line)
                    indices_str = ", ".join(indices)
                    outfile.write(f"circuit.add_barrier([{indices_str}])\n")
                    continue

                # Separar puerta y argumentos
                gate_part, args_part = clean_line.split(' ', 1)
                gate_name = gate_part.strip()
                
                # --- LIMPIEZA DE ARGUMENTOS ---
                args_clean = re.sub(r'\w+\[(\d+)\]', r'\1', args_part)
                
                # --- EXPANSIÓN DAGGERS ---
                if gate_name == 'sdg':
                    outfile.write(f"circuit.S({args_clean})\ncircuit.S({args_clean})\ncircuit.S({args_clean})\n")
                    continue
                if gate_name == 'tdg':
                    outfile.write(f"circuit.S({args_clean})\ncircuit.S({args_clean})\ncircuit.S({args_clean})\ncircuit.T({args_clean})\n")
                    continue

                # --- PUERTAS NORMALES ---
                params_str = ""
                if '(' in gate_name:
                    gate_name, params_str = gate_name.split('(', 1)
                    params_str = params_str.replace(')', '')
                
                tket_gate = gate_map.get(gate_name, gate_name.capitalize())
                
                if params_str:
                    if tket_gate in rotation_gates:
                        p_list = params_str.split(',')
                        new_params = ", ".join([f"({p})/pi" for p in p_list])
                        outfile.write(f"circuit.{tket_gate}({new_params}, {args_clean})\n")
                    else:
                        outfile.write(f"circuit.{tket_gate}({params_str}, {args_clean})\n")
                else:
                    outfile.write(f"circuit.{tket_gate}({args_clean})\n")

        # --- MEDICIÓN FINAL ---
        outfile.write("\n# Medición automática de todos los qubits\n")
        outfile.write("circuit.measure_all()\n")

    print(f"¡Terminado! Script generado en {output_file}")

def translate_qasm_to_cirq(input_file, output_file):
    print(f"Generando script Cirq desde {input_file}...")
    
    gate_map = {
        'h': 'H', 'x': 'X', 'y': 'Y', 'z': 'Z',
        's': 'S', 't': 'T', 
        'cx': 'CNOT', 'cz': 'CZ',
        'ccx': 'CCNOT'
    }

    rotation_gates = {'rx', 'ry', 'rz'}
    line_count = 0
    
    # Variable para guardar el tamaño del registro principal
    main_reg_size = 0
    main_reg_name = 'q'

    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        # Cabecera
        outfile.write("import cirq\n")
        outfile.write("from numpy import pi\n")
        outfile.write("from cirq.circuits.qasm_output import QasmUGate\n\n")
        
        outfile.write("# --- INICIO CIRCUITO ---\n")
        outfile.write("circuit = cirq.Circuit()\n\n")

        for line in infile:
            line_count += 1
            original_line = line.strip()
            
            if not original_line or original_line.startswith('//') or original_line.startswith('OPENQASM') or original_line.startswith('include'):
                continue
            
            clean_line = original_line.replace(';', '')

            # --- REGISTROS ---
            if clean_line.startswith('qreg'):
                match = re.search(r'qreg\s+(\w+)\[(\d+)\]', clean_line)
                if match:
                    name, size = match.groups()
                    main_reg_name = name
                    main_reg_size = int(size)
                    outfile.write(f"# Registro {name}\n")
                    outfile.write(f"{name} = [cirq.NamedQubit(str(i)) for i in range({size})]\n\n")
                continue

            if clean_line.startswith('creg') or clean_line.startswith('measure'):
                continue

            # --- PUERTAS ---
            if ' ' in clean_line:
                gate_part, args_part = clean_line.split(' ', 1)
                gate_name = gate_part.strip()
                args = args_part.strip() # ej: q[0]

                # --- EXPANSIÓN DE DAGGERS ---
                if gate_name == 'sdg':
                    outfile.write(f"circuit.append([cirq.S({args}), cirq.S({args}), cirq.S({args})])\n")
                    continue
                if gate_name == 'tdg':
                    outfile.write(f"circuit.append([cirq.S({args}), cirq.S({args}), cirq.S({args}), cirq.T({args})])\n")
                    continue

                # --- PARÁMETROS ---
                params_str = ""
                if '(' in gate_name:
                    gate_name, params_str = gate_name.split('(', 1)
                    params_str = params_str.replace(')', '')
                
                # --- U GATES (Usando QasmUGate nativa) ---                
                if gate_name == 'u3': 
                    theta, phi, lam = params_str.split(',')
                    outfile.write(f"circuit.append(QasmUGate(theta=({theta})/pi, phi=({phi})/pi, lmda=({lam})/pi).on({args}))\n")
                    continue

                if gate_name == 'u2':
                    phi, lam = params_str.split(',')
                    outfile.write(f"circuit.append(QasmUGate(theta=0.5, phi=({phi})/pi, lmda=({lam})/pi).on({args}))\n")
                    continue
                
                if gate_name == 'u1':
                    outfile.write(f"circuit.append(cirq.rz({params_str})({args}))\n")
                    continue

                # --- PUERTAS ESTÁNDAR ---
                cirq_gate = gate_map.get(gate_name)
                
                if cirq_gate:
                    outfile.write(f"circuit.append(cirq.{cirq_gate}({args}))\n")
                elif gate_name in rotation_gates:
                    outfile.write(f"circuit.append(cirq.{gate_name}({params_str})({args}))\n")

        if main_reg_size > 0:
            outfile.write("\n# Medición explícita de cada qubit\n")
            for i in range(main_reg_size):
                outfile.write(f'circuit.append(cirq.measure({main_reg_name}[{i}], key="m{i}"))\n')

    print(f"¡Hecho! Script Cirq generado en {output_file}")

def translate_qasm_to_pennylane(input_file, output_file):
    print(f"Generando script PennyLane (Sintaxis corregida) desde {input_file}...")
    
    gate_map = {
        'h': 'Hadamard', 
        'x': 'PauliX', 'y': 'PauliY', 'z': 'PauliZ',
        's': 'S', 't': 'T',
        'cx': 'CNOT', 'ccx': 'Toffoli', 'cz': 'CZ',
        'rx': 'RX', 'ry': 'RY', 'rz': 'RZ',
        'u1': 'PhaseShift',
        'u2': 'U2', 'u3': 'U3'
    }

    line_count = 0
    n_qubits = 0
    circuit_lines = []

    with open(input_file, 'r') as infile:
        for line in infile:
            line_count += 1
            original_line = line.strip()
            
            if not original_line or original_line.startswith('//') or original_line.startswith('OPENQASM') or original_line.startswith('include'):
                continue
            
            clean_line = original_line.replace(';', '')

            # --- DETECCIÓN DE QUBITS ---
            if clean_line.startswith('qreg'):
                match = re.search(r'qreg\s+(\w+)\[(\d+)\]', clean_line)
                if match:
                    _, size = match.groups()
                    n_qubits = int(size)
                continue

            if clean_line.startswith('creg') or clean_line.startswith('measure'):
                continue

            # --- TRADUCCIÓN PUERTAS ---
            if ' ' in clean_line:
                # Barrier
                if clean_line.startswith('barrier'):
                    if clean_line.strip() == 'barrier':
                         circuit_lines.append(f"    qml.Barrier(wires=range({n_qubits}))")
                    else:
                        indices = re.findall(r'\[(\d+)\]', clean_line)
                        indices_str = ",".join(indices)
                        circuit_lines.append(f"    qml.Barrier(wires=[{indices_str}])")
                    continue

                gate_part, args_part = clean_line.split(' ', 1)
                gate_name = gate_part.strip()
                
                args_clean = re.sub(r'\w+\[(\d+)\]', r'\1', args_part)
                wire_list = [int(x) for x in re.findall(r'\d+', args_clean)]
                
                if len(wire_list) == 1:
                    wires_str = f"wires={wire_list[0]}"
                else:
                    wires_str = f"wires={wire_list}"

                # Daggers
                if gate_name == 'sdg':
                    circuit_lines.append(f"    qml.S({wires_str})")
                    circuit_lines.append(f"    qml.S({wires_str})")
                    circuit_lines.append(f"    qml.S({wires_str})")
                    continue
                if gate_name == 'tdg':
                    circuit_lines.append(f"    qml.S({wires_str})")
                    circuit_lines.append(f"    qml.S({wires_str})")
                    circuit_lines.append(f"    qml.S({wires_str})")
                    circuit_lines.append(f"    qml.T({wires_str})")
                    continue

                # Params
                params_str = ""
                if '(' in gate_name:
                    gate_name, params_str = gate_name.split('(', 1)
                    params_str = params_str.replace(')', '')
                
                pl_gate = gate_map.get(gate_name)
                
                if pl_gate:
                    if params_str:
                        circuit_lines.append(f"    qml.{pl_gate}({params_str}, {wires_str})")
                    else:
                        circuit_lines.append(f"    qml.{pl_gate}({wires_str})")

    # --- ESCRITURA FINAL ---
    with open(output_file, 'w') as outfile:
        outfile.write("import pennylane as qml\n")
        outfile.write("from numpy import pi\n\n")
        
        outfile.write(f"# Configuración del dispositivo\n")
        outfile.write(f'dev = qml.device("default.qubit", wires={n_qubits})\n\n')
        
        outfile.write("# Definimos los shots en el decorador\n")
        outfile.write("@qml.qnode(dev, shots=1024)\n")
        outfile.write("def circuit():\n")
        
        for line in circuit_lines:
            outfile.write(line + "\n")
            
        outfile.write("\n    return qml.sample(wires=range({}))\n".format(n_qubits))
        
        outfile.write("\n# Ejecución de prueba (opcional)\n")
        outfile.write("# print(circuit())\n")

    print(f"Archivo guardado en {output_file}")

def translate_qasm_to_myqlm(input_file, output_file):
    print(f"Generando script myQLM desde {input_file}...")
    
    gate_map = {
        'h': 'H', 'x': 'X', 'y': 'Y', 'z': 'Z',
        's': 'S', 't': 'T', 
        'cx': 'CNOT', 'ccx': 'CCNOT', 'cz': 'CSIGN', 
        'rx': 'RX', 'ry': 'RY', 'rz': 'RZ'
    }

    rotation_gates = {'RX', 'RY', 'RZ', 'PH'}
    
    q_reg_name = 'q' 

    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        # Cabecera
        outfile.write("import numpy as np\n")
        outfile.write("from qat.lang.AQASM import Program, AbstractGate, H, X, Y, Z, S, T, CNOT, CCNOT, CSIGN, SWAP, RX, RY, RZ, PH\n\n")
        
        # --- DEFINICIÓN DE LA BARRERA ---
        outfile.write("# Definición de BARRIER\n")
        outfile.write("BARRIER = AbstractGate(\"BARRIER\", [], arity=1)\n")
        outfile.write("BARRIER.set_matrix_generator(lambda: np.eye(2))\n\n")
        
        outfile.write("# --- INICIO DEL PROGRAMA ---\n")
        outfile.write("prog = Program()\n\n")

        for line in infile:
            original_line = line.strip()
            
            # Ignorar comentarios y cabeceras
            if not original_line or original_line.startswith('//') or original_line.startswith('OPENQASM') or original_line.startswith('include'):
                continue
            
            clean_line = original_line.replace(';', '')

            # --- REGISTROS ---
            if clean_line.startswith('qreg'):
                match = re.search(r'qreg\s+(\w+)\[(\d+)\]', clean_line)
                if match:
                    name, size = match.groups()
                    q_reg_name = name
                    outfile.write(f"# Registro Cuántico\n")
                    outfile.write(f"{name} = prog.qalloc({size})\n\n")
                continue

            if clean_line.startswith('creg'):
                continue

            # --- PUERTAS ---
            if ' ' in clean_line:
                # Barrier
                if clean_line.startswith('barrier'):
                    indices = re.findall(r'\[(\d+)\]', clean_line)
                    if indices:
                        for idx in indices:
                            outfile.write(f"prog.apply(BARRIER(), {q_reg_name}[{idx}])\n")
                    continue

                gate_part, args_part = clean_line.split(' ', 1)
                gate_name = gate_part.strip()
                
                args = re.sub(r'(\w+)\[(\d+)\]', rf'{q_reg_name}[\2]', args_part)
                
                
                # --- EXPANSIÓN DE DAGGERS ---
                if gate_name == 'sdg':
                    outfile.write(f"prog.apply(S, {args})\nprog.apply(S, {args})\nprog.apply(S, {args})\n")
                    continue
                if gate_name == 'tdg':
                    outfile.write(f"prog.apply(S, {args})\nprog.apply(S, {args})\nprog.apply(S, {args})\nprog.apply(T, {args})\n")
                    continue

                # --- PARÁMETROS ---
                params_str = ""
                if '(' in gate_name:
                    gate_name, params_str = gate_name.split('(', 1)
                    params_str = params_str.replace(')', '')
                
                # --- TRADUCCIÓN DE U GATES (Descomposición Euler Z-Y-Z) ---
                
                # U3(theta, phi, lam) -> RZ(lam) RY(theta) RZ(phi)
                if gate_name == 'u3':
                    theta, phi, lam = params_str.split(',')
                    outfile.write(f"# U3 descompuesta\n")
                    outfile.write(f"prog.apply(RZ({lam}), {args})\n")
                    outfile.write(f"prog.apply(RY({theta}), {args})\n")
                    outfile.write(f"prog.apply(RZ({phi}), {args})\n")
                    continue

                # U2(phi, lam) -> RZ(lam) RY(pi/2) RZ(phi)
                if gate_name == 'u2':
                    phi, lam = params_str.split(',')
                    outfile.write(f"# U2 descompuesta\n")
                    outfile.write(f"prog.apply(RZ({lam}), {args})\n")
                    outfile.write(f"prog.apply(RY(np.pi/2), {args})\n")
                    outfile.write(f"prog.apply(RZ({phi}), {args})\n")
                    continue
                
                # U1(lam) -> PH(lam) o RZ(lam)
                if gate_name == 'u1':
                    outfile.write(f"prog.apply(PH({params_str}), {args})\n")
                    continue

                # --- PUERTAS ESTÁNDAR ---
                qlm_gate = gate_map.get(gate_name)
                
                if qlm_gate:
                    if params_str:
                        outfile.write(f"prog.apply({qlm_gate}({params_str}), {args})\n")
                    else:
                        outfile.write(f"prog.apply({qlm_gate}, {args})\n")

        # --- MEDICIÓN Y GENERACIÓN ---
        outfile.write("\n# --- Generación del Circuito ---\n")
        outfile.write("circuit = prog.to_circ()\n")
        outfile.write("# Para ejecutar: result = qpu.submit(circuit.to_job())\n")

    print(f"Script myQLM generado en {output_file}")

def translate_qasm_to_qiskit(input_file, output_file):
    print(f"Iniciando traducción de {input_file}...")
    
    gate_map = {
        'h': 'h', 'x': 'x', 'y': 'y', 'z': 'z',
        'cx': 'cx', 'ccx': 'ccx', 'cz': 'cz',
        'rx': 'rx', 'ry': 'ry', 'rz': 'rz',
        'u1': 'p', 'u2': 'u2', 'u3': 'u',
        's': 's', 'sdg': 'sdg', 't': 't', 
        'tdg': 'tdg', 'barrier': 'barrier',
        'measure': 'measure' # Tratamos measure como una puerta más
    }

    line_count = 0
    
    # --- BANDERA DE CONTROL ---
    circuit_created = False
    
    q_regs_found = []
    c_regs_found = []

    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        # Cabecera
        outfile.write("from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister\n")
        outfile.write("from numpy import pi\n\n")
        outfile.write("# --- CIRCUITO GENERADO ---\n\n")

        outfile.write("\n# Parche de compatibilidad para u2\n")
        outfile.write("def u2_patch(self, phi, lam, qubit):\n")
        outfile.write("    return self.u(pi/2, phi, lam, qubit)\n")
        outfile.write("QuantumCircuit.u2 = u2_patch\n\n")

        for line in infile:
            line_count += 1
            original_line = line.strip()
            
            if not original_line or original_line.startswith('//') or original_line.startswith('OPENQASM') or original_line.startswith('include'):
                continue

            clean_line = original_line.replace(';', '')

            if clean_line.startswith('qreg'):
                match = re.search(r'qreg\s+(\w+)\[(\d+)\]', clean_line)
                if match:
                    name, size = match.groups()
                    outfile.write(f"{name} = QuantumRegister({size}, '{name}')\n")
                    q_regs_found.append(name)
                continue # Saltamos a la siguiente línea

            if clean_line.startswith('creg'):
                match = re.search(r'creg\s+(\w+)\[(\d+)\]', clean_line)
                if match:
                    name, size = match.groups()
                    outfile.write(f"{name} = ClassicalRegister({size}, '{name}')\n")
                    c_regs_found.append(name)
                continue

            if not circuit_created:
                regs_str = ", ".join(q_regs_found + c_regs_found)
                outfile.write(f"\ncircuit = QuantumCircuit({regs_str})\n\n")
                circuit_created = True

            if clean_line.startswith('measure'):
                parts = clean_line.split('->')
                if len(parts) == 2:
                    src = parts[0].replace('measure', '').strip()
                    dst = parts[1].strip()
                    outfile.write(f"circuit.measure({src}, {dst})\n")
                continue

            if ' ' in clean_line:
                gate_part, args_part = clean_line.split(' ', 1)
                gate_name = gate_part.strip()
                
                params = ""
                if '(' in gate_name:
                    gate_name, params = gate_name.split('(', 1)
                    params = params.replace(')', '')
                
                qiskit_gate = gate_map.get(gate_name, gate_name)
                
                args = args_part.strip()
                
                if params:
                    outfile.write(f"circuit.{qiskit_gate}({params}, {args})\n")
                else:
                    outfile.write(f"circuit.{qiskit_gate}({args})\n")

    print(f"¡Hecho! {line_count} líneas procesadas.")

def translator(sdk,file):
    """
    Translate from QASM to the sdk argument sent from the .txt file sent
    """
    nombre, extension = os.path.splitext(file)

    if sdk == 'qiskit':
        newfile = f"{nombre}_qiskit{extension}"
        translate_qasm_to_qiskit(file,newfile)
    elif sdk == 'myqlm':
        newfile = f"{nombre}_myqlm{extension}"
        translate_qasm_to_myqlm(file,newfile)
    elif sdk == 'cirq':
        newfile = f"{nombre}_cirq{extension}"
        translate_qasm_to_cirq(file,newfile)
    elif sdk == 'tket':
        newfile = f"{nombre}_tket{extension}"
        translate_qasm_to_tket(file,newfile)
    elif sdk == 'pennylane':
        newfile = f"{nombre}_pennylane{extension}"
        translate_qasm_to_pennylane(file,newfile)
    else:
        print("Aergument not valid")

translator('qiskit','vqe_uccsd_n28.txt')
