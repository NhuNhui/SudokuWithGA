import random

# Kích thước Sudoku
GRID_SIZE = 9
SUBGRID_SIZE = 3

# Hàm đánh giá độ phù hợp: Tính số lượng cặp số trùng
def fitness(sudoku):
    conflicts = 0
    
    # Kiểm tra những xung đột trong hàng
    for row in range(GRID_SIZE):
        row_count = [0] * (GRID_SIZE + 1)
        for col in range(GRID_SIZE):
            value = sudoku[row][col]
            if value > 0:
                row_count[value] += 1
        conflicts += sum(count - 1 for count in row_count if count > 1)

    # Kiểm tra những xung đột trong cột
    for col in range(GRID_SIZE):
        col_count = [0] * (GRID_SIZE + 1)
        for row in range(GRID_SIZE):
            value = sudoku[row][col]
            if value > 0:
                col_count[value] += 1
        conflicts += sum(count - 1 for count in col_count if count > 1)

    # Kiểm tra những xung đột trong 3x3 subgrid
    for box_row in range(SUBGRID_SIZE):
        for box_col in range(SUBGRID_SIZE):
            box_count = [0] * (GRID_SIZE + 1)
            for row in range(box_row * SUBGRID_SIZE, (box_row + 1) * SUBGRID_SIZE):
                for col in range(box_col * SUBGRID_SIZE, (box_col + 1) * SUBGRID_SIZE):
                    value = sudoku[row][col]
                    if value > 0:
                        box_count[value] += 1
            conflicts += sum(count - 1 for count in box_count if count > 1)

    return conflicts

# Tạo một quần thể ban đầu
def create_initial_population(pop_size, clues):
    population = []
    
    for _ in range(pop_size):
        # Bắt đầu từ một lưới all-zeros
        new_sudoku = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        
        # Điền gợi ý vào Sudoku
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                new_sudoku[i][j] = clues[i][j]

        # Điền các ô trống với các giá trị ngẫu nhiên
        for i in range(GRID_SIZE):
            current_row_values = [new_sudoku[i][j] for j in range(GRID_SIZE) if new_sudoku[i][j] != 0]
            missing_values = [value for value in range(1, GRID_SIZE + 1) if value not in current_row_values]
            random.shuffle(missing_values)
            
            for j in range(GRID_SIZE):
                if new_sudoku[i][j] == 0:
                    if missing_values:
                        new_sudoku[i][j] = missing_values.pop()

        population.append(new_sudoku)

    return population

# Chọn lọc
def selection(population):
    assessed_population = [(sudoku, fitness(sudoku)) for sudoku in population]
    assessed_population.sort(key=lambda x: x[1])  # Sắp xếp theo độ phù hợp
    return [sudoku for sudoku, _ in assessed_population[:len(population) // 2]]  # Lấy nửa tốt nhất

# Giao phối
def crossover(parent1, parent2):
    child = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
    crossover_point = random.randint(0, GRID_SIZE - 1)

    for i in range(GRID_SIZE):
        if i < crossover_point:
            child[i] = parent1[i][:]
        else:
            child[i] = parent2[i][:]
    
    return child

# Đột biến
def mutate(sudoku, mutation_rate=0.05):
    for i in range(GRID_SIZE):
        if random.random() < mutation_rate:  # Giá trị ngẫu nhiên giữa 0 và 1
            j1, j2 = random.sample(range(GRID_SIZE), 2)
            # Hoán đổi hai số trong một hàng
            sudoku[i][j1], sudoku[i][j2] = sudoku[i][j2], sudoku[i][j1]

# Hàm chính để giải Sudoku bằng thuật toán di truyền
def genetic_algorithm_sudoku(clues, pop_size=100, generations=1000):
    population = create_initial_population(pop_size, clues)
    
    for generation in range(generations):
        population = selection(population)

        new_population = []
        for _ in range(pop_size):
            parents = random.sample(population, 2)
            child = crossover(parents[0], parents[1])
            mutate(child)
            new_population.append(child)

        population = new_population

        # Kiểm tra xem có giải pháp nào hợp lệ không
        for sudoku in population:
            if fitness(sudoku) == 0:
                return sudoku

    return None


def generate_initial_state():
    # Khởi tạo bảng với số ngẫu nhiên
    state = [[0] * 9 for _ in range(9)]
    for i in range(random.randint(17, 30)):  # Đảm bảo có đủ ô đã điền
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        if state[row][col] == 0:
            state[row][col] = random.randint(1, 9)
    return state
   

def is_valid_sudoku(board):
    # Kiểm tra hàng
    for row in board:
        if not is_valid_unit(row):
            return False

    # Kiểm tra cột
    for col in range(9):
        column = [board[row][col] for row in range(9)]
        if not is_valid_unit(column):
            return False

    # Kiểm tra các vùng 3x3
    for box_row in range(3):
        for box_col in range(3):
            box = []
            for row in range(box_row * 3, box_row * 3 + 3):
                for col in range(box_col * 3, box_col * 3 + 3):
                    box.append(board[row][col])
            if not is_valid_unit(box):
                return False
    
    return True

def is_valid_unit(unit):
    #Kiểm tra tính hợp lệ của một hàng, cột hoặc vùng 3x3
    unit = [num for num in unit if num != 0]  # Lọc bỏ các ô trống (giá trị 0)
    return len(unit) == len(set(unit))  # So sánh số lượng phần tử và số lượng phần tử duy nhất

if __name__ == "__main__":
    matrix = generate_initial_state()
    
    while(True): #chạy đến khi nào không bị đụng độA
        if(is_valid_sudoku(matrix)):
            break
        matrix = generate_initial_state()
    
    print("\n------------- Init State -------------\n")
    for i in range(9):
        print(matrix[i])
    
    solution = genetic_algorithm_sudoku(matrix)
    
    if solution is not None:
        print("\n------------- Solution -------------\n")
        for row in solution:
            print(row)
    else:
        print("\n------------- No solution -------------\n")
