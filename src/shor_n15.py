from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

from src.qft import inverse_qft


def c_amod15(a, power):
    """
    Controlled modular multiplication by a^power mod 15.
    Works for a in {2,7,8,11,13}.
    """
    U = QuantumCircuit(4)

    for _ in range(power):
        if a in [2, 13]:
            U.swap(2, 3)
            U.swap(1, 2)
            U.swap(0, 1)
        if a in [7, 8]:
            U.swap(0, 1)
            U.swap(1, 2)
            U.swap(2, 3)
        if a in [11, 14]:
            U.swap(0, 2)
            U.swap(1, 3)
        if a in [7, 11, 13]:
            for q in range(4):
                U.x(q)

    U = U.to_gate()
    U.name = f"{a}^{power} mod 15"
    return U.control()


def build_order_finding_circuit(a):
    """
    Build the quantum circuit for order finding in Shor's algorithm.
    N = 15
    """
    n_count = 8  # counting qubits
    qc = QuantumCircuit(n_count + 4, n_count)

    # Initialize counting qubits
    for q in range(n_count):
        qc.h(q)

    # Initialize work register to |1>
    qc.x(n_count + 3)

    # Controlled modular exponentiation
    for q in range(n_count):
        qc.append(
            c_amod15(a, 2 ** q),
            [q] + list(range(n_count, n_count + 4))
        )

    # Inverse QFT
    inverse_qft(qc, n_count)

    # Measurement
    qc.measure(range(n_count), range(n_count))

    return qc


def run_shor(a=7, shots=1024):
    """
    Run Shor order finding using Aer simulator.
    """
    qc = build_order_finding_circuit(a)
    backend = AerSimulator()
    tqc = transpile(qc, backend)
    result = backend.run(tqc, shots=shots).result()
    return result.get_counts()

