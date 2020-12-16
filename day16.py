import re

class InputClass:
    def __init__(self, name, r1_min, r1_max, r2_min, r2_max):
        self.name = str(name)
        self.r1_min = int(r1_min)
        self.r1_max = int(r1_max)
        self.r2_min = int(r2_min)
        self.r2_max = int(r2_max)

    def contains(self, value):
        return (value >= self.r1_min and value <= self.r1_max) \
            or (value >= self.r2_min and value <= self.r2_max)

def read_input(file_name):
    class_pattern = re.compile(r"^(.+): (\d+)-(\d+) or (\d+)-(\d+)")

    input_classes = []
    your_ticket = []
    nearby_tickets = []
    parsing_classes = True
    parsing_my_ticket = False
    parsing_nearby = False

    with open(file_name) as input_file:
        for line in input_file:
            line = line.strip()
            if parsing_classes:
                if len(line) == 0:
                    parsing_classes = False
                    parsing_my_ticket = True
                else:
                    matcher = class_pattern.match(line)
                    ic = InputClass(matcher.group(1), matcher.group(2), matcher.group(3), matcher.group(4), matcher.group(5))
                    input_classes.append(ic)
            elif parsing_my_ticket:
                if len(line) == 0:
                    parsing_my_ticket = False
                    parsing_nearby = True
                elif line != "your ticket:":
                    your_ticket = list(map(int, line.split(",")))
            elif parsing_nearby:
                if len(line) == 0:
                    parsing_nearby = False
                    break
                elif line != "nearby tickets:":
                    nearby_tickets.append(list(map(int, line.split(","))))


    return (input_classes, your_ticket, nearby_tickets)

def part1(input_classes, your_ticket, nearby_tickets):
    valid_anywhere = set()
    for input_class in input_classes:
        for i in range(input_class.r1_min, input_class.r1_max+1):
            valid_anywhere.add(i)
        for i in range(input_class.r2_min, input_class.r2_max+1):
            valid_anywhere.add(i)

    scanning_error = 0
    valid_tickets = []
    valid_tickets.append(your_ticket)
    for ticket in nearby_tickets:
        is_valid = True
        for val in ticket:
            if not val in valid_anywhere:
                scanning_error += val
                is_valid = False
        if is_valid: valid_tickets.append(ticket)

    return (scanning_error, valid_tickets)

def part2(input_classes, your_ticket, valid_tickets):
    # figure out what positions correspond to which input classes
    num_classes = len(input_classes)
    possibilites = [set() for x in range(num_classes)]
    for i in range(num_classes):
        for j in range(num_classes):
            possibilites[i].add(input_classes[j].name)

    # Eliminate impossible values
    for ticket in valid_tickets:
        for col in range(num_classes):
            ticket_value = ticket[col]
            for input_class in input_classes:
                if not input_class.contains(ticket_value):
                    if input_class.name in possibilites[col]:
                        possibilites[col].remove(input_class.name)

    # Now use the classes where there is only 1 possibility to hopefully find the real classes
    actuals = [None for i in range(num_classes)]
    changes = True
    while changes:
        changes = False
        for i in range(num_classes):
            if len(possibilites[i]) == 1:
                changes = True
                actual = possibilites[i].pop()
                actuals[i] = actual
                for j in range(num_classes):
                    if i != j and actual in possibilites[j]:
                        possibilites[j].remove(actual)


    product = 1
    for i in range(num_classes):
        if actuals[i].startswith("departure"):
            product *= your_ticket[i]
    return product


(input_classes, your_ticket, nearby_tickets) = read_input('day16_input.txt')
#(input_classes, your_ticket, nearby_tickets) = read_input('day16_example2_input.txt')

part1_answer = part1(input_classes, your_ticket, nearby_tickets)
print("Part 1: {}".format(part1_answer[0]))
# My answer to part 1: 26980
part2_answer = part2(input_classes, your_ticket, part1_answer[1])
print("Part 2: {}".format(part2_answer))
# My answer to part 2: 3021381607403
