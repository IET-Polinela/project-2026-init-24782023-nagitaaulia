import random

class NQueensSolver:
    def __init__(self, n=8):
        self.n = n
    
    def generate_random_state(self):
        return [random.randint(0, self.n - 1) for _ in range(self.n)]

    def calculate_cost(self, state):
        conflicts = 0
        for i in range(self.n):
            for j in range(i + 1, self.n):
                if state[i] == state[j]:
                    conflicts += 1
                elif abs(state[i] - state[j]) == abs(i - j):
                    conflicts += 1
        return conflicts

    def get_neighbors(self, state):
        neighbors = []
        for col in range(self.n):
            for row in range(self.n):
                if state[col] != row:
                    new_state = list(state)
                    new_state[col] = row
                    neighbors.append(new_state)
        return neighbors

    def hill_climbing(self, max_restart=0):
        
        # --- KODE MAHASISWA DISINI ---
        current = self.generate_random_state()
        current_cost = self.calculate_cost(current)
        steps = 0

        while True:
            neighbors = self.get_neighbors(current)

            best_neighbor = None
            best_cost = current_cost

            for neighbor in neighbors:
                cost = self.calculate_cost(neighbor)
                if cost < best_cost:
                    best_neighbor = neighbor
                    best_cost = cost

            if best_neighbor is None:
                break

            current = best_neighbor
            current_cost = best_cost
            steps += 1

            if current_cost == 0:
                break

        return current, current_cost, steps

    def visualize_board(self, state):
        """Mencetak papan catur ke terminal."""
        board = [['.' for _ in range(self.n)] for _ in range(self.n)]
        for col, row in enumerate(state):
            board[row][col] = 'Q'
        
        print("\n".join([" ".join(row) for row in board]))
        print(f"Cost: {self.calculate_cost(state)}")

# --- MAIN EXPERIMENT ---
if __name__ == "__main__":
    n = 8
    solver = NQueensSolver(n)
    
    print(f"--- EXPERIMENT 1: Single Run Hill Climbing (N={n}) ---")
    # Jalankan sekali, lihat hasilnya
    # (Mahasiswa harus mengisi fungsi hill_climbing dulu)
    
    final_state, final_cost, steps = solver.hill_climbing()

    print("\n[Final Board State]")
    solver.visualize_board(final_state)
    print(f"Langkah yang diambil: {steps} steps")

    if final_cost == 0:
        print("KESIMPULAN: BERHASIL (Solusi optimal ditemukan)")
    else:
        print(f"KESIMPULAN: STUCK! (Terjebak di Local Optimum dengan {final_cost} konflik)")

    print("\n--- EXPERIMENT 2: Failure Analysis (100 Runs) ---")
    # TUGAS MAHASISWA:
    # Jalankan hill_climbing() sebanyak 100 kali.
    # Hitung:
    # 1. Berapa kali sukses (Cost = 0)?
    # 2. Berapa kali gagal (Cost > 0)?
    # 3. Rata-rata cost saat gagal?
    
    success = 0
    failure = 0
    total_failure_cost = 0

    for _ in range(100):
        _, cost, _ = solver.hill_climbing()

        if cost == 0:
            success += 1
        else:
            failure += 1
            total_failure_cost += cost

    avg_failure_cost = total_failure_cost / failure if failure > 0 else 0

    print(f"Total Runs        : 100")
    print(f"Success Rate      : {success}%")
    print(f"Failure Rate      : {failure}%")
    print(f"Average Failure Cost : {avg_failure_cost:.2f}")