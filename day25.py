import math

def read_input(file_name):
    inputs = []
    with open(file_name) as input_file:
        for line in input_file:
            line = line.strip()
            inputs.append(int(line))

    return inputs

def part1(input):
    card_public_key = input[0]
    card_secret = discrete_log_20201227_7(card_public_key)
    door_public_key = input[1]
    door_secret = discrete_log_20201227_7(door_public_key)

    ek1 = mod_exp(door_public_key, card_secret)
    ek2 = mod_exp(card_public_key, door_secret)
    print(f"{ek1}, {ek2}")
    if ek1 != ek2:
        raise RuntimeError("You didn't understand the question and implemented this incorrectly")
    return ek1

def mod_exp(subject_number, loop_size):
    curr_val = 1
    for _ in range(loop_size):
        curr_val = (curr_val * subject_number) % 20201227
    return curr_val

def discrete_log_20201227_7(n):
    # Small enough that it finishes in a reasonable amount of time
    curr_val = 1
    for i in range(20201227):
        curr_val = (curr_val * 7) % 20201227
        if curr_val == n:
            print(f"Discrete log is {i+1}")
            return i+1
    raise RuntimeError("Couldnt do it")

# 20201227 is prime, this prints nothing
# for i in range(2, int(math.sqrt(20201227))):
#     if 20201227 % i == 0:
#         print(f"{i} is a factor")

input = read_input('day25_input.txt')
# input = [5764801, 17807724]
# for l in input: print(l)

part1_answer = part1(input)
print(f"Part 1: {part1_answer}")
# My answer to part 1: 12929

# There is no part 2
