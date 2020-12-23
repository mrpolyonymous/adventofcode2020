import datetime
import time

class Node:
    def __init__(self, val):
        self.val = val
        self.next = None

    def __str__(self):
        return str(self.val)

    def __repr__(self):
        return str(self.val)


class NodeRing:
    def __init__(self, values_in_order, max_value):
        self.value_lookup = [None for i in range(max_value+1)]
        self.max_value = max_value

        root_node = Node(values_in_order[0])
        self.value_lookup[values_in_order[0]] = root_node
        prev_node = current_node = root_node
        for i in range(1, len(values_in_order)):
            current_node = Node(values_in_order[i])
            prev_node.next = current_node

            prev_node = current_node
            self.value_lookup[values_in_order[i]] = current_node
        current_node.next = root_node

        self.current_root = root_node

    def __str__(self):
        if self.current_root == None:
            return "Empty"
        
        i = 0
        node = self.current_root
        s = str(node.val) + "->"
        while i <= len(self.value_lookup) and i < 10:
            i+=1
            if node.next == None:
                s = s + "End"
                break
            node = node.next
            if node == self.current_root:
                s = s+"Back to start"
                break
            s = s + str(node.val) + "->"
        return s

    def __repr__(self):
        return self.__str__()


def read_input(file_name):
    with open(file_name) as input_file:
        for line in input_file:
            return line.strip()

def part1(input):
    cups = list(map(lambda x: int(x), input))
    # cups = play_game_naive(cups, 100)
    # one_idx = cups.index(1)
    # return "".join(map(lambda x:str(x), cups[one_idx+1:] + cups[:one_idx]))
    cup_ring = play_game(cups, 100)
    one_node = cup_ring.value_lookup[1]
    s = ""
    node = one_node.next
    while node != one_node:
        s += str(node.val)
        node = node.next
    return s

# Works for part 1 but it's inefficient as heck and can't handle part 2 
def play_game_naive(cups, iterations):
    num_cups = len(cups)
    min_cup = min(cups)
    max_cup = max(cups)
    cup_offset = 0
    transient_cups = []
    for iter in range(iterations):
        current_cup = cups[cup_offset]

        if cup_offset < num_cups - 3:
            transient_cups = cups[cup_offset+1:cup_offset+4]
        elif cup_offset == num_cups - 3:
            transient_cups = cups[-2:] + cups[0:1]
        elif cup_offset == num_cups - 2:
            transient_cups = cups[-1:] + cups[0:2]
        elif cup_offset == num_cups - 1:
            transient_cups = cups[0:3]

        # print(f"move {iter+1}, cups={cups}, offset={cup_offset}, cup={current_cup}, pick up={transient_cups}")
        print(f"move {iter+1}, offset={cup_offset}, cup={current_cup}, pick up={transient_cups}")
        for c in transient_cups: cups.remove(c)

        cup_offset = cups.index(current_cup)
        next_cup_clockwise = cups[(cup_offset + 1) % (num_cups-3)]

        destination_cup = current_cup - 1
        if destination_cup < min_cup: destination_cup = max_cup
        while destination_cup in transient_cups:
            destination_cup -= 1
            if destination_cup < min_cup: destination_cup = max_cup

        destination_offset = cups.index(destination_cup) + 1
        cups = cups[0:destination_offset] + transient_cups + cups[destination_offset:]

        cup_offset = cups.index(next_cup_clockwise)

    return cups

def part2(input):
    cups = list(map(lambda x: int(x), input))
    desired_num_cups = 1000000
    max_cup = max(cups)
    while len(cups) < desired_num_cups:
        max_cup += 1
        cups.append(max_cup)

    cup_ring = play_game(cups, 10000000)

    one_node = cup_ring.value_lookup[1]
    return one_node.next.val * one_node.next.next.val

def play_game(cups, iterations):
    min_cup = 1         # min(cups)
    max_cup = len(cups) # max(cups)

    print("Make node ring")
    cup_ring = NodeRing(cups, max_cup)
    print("Node ring made")

    iter = 0
    while iter < iterations:
        iter += 1

        # current_cup_id = cup_ring.current_root.val
        first_pickup_node = cup_ring.current_root.next
        last_pickup_node = first_pickup_node.next.next
        next_cup_node_clockwise = last_pickup_node.next
        banned_id_1 = first_pickup_node.val
        banned_id_2 = first_pickup_node.next.val
        banned_id_3 = last_pickup_node.val

        destination_cup_id = cup_ring.current_root.val - 1
        if destination_cup_id < min_cup: destination_cup_id = max_cup
        while destination_cup_id == banned_id_1 or destination_cup_id == banned_id_2 or destination_cup_id == banned_id_3:
            destination_cup_id -= 1
            if destination_cup_id < min_cup: destination_cup_id = max_cup

        destination_cup_node = cup_ring.value_lookup[destination_cup_id]
        current_next_node = destination_cup_node.next
        destination_cup_node.next = first_pickup_node
        last_pickup_node.next = current_next_node

        cup_ring.current_root.next = next_cup_node_clockwise
        cup_ring.current_root = cup_ring.current_root.next

    return cup_ring


input = read_input('day23_input.txt')
# example:
# input = "389125467"

part1_answer = part1(input)
print(f"Part 1: {part1_answer}")
# My answer to part 1: 89372645
p2_start = time.time()
part2_answer = part2(input)
print(f"Part 2: {part2_answer}")
# My answer to part 2: 21273394210
p2_end = time.time()
p2_duration = p2_end - p2_start
print(f"Part 2 duration: {p2_duration}")
# Best duration: 18.0s (worst, before changes: 29.4s)
