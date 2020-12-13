# EMPTY = "L"
# OCCUPIED = "#"
# FIXED = "."
EMPTY = 0
OCCUPIED = 1
FIXED = -1

def read_input(file_name):
    seats = []

    with open(file_name) as input_file:
        for line in input_file:
            line = line.strip()
            seats.append( list(map(map_input, line) ))

    return seats

# Failed attempt to speed up the program
def map_input(x):
    if x == ".":
        return FIXED
    elif x == "L":
        return EMPTY
    elif x == "#":
        return OCCUPIED
    else:
        raise RuntimeError("Unhandled input")

# The following rules are applied to every seat simultaneously:

# If a seat is empty (L) and there are no occupied seats adjacent to it, the seat becomes occupied.
# If a seat is occupied (#) and four or more seats adjacent to it are also occupied, the seat becomes empty.
# Otherwise, the seat's state does not change.
# Floor (.) never changes; seats don't move, and nobody sits on the floor.
# adjacent = left, right, or diagonal from the seat
def part1(seats):
    # My answer: 2303
    return run_iterations(seats, 1, 4)

# Part 2: like part 1, but different rules for state change
def part2(seats):
    # my answer: 2057
    return run_iterations(seats, max(len(seats), len(seats[0])), 5)

def run_iterations(seats, max_extent, occupied_limit):
    num_cycles = 0
    num_rows = len(seats)
    num_columns = len(seats[0])
    seats_copy = [row.copy() for row in seats]
    new_seat_state = [ [FIXED for j in range(num_columns)] for i in range(num_rows) ]

    while True:
        num_cycles += 1
        num_changes = 0

        for row in range(num_rows):
            for column in range(num_columns):
                current_state = seats_copy[row][column]
                if current_state != FIXED:
                    occupied = count_occupied(seats_copy, row, column, max_extent)
                    if current_state == EMPTY and occupied == 0:
                        new_seat_state[row][column] = OCCUPIED
                        num_changes += 1
                    elif current_state == OCCUPIED and occupied >= occupied_limit:
                        new_seat_state[row][column] = EMPTY
                        num_changes += 1
                    else:
                        new_seat_state[row][column] = current_state

        if num_changes == 0 or num_cycles > 1000:
            break
        # else:
        #     print("Iteration {} num changes: {}".format(num_cycles, num_changes))

        tmp = new_seat_state
        new_seat_state = seats_copy
        seats_copy = tmp

    num_occupied = 0
    for row in seats_copy:
        for seat in row:
            if seat == OCCUPIED:
                num_occupied += 1

    return num_occupied

def count_occupied(seats, row, column, max_extent):
    occupied = 0
    offsets = [-1, 0, 1]
    num_rows = len(seats)
    num_columns = len(seats[0])

    for r in offsets:
        for c in offsets:
            if r == 0 and c == 0:
                continue
            for i in range(1, max_extent + 1):
                offset_row = row + r * i
                if offset_row < 0 or offset_row >= num_rows:
                    break
                offset_column = column + c * i
                if offset_column < 0 or offset_column >= num_columns:
                    break

                current_state = seats[offset_row][offset_column]
                if current_state == OCCUPIED:
                    occupied += 1
                    break
                elif current_state == EMPTY:
                    break

    return occupied

# This is pathetically slow. Not sure why, this would be fast in Java.
seats = read_input('day11_input.txt')
num_seats_filled = part1(seats)
print("Part 1: number of seats filled : {}".format(num_seats_filled))
num_seats_filled = part2(seats)
print("Part 2: number of seats filled {}".format(num_seats_filled))
