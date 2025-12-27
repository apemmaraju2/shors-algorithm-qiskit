from src.shor_n15 import run_shor

def main():
    print("Running Shor's algorithm for N = 15 (a = 7)")
    counts = run_shor(a=7, shots=1024)
    print("Measurement results:")
    print(counts)

if __name__ == "__main__":
    main()

