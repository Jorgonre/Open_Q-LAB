FROM python:3.11

WORKDIR /app

RUN pip install pennylane
RUN python -m pip install jax~=0.6.0

COPY circuito_prueba.py /app/

CMD ["python", "circuito_prueba.py"]