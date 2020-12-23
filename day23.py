def read_input(file_name):
    inputs = []
    with open(file_name) as input_file:
        for line in input_file:
            line = line.strip()
            inputs.append(line)

    return inputs

def part1(input):
    answer = 0
    return answer


def part2(input):
    answer = 0
    return answer

input = read_input('day23_input.txt')
# input = read_input('day23_example_input.txt')
# for l in input: print(l)

part1_answer = part1(input)
print(f"Part 1: {part1_answer}")
# My answer to part 1: 
part2_answer = part2(input)
print(f"Part 2: {part2_answer}")
# My answer to part 2: 
