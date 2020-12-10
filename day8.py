
def read_input():
    # example lines:
    # jmp -388
    # acc +31
    # acc +45
    # nop -555

    instructions = []
    with open('day8_input.txt') as input_file:
        for line in input_file:
            line = line.strip()
            split_line = line.split(" ")
            if len(split_line) != 2:
                # sanity check
                raise RuntimeError("Unmatched line: " + line)
            instructions.append( (split_line[0], int(split_line[1])) )

    return instructions

# Does program terminate, and what is the accumulator value prior to termination
# or entering an infinite loop
def part1(instructions):
    accumulator = 0
    executed_lines = set()
    instruction_index = 0
    while True:
        if instruction_index in executed_lines:
            return (accumulator, True)
        elif instruction_index >= len(instructions):
            return (accumulator, False)

        executed_lines.add(instruction_index)
        instruction = instructions[instruction_index]
        if instruction[0] == "jmp":
            instruction_index += instruction[1]
        elif instruction[0] == "acc":
            accumulator += instruction[1]
            instruction_index += 1
        elif instruction[0] == "nop":
            instruction_index += 1
        else:
            raise RuntimeError("Unhandled instruction: {}".format(instruction[0]))

    return accumulator

# Part 2: One of the nops has been switched to jmp, or vice-versa.
# which one is it, and what is the accumulator value when the program
# is fixed?
def part2(instructions):
    # brute-force time.
    for i in range(0, len(instructions)):
        instruction = instructions[i]
        if instruction[0] == "acc":
            continue

        instructions_fixed = instructions.copy()
        if (instruction[0] == "nop"):
            instructions_fixed[i] = ("jmp", instruction[1])
        else:
            instructions_fixed[i] = ("nop", instruction[1])

        program_results = part1(instructions_fixed)
        if program_results[1] == False:
            print("Fixing instruction {}, {} fixed the program".format(i, instruction))
            return program_results[0]

    raise RuntimeError("Could not find a single instruction to fix")

instructions = read_input()
print("Part 1: accumulator before infinite loop begins: {}".format(part1(instructions)[0]))
print("Part 2: accumulator after fixing program={}".format(part2(instructions)))
