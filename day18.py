from functools import reduce

def read_input(file_name):
    with open(file_name) as input_file:
        return input_file.readlines()

EOF = -1
NUM = 0
OP = 1
EXPRESSION = 2

PRECEDENCE_ORDER = 0
PRECEDENCE_PLUS = 1

def part1(expressions):
    return reduce(lambda x, y: x+y, map(lambda x:evaluate_expression(x, PRECEDENCE_ORDER), expressions))

def part2(expressions):
    return reduce(lambda x, y: x+y, map(lambda x:evaluate_expression(x, PRECEDENCE_PLUS), expressions))

def evaluate_expression(expression, precedence):
    # print(expression)

    vals = []
    ops = []

    (val, token_type, offset) = find_next_token(expression, 0)
    while token_type != EOF:
        if token_type == EXPRESSION:
            val = evaluate_expression(val, precedence)
            vals.append(val)
        elif token_type == NUM:
            vals.append(val)
        else:
            ops.append(val)
        (val, token_type, offset) = find_next_token(expression, offset)

    # This code is not the least bit resilient to bad input.

    #print(vals)
    #print(ops)
    if precedence == PRECEDENCE_ORDER:
        current = vals[0]
        for i in range(len(ops)):
            if ops[i] == "+":
                current += vals[i+1]
            elif ops[i] == "*":
                current *= vals[i+1]
            else:
                raise RuntimeError("oops")
        return current
    elif precedence == PRECEDENCE_PLUS:
        # treat ops and vals like a stack, only really inefficiently
        s = None
        i = 0
        while True:
            if i >= len(ops): break

            if ops[i] == "+":
                s = vals[i] + vals[i+1]
                # gotta love python's consistency - list length is a stand-alone function,
                # addition is a method, and removal is an operator
                del vals[i]
                del ops[i]
                vals[i] = s
            else:
                i += 1
        return reduce(lambda x,y:x*y, vals)

    return 0

def find_next_token(expression, offset):
    while offset < len(expression) and expression[offset].isspace():
        offset += 1
    if offset == len(expression):
        return (None, EOF, 0)
    
    if expression[offset].isdigit():
        start_offset = offset
        while offset < len(expression) and expression[offset].isdigit():
            offset += 1
        return (int(expression[start_offset:offset]), NUM, offset)
    elif expression[offset] == "+" or expression[offset] == "*":
        return (expression[offset], OP, offset + 1)
    elif expression[offset] == "(":
        offset += 1
        start_offset = offset
        depth = 1
        while depth > 0:
            if expression[offset] == "(": depth +=1
            elif expression[offset] == ")": depth -=1
            offset += 1

        return (expression[start_offset:offset-1], EXPRESSION, offset)

    return (None, EOF, 0)

print(evaluate_expression("1 + 2 * 3 + 4 * 5 + 6", PRECEDENCE_ORDER))
print(evaluate_expression("1 + 2 * 3 + 4 * 5 + 6", PRECEDENCE_PLUS))
print(evaluate_expression("1 + (2 * 3) + (4 * (5 + 6))", PRECEDENCE_PLUS))

expressions = read_input('day18_input.txt')

part1_answer = part1(expressions)
print(f"Part 1: {part1_answer}")
# My answer to part 1: 8298263963837
part2_answer = part2(expressions)
print(f"Part 2: {part2_answer}")
# # My answer to part 2: 145575710203332
