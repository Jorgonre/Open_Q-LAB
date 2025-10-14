FROM python:3.11

WORKDIR /app

RUN pip install qiskit
RUN pip install qiskit_ibm_runtime
RUN pip install qiskit[visualization]

COPY circuito_prueba.py /app/

CMD ["python", "circuito_prueba.py"]