print('placeholder for day 9')
 
def read_input():
    xmas_code = []
    with open('day9_input.txt') as input_file:
        for line in input_file:
            line = line.strip()
            xmas_code.append( int(line) )

    return xmas_code

# find the first number in the list (after the preamble) which is not 
# the sum of two of the 25 numbers before it.
def part1(xmas_code):
    for i in range(25, len(xmas_code)):
        prior_numbers = sorted(xmas_code[i-25:i])
        found_prior_numbers = False
        for j in range(0, len(prior_numbers)):
            prior_possibility = prior_numbers[j]
            remaining = xmas_code[i] - prior_possibility

            possible_index = binary_search(remaining, prior_numbers)
            if possible_index >= 0:
                found_prior_numbers = True
                break

        if not found_prior_numbers:
            return xmas_code[i]

    raise RuntimeError("Could not find answer")

# This must exist in python but it's fun to write
def binary_search(find_this, in_this):
    low = 0
    high = len(in_this)
    while True:
        mid = low + ((high - low) >> 1)

        if in_this[mid] == find_this:
            return mid
        elif in_this[mid] < find_this:
            low = mid + 1
        else:
            high = mid
        
        if high <= low:
            break

    return -1


# Part 2: 
# find a contiguous set of at least two numbers in your
# list which sum to the invalid number from step 1. Add the
# largest and smallest numbers in the list.
def part2(bad_number, xmas_code):
    # There are more efficient ways to do this but this is fast
    # enough on the input data.
    for low_index in range(0, len(xmas_code) - 1):
        total = xmas_code[low_index]
        for high_index in range(low_index + 1, len(xmas_code)):
            total += xmas_code[high_index]
            if total == bad_number:
                print("found it, {} to {}".format(low_index, high_index))
                sub_range = sorted(xmas_code[low_index:high_index])
                return sub_range[0] + sub_range[-1]
            elif total > bad_number:
                # too big
                break
                
    raise RuntimeError("Could not find answer")

xmas_code = read_input()
part1_answer = part1(xmas_code)
print("Part 1: first bad number in list: {}".format(part1_answer))
print("Part 2: weakness is {}".format(part2(part1_answer, xmas_code)))
 