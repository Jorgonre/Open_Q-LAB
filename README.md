# Quantum Computing Frameworks Benchmark

This project performs a performance comparison benchmark among leading quantum computing frameworks (**Qiskit, Cirq, PennyLane, MyQLM, and Tket**).

The goal is to measure and visualize key metrics such as **Execution Time**, **RAM Usage**, and **CPU Usage** by executing identical quantum circuits across different environments using a unified Docker architecture.

## Architecture

Instead of installing dependencies individually for each framework container, this project uses a **Base Image strategy** to ensure consistency and reduce build times.

1.  **`Dockerfile.base`**: A single Docker image that installs Python 3.11 and **all** the required quantum libraries (Qiskit, Cirq, PennyLane, MyQLM, Tket, etc.) once.
2.  **Service Containers**: The containers for each framework in `docker-compose.yml` inherit from this base image (`FROM quantum-base:latest`).
3.  **Volume Mounting**: The source code is mounted dynamically (`.:/app`), allowing the `benchmark.py` script to run inside the container without rebuilding the image for every code change.

## Prerequisites

* **Docker Desktop** (installed and running).
* **Git** (to clone the repository).

## Usage

### 1. Build the Base Image
First, you must build the common image that contains all the dependencies. This prevents installing libraries repeatedly for each container.

      docker build -f Dockerfile.base -t quantum-base:latest .

### 2. Run the Benchmark
Once the base image is ready, use Docker Compose to launch the benchmarks. This will spin up containers for Qiskit, Cirq, PennyLane, MyQLM, and Tket, executing the benchmark.py script inside each one.

      docker-compose up
(You can use docker-compose up --build if you need to recreate the service containers).

### 3. View Results
The containers will print the execution logs to the console. Upon completion, the detailed metrics (Time, RAM, CPU) are saved automatically to a CSV file:

Location: results/framework_name/circuit

### 4. Visualization
To generate the comparative plots (Bar charts, Boxplots, and Stacked Gate Counts) from the CSV data, run the visualization script:

      python graficar_results.py
(Requires matplotlib, seaborn, and pandas installed locally if running outside Docker).
