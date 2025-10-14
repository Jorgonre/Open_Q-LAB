FROM python:3.11

WORKDIR /app

RUN pip install cirq
RUN python -m pip install cirq-core[contrib]

COPY circuito_prueba.py /app/

CMD ["python", "circuito_prueba.py"]