def read_input(file_name):
    instructions = []
    with open(file_name) as input_file:
        for line in input_file:
            line = line.strip()
            instructions.append( (line[0:1], int(line[1:])) )

    return instructions

# Figure out where the navigation instructions lead.
# What is the Manhattan distance between that location and the ship's starting position?
def part1(instructions):
    direction = 0
    east_west_offset = 0 # east = +1, west = -1
    north_south_offset = 0 # north = +1, south = -1
    for instruction in instructions:
        command = instruction[0]
        amount = instruction[1]
        if command == "N":
            north_south_offset += amount
        elif command == "S":
            north_south_offset -= amount
        elif command == "E":
            east_west_offset += amount
        elif command == "W":
            east_west_offset -= amount
        elif command == "L":
            direction -= int(amount / 90)
            direction = direction % 4
        elif command == "R":
            direction += int(amount / 90)
            direction = direction % 4
        elif command == "F":
            if direction == 0:
                east_west_offset += amount
            elif direction == 1:
                north_south_offset -= amount
            elif direction == 2:
                east_west_offset -= amount
            else:
                north_south_offset += amount
        else:
            raise RuntimeError("Unhandled case")

    return abs(east_west_offset) + abs(north_south_offset)

# a bunch of complicated nonsense about moving waypoints
def part2(instructions):
    rotation_amount = 0
    waypoint_x = 10 # 10 East
    waypoint_y = 1 # 1 North
    ship_x = 0
    ship_y = 0
    for instruction in instructions:
        command = instruction[0]
        amount = instruction[1]
        if command == "N":
            waypoint_y += amount
        elif command == "S":
            waypoint_y -= amount
        elif command == "E":
            waypoint_x += amount
        elif command == "W":
            waypoint_x -= amount
        elif command == "L" or command == "R":
            if command == "L":
                amount = 360 - amount
            rotation_amount = int(amount / 90) % 4
            if rotation_amount == 1:
                tmp = waypoint_x
                waypoint_x = waypoint_y
                waypoint_y = -tmp
            elif rotation_amount == 2:
                waypoint_x = -waypoint_x
                waypoint_y = -waypoint_y
            elif rotation_amount == 3:
                tmp = waypoint_x
                waypoint_x = -waypoint_y
                waypoint_y = tmp
            else:
                raise RuntimeError("Unhandled case")
        elif command == "F":
            ship_x += waypoint_x * amount
            ship_y += waypoint_y * amount
        else:
            raise RuntimeError("Unhandled case")

    return abs(ship_x) + abs(ship_y)


instructions = read_input('day12_input.txt')

part1_answer = part1(instructions)
print("Part 1: {}".format(part1_answer))
part2_answer = part2(instructions)
print("Part 2: {}".format(part2_answer))
