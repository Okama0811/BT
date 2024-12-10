import numpy as np
import matplotlib.pyplot as plt

# Hàm mục tiêu Rastrigin
def rastrigin(x):
    A = 10
    return A * len(x) + sum(x_i**2 - A * np.cos(2 * np.pi * x_i) for x_i in x)

# Thuật toán Moth-Flame Optimization (MFO)
class MFO:
    def __init__(self, population_size, max_iter, dim, lower_bound, upper_bound):
        self.population_size = population_size  # Số lượng cá thể trong quần thể
        self.max_iter = max_iter  # Số vòng lặp tối đa
        self.dim = dim  # Số chiều của không gian tìm kiếm
        self.lower_bound = lower_bound  # Giới hạn dưới của không gian tìm kiếm
        self.upper_bound = upper_bound  # Giới hạn trên của không gian tìm kiếm
        self.population = np.random.uniform(self.lower_bound, self.upper_bound, (self.population_size, self.dim))  # Khởi tạo quần thể ngẫu nhiên
        self.best_solution = None  # Giải pháp tốt nhất
        self.best_fitness = float('inf')  # Giá trị hàm mục tiêu tốt nhất (khởi tạo vô cùng)

    # Hàm tính toán độ phù hợp (fitness)
    def fitness(self, solution):
        return rastrigin(solution)

    # Hàm cập nhật vị trí của một con bướm
    def update_position(self, moth, flame, iteration):
        distance = np.abs(flame - moth)  # Khoảng cách giữa con bướm và ngọn lửa
        a = 2 - iteration * (2 / self.max_iter)  # Tham số điều chỉnh
        return flame - a * distance * np.random.randn(self.dim)  # Cập nhật vị trí của con bướm

    # Hàm tối ưu hóa chính
    def optimize(self):
        history = []  # Lịch sử độ phù hợp tốt nhất qua các vòng lặp
        moths_positions = []  # Danh sách các vị trí của bướm đêm
        flames_positions = []  # Danh sách các vị trí của ngọn lửa
        for iteration in range(self.max_iter):
            flames = self.population[np.argsort([self.fitness(moth) for moth in self.population])]  # Sắp xếp quần thể theo độ phù hợp
            best_flame = flames[0]  # Ngọn lửa tốt nhất
            best_fitness = self.fitness(best_flame)  # Độ phù hợp của ngọn lửa tốt nhất

            if best_fitness < self.best_fitness:  # Cập nhật giải pháp tốt nhất
                self.best_fitness = best_fitness
                self.best_solution = best_flame

            # Lưu các vị trí của bướm đêm và ngọn lửa
            moths_positions.append(self.population)
            flames_positions.append(best_flame)

            new_population = []  # Quần thể mới
            for moth in self.population:
                flame = flames[np.random.randint(0, self.population_size)]  # Chọn ngẫu nhiên một ngọn lửa
                new_moth = self.update_position(moth, flame, iteration)  # Cập nhật vị trí của con bướm
                new_moth = np.clip(new_moth, self.lower_bound, self.upper_bound)  # Giới hạn giá trị để không vượt quá phạm vi tìm kiếm
                new_population.append(new_moth)

            self.population = np.array(new_population)  # Cập nhật lại quần thể
            history.append(self.best_fitness)  # Lưu giá trị độ phù hợp tốt nhất qua các vòng lặp
            print(f"Vòng lặp {iteration + 1}/{self.max_iter}, Độ phù hợp tốt nhất: {self.best_fitness}")

        return history, moths_positions, flames_positions  # Trả về lịch sử độ phù hợp và vị trí của bướm đêm và ngọn lửa

# Tạo và tối ưu hóa bằng thuật toán MFO
population_size = 50  # Số lượng cá thể trong quần thể
max_iter = 100  # Số vòng lặp tối đa
dim = 10  # Số chiều
lower_bound = -5.12  # Giới hạn dưới
upper_bound = 5.12  # Giới hạn trên

mfo = MFO(population_size, max_iter, dim, lower_bound, upper_bound)
history, moths_positions, flames_positions = mfo.optimize()  # Tối ưu hóa bằng thuật toán MFO

# Vẽ đồ thị kết quả
plt.plot(history)
plt.xlabel('Vòng lặp')
plt.ylabel('Độ phù hợp tốt nhất')
plt.title('Moth-Flame Optimization')

# Vẽ các điểm của bướm đêm và ngọn lửa
moths_positions = np.array(moths_positions)
flames_positions = np.array(flames_positions)

# Vẽ ngọn lửa (giải pháp tốt nhất)
plt.scatter(range(max_iter), flames_positions[:, 0], color='red', label='Ngọn lửa', marker='x')

# Vẽ bướm đêm
for i in range(population_size):
    plt.scatter(range(max_iter), moths_positions[:, i, 0], color='blue', alpha=0.3, label='Bướm đêm' if i == 0 else "")

plt.legend()
plt.show()
