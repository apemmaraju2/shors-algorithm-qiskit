from math import gcd
from fractions import Fraction

def continued_fraction_phase(phase, max_denominator):
    """
    Approximate a phase using continued fractions.
    """
    frac = Fraction(phase).limit_denominator(max_denominator)
    return frac.numerator, frac.denominator


def recover_period(measured_value, num_qubits, max_denominator=15):
    """
    Recover the period r from a measured QFT value.
    """
    phase = measured_value / (2 ** num_qubits)
    _, r = continued_fraction_phase(phase, max_denominator)
    return r


def factor_from_period(a, r, N):
    """
    Classical post-processing step of Shor's algorithm.
    """
    if r % 2 != 0:
        return None

    x = pow(a, r // 2, N)
    if x == N - 1:
        return None

    p = gcd(x - 1, N)
    q = gcd(x + 1, N)

    if p * q == N and p > 1 and q > 1:
        return p, q

    return None

