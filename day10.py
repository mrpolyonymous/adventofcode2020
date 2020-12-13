def read_input():
    joltages = []
    with open('day10_input.txt') as input_file:
        for line in input_file:
            line = line.strip()
            joltages.append( int(line) )

    return joltages

# Find a chain that uses all of your adapters to connect the charging outlet
# to your device's built-in adapter and count the joltage differences
# between the charging outlet, the adapters, and your device. What is
# the number of 1-jolt differences multiplied by the number of 3-jolt
# differences?
def part1(joltages):
    # 1 in position 3 as there's an implicit 3 jolt jump
    # as the last step
    diffs = [0, 0, 0, 1]
    for i in range(1, len(joltages)):
        diff = joltages[i] - joltages[i-1]
        diffs[diff] += 1

    return diffs

# Part 2: What is the total number of distinct ways you can arrange
# the adapters to connect the charging outlet to your device?
def part2(joltages, joltage_jumps):
    # observation: 3-jolt jumps are mandatory and so don't count for anything
    # How many possibilites does a run of n consecutive 1-jolt jumps allow for?
    # Find all the runs of 1-jumps, then how many possibilites they provide,
    # then multiply them all.

    # Consider runs  x, x+1, x+2, ..., x+N
    # For N=2, the 2 possibilities are:
    #    0, 1, 2 OR 0, 2
    # For N=3, the 4 possibilities are:
    #    0, 1, 2, 3 OR 0, 2, 3 OR 0, 1, 3 OR 0, 3
    # For N=4, the 7 possibilities are:
    #    0, 1, 2, 3, 4 OR 0, 2, 3, 4 OR 0, 1, 3, 4 OR 0, 1, 2, 4 OR
    #    0, 1, 4 OR 0, 2, 4 OR 0, 3, 4
    # There must be a more satisfying way to do this but N=4 is all that was
    # needed to solve the problem
    permutations = [1, 1, 2, 4, 7]
    one_jump_runs = []
    run_length = 0
    
    for i in range(1, len(joltages)):
        diff = joltages[i] - joltages[i - 1]
        if diff == 1:
            run_length += 1
        else:
            one_jump_runs.append(run_length)
            run_length = 0
    one_jump_runs.append(run_length)
    one_jump_runs = list(filter(lambda x: x > 1, one_jump_runs))

    total_possibilities = 1
    for run_length in one_jump_runs:
        total_possibilities *= permutations[run_length]

    return total_possibilities


joltages = read_input()
joltages.append(0) # add implicit 0 that forms the start of the chain
joltages = sorted(joltages)
joltage_jumps = part1(joltages)
print("Part 1: product of 1-jolt jumps with 3-jolt jumps : {}"
    .format(joltage_jumps[1] * joltage_jumps[3]))
print("Part 2: Total possible arrangements of adapters {}".format(part2(joltages, joltage_jumps)))
