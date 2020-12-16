def read_input(file_name):
    with open(file_name) as input_file:
        for line in input_file:
            return line.strip().split(",")

def part1(starting_numbers):
    return run_game(starting_numbers, 2020)

def part2(starting_numbers):
    # there must be a trick to this but brute force works just fine
    return run_game(starting_numbers, 30000000)

def run_game(starting_numbers, max_iters):
    turns_for_numbers = dict()
    for i, n in enumerate(starting_numbers):
        last_number = int(n)
        turns_for_number = [i]
        turns_for_numbers[last_number] = turns_for_number

    next_number = 0
    for i in range(len(starting_numbers), max_iters):
        if len(turns_for_number) == 1:
            next_number = 0
        else:
            next_number = turns_for_number[1] - turns_for_number[0]

        if next_number in turns_for_numbers:
            turns_for_number = turns_for_numbers[next_number]
            if len(turns_for_number) == 1:
                turns_for_number.append(i)
            else:
                turns_for_number[0] = turns_for_number[1]
                turns_for_number[1] = i
        else:
            turns_for_number = [i]
            turns_for_numbers[next_number] = turns_for_number

        # print("Turn {}: number spoken is {}".format(i+1, next_number))
        # print(turns_for_numbers)
        last_number = next_number

    # print(len(turns_for_numbers))
    return last_number


starting_numbers = read_input('day15_input.txt')

# starting_numbers = [0, 3, 6]
# starting_numbers = [1, 3, 2] # 1
# starting_numbers = [2, 1, 3] # 10
# starting_numbers = [1, 2, 3] # 27
# starting_numbers = [2, 3, 1] # 78
# starting_numbers = [3, 2, 1] # 438
# starting_numbers = [3, 1, 2] # 1836

part1_answer = part1(starting_numbers)
print("Part 1: {}".format(part1_answer))
# My answer to part 1: 870
part2_answer = part2(starting_numbers)
print("Part 2: {}".format(part2_answer))
# My answer to part 2: 9136
