FROM python:3.11

WORKDIR /app

COPY ../common /app/common

RUN pip install myqlm

COPY circuito_prueba.py /app/

CMD ["python", "circuito_prueba.py"]