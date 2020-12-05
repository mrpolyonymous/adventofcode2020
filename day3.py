import pandas

# 1 column of strings
df = pandas.read_csv("day3_input.txt", sep=" ", header=None)
# print(df)

numTrees = 0
offset = 0
started = False
for row in df[0]:
    if started:
        if row[offset] == "#":
            numTrees += 1
    started = True
    offset = (offset + 3) % len(row)

print(f"Number of trees hit for part 1: {numTrees}")

# Part 2
# Determine the number of trees you would encounter if, for each of the
# following slopes, you start at the top-left corner and traverse the
# map all the way to the bottom:
# Right 1, down 1.
# Right 3, down 1. (This is the slope you already checked.)
# Right 5, down 1.
# Right 7, down 1.
# Right 1, down 2.

routes = [[1, 1], [3, 1], [5, 1], [7, 1], [1, 2]]
numTreesPerRoute = []

for route in routes:
    numTrees = 0
    offset = 0
    started = False
    for rowIndex in range(0, len(df[0]), route[1]):
        row = df[0][rowIndex]
        if started:
            if row[offset] == "#":
                numTrees += 1
        started = True
        offset = (offset + route[0]) % len(row)
    numTreesPerRoute.append(numTrees)

product = 1
for num in numTreesPerRoute:
    product *= num    
print(numTreesPerRoute)
print(f"Product of these numbers is: {product}")

