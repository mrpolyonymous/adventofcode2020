def read_input(file_name):
    instructions = []
    with open(file_name) as input_file:
        for line in input_file:
            kv = line.strip().split(" = ")
            instructions.append( (kv[0], kv[1]) )
    return instructions

def part1(instructions):
    and_mask = 0
    or_mask = 0
    memory_values = dict()
    for instruction in instructions:
        if instruction[0] == "mask":
            (and_mask, or_mask) = parse_mask(instruction[1])
        elif instruction[0].startswith("mem"):
            value = int(instruction[1])
            value &= and_mask
            value |= or_mask
            memory_values[instruction[0]] = value
        else:
            raise RuntimeError("unhandled case")

    sum_of_values = 0
    for v in memory_values.values(): sum_of_values += v
    return sum_of_values

def parse_mask(mask_str):
    and_mask = 0
    or_mask = 0
    for c in mask_str:
        if c == "1":
            and_mask = (and_mask << 1) | 1
            or_mask = (or_mask << 1) | 1
        elif c == "0":
            and_mask = (and_mask << 1) | 0
            or_mask = (or_mask << 1) | 0
        elif c == "X":
            and_mask = (and_mask << 1) | 1
            or_mask = (or_mask << 1) | 0
        else:
            raise RuntimeError("Unhandled mask")
    return (and_mask, or_mask)

def part2(instructions):
    mask_str = "0"
    memory_values = dict()
    for instruction in instructions:
        if instruction[0] == "mask":
            mask_str = instruction[1]
        elif instruction[0].startswith("mem"):
            base_address = int(instruction[0][instruction[0].index("[")+1:instruction[0].index("]")])
            all_addresses = combine_with_mask(base_address, mask_str)
            for addr in all_addresses: memory_values[addr] = int(instruction[1])
        else:
            raise RuntimeError("unhandled case")

    sum_of_values = 0
    for v in memory_values.values(): sum_of_values += v
    return sum_of_values

def combine_with_mask(address, mask_str):
    # If the bitmask bit is 0, the corresponding memory address bit is unchanged.
    # If the bitmask bit is 1, the corresponding memory address bit is overwritten with 1.
    # If the bitmask bit is X, the corresponding memory address bit is floating.
    bit_mask = 1
    combined_with_mask = [0]
    for c in reversed(mask_str):
        if c == "1":
            combined_with_mask = [x|bit_mask for x in combined_with_mask]
        elif c == "0":
            combined_with_mask = [x|(address&bit_mask) for x in combined_with_mask]
        elif c == "X":
            new_list = []
            for addr in combined_with_mask:
                new_list.append(addr)
                new_list.append(addr|bit_mask)
            combined_with_mask = new_list
        else:
            raise RuntimeError("Unhandled mask")

        bit_mask <<= 1

    # for addr in combined_with_mask: print("{:036b}".format(addr))
    return combined_with_mask

 
instructions = read_input('day14_input.txt')
#instructions = read_input('day14_example_input.txt')
# for i in instructions: print(i)

part1_answer = part1(instructions)
print("Part 1: {}".format(part1_answer))
part2_answer = part2(instructions)
print("Part 2: {}".format(part2_answer))
