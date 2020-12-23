from functools import reduce

def read_input(file_name):
    rows = []
    with open(file_name) as input_file:
        for line in input_file:
            line = line.strip()
            columns = [0 for i in range(len(line))]
            for i in range(len(line)):
                if line[i] == "#":
                    columns[i] = 1
            rows.append(columns)
    return rows

def part1(starting_grid):
    return run_game_3d(starting_grid, 6)

def run_game_3d(starting_grid, max_iters):
    num_active = 0
    num_rows = len(starting_grid)
    num_columns = len(starting_grid[0])
    # expand grid way beyond what is needed because I can't be bothered to code the required if checks.
    expanded_row_count = num_rows + 2*(max_iters+1)
    expanded_col_count = num_columns + 2*(max_iters+1)
    expanded_stack_count = 1 + 2*(max_iters+1)

    # top-left of original grid is [0, 0, 0],
    # which will be [max_iters+1, max_iters+1, max_iters+1] in the expanded grid
    current_lattice = [[[0 for i in range(expanded_col_count)] for j in range(expanded_row_count)] for k in range(expanded_stack_count)]
    new_lattice = [[[0 for i in range(expanded_col_count)] for j in range(expanded_row_count)] for k in range(expanded_stack_count)]
    for row in range(num_rows):
        for col in range(num_columns):
            current_lattice[max_iters+1][row+max_iters+1][col+max_iters+1] = starting_grid[row][col]

    print_lattice(current_lattice)

    # Rules
    # If a cube is active and exactly 2 or 3 of its neighbors are also active, the cube remains active. Otherwise, the cube becomes inactive.
    # If a cube is inactive but exactly 3 of its neighbors are active, the cube becomes active. Otherwise, the cube remains inactive.

    z_min = max_iters + 1
    z_max = max_iters + 1
    y_min = max_iters + 1
    y_max = max_iters + num_rows
    x_min = max_iters + 1
    x_max = max_iters + num_columns
    for iter in range(max_iters):
        z_min -= 1
        z_max += 1
        y_min -= 1
        y_max += 1
        x_min -= 1
        x_max += 1
        for z in range( z_min, z_max + 1):
            for y in range( y_min, y_max + 1):
                for x in range( x_min, x_max + 1):
                    active_neighbors = count_3d_neighbors(current_lattice, z, y, x)
                    if current_lattice[z][y][x] > 0:
                        if active_neighbors == 2 or active_neighbors == 3:
                            new_lattice[z][y][x] = 1
                        else:
                            new_lattice[z][y][x] = 0
                    else:
                        if active_neighbors == 3:
                            new_lattice[z][y][x] = 1
                        else:
                            new_lattice[z][y][x] = 0
        tmp = current_lattice
        current_lattice = new_lattice
        new_lattice = tmp
        print("Iteration {}".format(iter))
    
    for stack in current_lattice:
        for row in stack:
            num_active += reduce(sum, row)
    return num_active

def sum(a, b):
    return a+b

def print_lattice(lattice):
    num_iters = len(lattice) // 2
    z = -num_iters
    for l in range(len(lattice)):
        print("z={}".format(z))
        z+=1
        for row in lattice[l]:
            print(row)

def make_3d_neighbors():
    neighbors = []
    for x in [-1, 0, 1]:
        for y in [-1, 0, 1]:
            for z in [-1, 0, 1]:
                if x != 0 or y != 0 or z != 0:
                    neighbors.append((x, y, z))
    return neighbors
                
three_d_neighbors = make_3d_neighbors()


def count_3d_neighbors(lattice, z, y, x):
    n_count = 0
    for offsets in three_d_neighbors:
        n_count += lattice[z + offsets[0]][y + offsets[1]][x + offsets[2]]
    return n_count

def part2(starting_grid):
    return run_game_4d(starting_grid, 6)

def run_game_4d(starting_grid, max_iters):
    num_active = 0
    num_rows = len(starting_grid)
    num_columns = len(starting_grid[0])
    # expand grid way beyond what is needed because I can't be bothered to code the required if checks.
    expanded_row_count = num_rows + 2*(max_iters+1)
    expanded_col_count = num_columns + 2*(max_iters+1)
    expanded_stack_count = 1 + 2*(max_iters+1)

    # top-left of original grid is [0, 0, 0, 0],
    # which will be [max_iters+1, max_iters+1, max_iters+1, max_iters+1] in the expanded grid
    current_lattice = [[[[0 for x in range(expanded_col_count)] for y in range(expanded_row_count)] for z in range(expanded_stack_count)] for w in range(expanded_stack_count)]
    new_lattice = [[[[0 for x in range(expanded_col_count)] for y in range(expanded_row_count)] for z in range(expanded_stack_count)] for w in range(expanded_stack_count)]
    for row in range(num_rows):
        for col in range(num_columns):
            current_lattice[max_iters+1][max_iters+1][row+max_iters+1][col+max_iters+1] = starting_grid[row][col]

    # Same rules as part 1, but more neighbors

    w_min = max_iters + 1
    w_max = max_iters + 1
    z_min = max_iters + 1
    z_max = max_iters + 1
    y_min = max_iters + 1
    y_max = max_iters + num_rows
    x_min = max_iters + 1
    x_max = max_iters + num_columns
    for iter in range(max_iters):
        w_min -= 1
        w_max += 1
        z_min -= 1
        z_max += 1
        y_min -= 1
        y_max += 1
        x_min -= 1
        x_max += 1
        for w in range(w_min, w_max + 1):
            for z in range( z_min, z_max + 1):
                for y in range( y_min, y_max + 1):
                    for x in range( x_min, x_max + 1):
                        active_neighbors = count_4d_neighbors(current_lattice, w, z, y, x)
                        if current_lattice[w][z][y][x] > 0:
                            if active_neighbors == 2 or active_neighbors == 3:
                                new_lattice[w][z][y][x] = 1
                            else:
                                new_lattice[w][z][y][x] = 0
                        else:
                            if active_neighbors == 3:
                                new_lattice[w][z][y][x] = 1
                            else:
                                new_lattice[w][z][y][x] = 0
        tmp = current_lattice
        current_lattice = new_lattice
        new_lattice = tmp
        print("Iteration {}".format(iter))
    
    for hyper_whatsit in current_lattice:
        for stack in hyper_whatsit:
            for row in stack:
                num_active += reduce(sum, row)
    return num_active

def make_4d_neighbors():
    neighbors = []
    for x in [-1, 0, 1]:
        for y in [-1, 0, 1]:
            for z in [-1, 0, 1]:
                for w in [-1, 0, 1]:
                    if x != 0 or y != 0 or z != 0 or w != 0:
                        neighbors.append((x, y, z, w))
    return neighbors
                
four_d_neighbors = make_4d_neighbors()


def count_4d_neighbors(lattice, w, z, y, x):
    n_count = 0
    for offsets in four_d_neighbors:
        n_count += lattice[w + offsets[0]][z + offsets[1]][y + offsets[2]][x + offsets[3]]
    return n_count



starting_grid = read_input('day17_input.txt')
#starting_grid = read_input('day17_example_input.txt')
for l in starting_grid: print(l)

part1_answer = part1(starting_grid)
print("Part 1: {}".format(part1_answer))
# My answer to part 1: 242
part2_answer = part2(starting_grid)
print("Part 2: {}".format(part2_answer))
# My answer to part 2: 2292
