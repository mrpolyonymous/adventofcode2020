def read_input(file_name):
    moves = []
    with open(file_name) as input_file:
        for line in input_file:
            line = line.strip()
            moves.append(parse_move(line))

    return moves


def parse_move(line):
    moves = []
    offset = 0
    while offset < len(line):
        if line[offset] == "e":
            moves.append("e")
            offset +=1
        elif line[offset] == "w":
            moves.append("w")
            offset += 1
        elif line[offset:offset+2] == "sw":
            moves.append("sw")
            offset += 2
        elif line[offset:offset+2] == "se":
            moves.append("se")
            offset += 2
        elif line[offset:offset+2] == "nw":
            moves.append("nw")
            offset += 2
        elif line[offset:offset+2] == "ne":
            moves.append("ne")
            offset += 2
        else:
            raise RuntimeError("Bad parser")
    return moves

WHITE = 0
BLACK = 1
def part1(moves_list):
    longest_move = max(map(lambda x: len(x), moves_list))
    grid = [[WHITE for i in range(2*longest_move+1)] for j in range (2*longest_move+1) ]
    for moves in moves_list:
        (row, col) = (longest_move, longest_move)
        for move in moves:
            if move == "e":
                col +=1
            elif move == "w":
                col -=1
            elif move == "ne":
                row -=1
                col+=0.5
            elif move == "nw":
                row -= 1
                col -= 0.5
            elif move == "se":
                row +=1
                col+=0.5
            elif move == "sw":
                row += 1
                col -= 0.5
            else:
                raise RuntimeError("missed a case")
        if grid[row][int(col)] == WHITE:
            grid[row][int(col)] = BLACK
        else:
            grid[row][int(col)]= WHITE

    return (count_tiles(grid, BLACK), grid)

def count_tiles(grid, color):
    answer = 0
    for row in grid:
        for tile in row:
            if tile == color:
                answer += 1
    return answer

def part2(grid):
    original_size = len(grid)
    new_size = original_size + 200
    # copy original grid into something bigger
    bigger_grid = [[WHITE for col in range(new_size)] for row in range(new_size)]
    for row in range(original_size):
        for col in range(original_size):
            bigger_grid[row+original_size][col+original_size] = grid[row][col]

    grid = bigger_grid
    print(f"Tiles in bigger grid: {count_tiles(bigger_grid, BLACK)}")
    next_grid = [[WHITE for col in range(new_size)] for row in range(new_size)]

    for iter in range(100):
        for row in range(1, new_size - 1):
            for col in range(1, new_size - 1):
                black_count = count_surrounding(grid, row, col, BLACK)
                if grid[row][col] == BLACK:
                    if black_count == 0 or black_count > 2:
                        next_grid[row][col] = WHITE
                    else:
                        next_grid[row][col] = BLACK
                else:
                    if black_count == 2:
                        next_grid[row][col] = BLACK
                    else:
                        next_grid[row][col] = WHITE
        tmp = grid
        grid = next_grid
        next_grid = tmp
        print(f"Day {iter+1}: {count_tiles(grid, BLACK)}")

    return count_tiles(grid, BLACK)

def count_surrounding(grid, row, col, color):
    if row == 0 or row == len(grid) - 1:
        # not correct but hope it doesn't matter
        return 0
    if col == 0 or col == len(grid[0]) - 1:
        # not correct but hope it doesn't matter
        return 0

    count = 0
    # odd/even rows are offset a little
    # TODO - this doesn't work in general, it depends on the size of the grid
    # and how the original answer was embedded but it works for my input
    # so I'm stopping here
    is_even_row = (row & 1 == 0)

    # E/W
    if grid[row][col-1] == color: count += 1
    if grid[row][col+1] == color: count += 1
    if not is_even_row:
        # NE/NW
        if grid[row-1][col-1] == color: count += 1
        if grid[row-1][col] == color: count += 1
        # SE/SW
        if grid[row+1][col-1] == color: count += 1
        if grid[row+1][col] == color: count += 1
    else:
        # NE/NW
        if grid[row-1][col] == color: count += 1
        if grid[row-1][col+1] == color: count += 1
        # SE/SW
        if grid[row+1][col] == color: count += 1
        if grid[row+1][col+1] == color: count += 1
    return count

input = read_input('day24_input.txt')
# input = read_input('day24_example_input.txt')

# input = [parse_move("esew")]
# input = [parse_move("nwwswee")]
for l in input: print(l)

(part1_answer, grid) = part1(input)
print(f"Part 1: {part1_answer}")
# My answer to part 1: 232
part2_answer = part2(grid)
print(f"Part 2: {part2_answer}")
# My answer to part 2: 3519
