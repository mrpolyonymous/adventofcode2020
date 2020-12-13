from functools import reduce

def read_input(file_name):
    with open(file_name) as input_file:
        lines = input_file.readlines()
        current_time = int(lines[0])
        running = lines[1].split(",")
        return (current_time, running)

def part1(current_time, running):
    running = list(map(lambda x: int(x), filter(lambda x: x != "x", running)))
    min_wait_time = 100000000
    bus_id = -1
    for n in running:
        time_to_wait = n - current_time % n
        if time_to_wait == n:
            time_to_wait = 0
        if time_to_wait < min_wait_time:
            min_wait_time = time_to_wait
            bus_id = n
    return bus_id * min_wait_time

def part2(current_time, running):
    running_with_offset = list(map(lambda x: ( x[0], int(x[1]) ), 
        filter(lambda x: x[1] != "x", enumerate(running))))
    # Find start time t so that
    #   t + offset_i = 0 mod bus_id_i
    #   or t = -offset_i mod bus_id_i
    #   for all elements of running_with_offset

    return chinese_remainder(
        list(map(lambda x: x[1], running_with_offset)),
        list(map(lambda x: -x[0], running_with_offset)) )

# CRT code taken from https://rosettacode.org/wiki/Chinese_remainder_theorem#Python_3.6
# n are the modulos, a is the desired value
def chinese_remainder(n, a):
    sum = 0
    prod = reduce(lambda a, b: a*b, n)
    for n_i, a_i in zip(n, a):
        p = prod // n_i
        sum += a_i * mul_inv(p, n_i) * p
    return sum % prod
 
def mul_inv(a, b):
    b0 = b
    x0, x1 = 0, 1
    if b == 1: return 1
    while a > 1:
        q = a // b
        a, b = b, a%b
        x0, x1 = x1 - q * x0, x0
    if x1 < 0: x1 += b0
    return x1
 
(current_time, running) = read_input('day13_input.txt')

part1_answer = part1(current_time, running)
print("Part 1: {}".format(part1_answer))
part2_answer = part2(current_time, running)
print("Part 2: {}".format(part2_answer))
