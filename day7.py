import re

# return a map from color->list of contents and the inverse map
# of color -> what contains it
def read_input():
    # example lines:
    # shiny aqua bags contain 2 vibrant black bags, 2 muted coral bags, 4 vibrant coral bags.
    # dotted tomato bags contain no other bags.
    # dim plum bags contain 1 dim chartreuse bag.

    bag_pattern = re.compile(r"^(\d+) (.+) bags?\.?")
    colors_to_contents = dict()
    color_contained_by = dict()
    with open('day7_input.txt') as input_file:
        for line in input_file:
            line = line.strip()
            split_line = line.split(" bags contain ")
            if len(split_line) != 2:
                # sanity check
                raise RuntimeError("Unmatched line: " + line)

            containing_color = split_line[0]
            contents_for_color = []
            if split_line[1] == "no other bags.":
                # print("empty")
                None
            else:
                for content in split_line[1].split(", "):
                    m = bag_pattern.match(content)
                    contained_color = m.group(2)
                    contents_for_color.append( (int(m.group(1)), contained_color) )

                    if contained_color in color_contained_by:
                        color_contained_by[contained_color].add(containing_color)
                    else:
                        color_contained_by[contained_color] = {containing_color}

            colors_to_contents[containing_color] = contents_for_color

    return (colors_to_contents, color_contained_by)

# How many bag colors can eventually contain at least one shiny gold bag?
def part1(contained_by):
    can_contain_gold = set()
    find_set = {"shiny gold"}
    new_find_set = set()

    while True:
        for find_color in find_set:
            can_contain_gold.add(find_color)
            if find_color in contained_by:
                containers = contained_by[find_color]

                for containing_color in containers:
                    if not containing_color in can_contain_gold:
                        can_contain_gold.add(containing_color)
                        new_find_set.add(containing_color)

        find_set = new_find_set
        new_find_set = set()

        if len(find_set) == 0:
            break

    # Minus one to subtract "shiny gold"
    return len(can_contain_gold) - 1

# Part 2: How many individual bags are required inside your single shiny gold bag?
def part2(colors_to_contents):
    return bag_count(colors_to_contents, "shiny gold") - 1

def bag_count(colors_to_contents, bag_color):
    size = 1 # 1 for the current bag
    contained_in_bag = colors_to_contents[bag_color]
    for bag_num_and_color in contained_in_bag:
        size += bag_num_and_color[0] * bag_count(colors_to_contents, bag_num_and_color[1])
    return size

color_maps = read_input()
colors_to_contents = color_maps[0]
contained_by = color_maps[1]
print("Part 1: how many colors can contain shiny gold?: {}".format(part1(contained_by)))
print("Part 2: number of other bags required={}".format(part2(colors_to_contents)))
