FROM python:3.11

WORKDIR /app

RUN pip install qiskit
RUN pip install qiskit_ibm_runtime
RUN pip install qiskit[visualization]
RUN pip install qiskit-aer

COPY adder_n4.py /app/

CMD ["python", "adder_n4.py"]