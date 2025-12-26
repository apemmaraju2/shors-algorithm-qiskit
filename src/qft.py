import numpy as np
from qiskit import QuantumCircuit

def qft(circuit: QuantumCircuit, n: int) -> None:
    """
    In-place Quantum Fourier Transform on the first n qubits of `circuit`.
    """
    for j in range(n):
        circuit.h(j)
        for k in range(j + 1, n):
            circuit.cp(np.pi / (2 ** (k - j)), k, j)

    # Reverse qubit order
    for i in range(n // 2):
        circuit.swap(i, n - i - 1)


def inverse_qft(circuit: QuantumCircuit, n: int) -> None:
    """
    In-place inverse QFT on the first n qubits of `circuit`.
    """
    # Reverse qubit order
    for i in range(n // 2):
        circuit.swap(i, n - i - 1)

    for j in reversed(range(n)):
        for k in reversed(range(j + 1, n)):
            circuit.cp(-np.pi / (2 ** (k - j)), k, j)
        circuit.h(j)

