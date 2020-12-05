
def findSeatId(line : str) -> int:
    row = findPosition(line[0:7], "F", "B")
    column = findPosition(line[7:], "L", "R")
    return (row << 3) + column

def findPosition(line : str, goLow: str, goHigh:str) -> int:
    pos = 0
    stride = 1 << (len(line) - 1)
    for c in line:
        if c == goHigh:
            pos += stride
        stride >>= 1
    return pos

    # A slightly more verbose version that is less trusting of the input
    # minInclusive = 0
    # maxExclusive = 1 << len(line)
    # for c in line:
    #     if c == goLow:
    #         maxExclusive -= (maxExclusive - minInclusive) >> 1
    #     elif c == goHigh:
    #         minInclusive += (maxExclusive - minInclusive) >> 1
    #     else:
    #         raise RuntimeError("Invalid character")
    # return minInclusive

def part1():
    maxSeatId = -1
    idToInt = dict()
    with open('day5_input.txt') as input_file:
        for line in input_file:
            line = line.strip()
            if len(line) == 10:
                seatId = findSeatId(line)
                idToInt[line] = seatId
                maxSeatId = max(maxSeatId, seatId)

    return (maxSeatId, idToInt)

def part2(idToInt):
    usedSeatIds = [v for v in idToInt.values()]
    usedSeatIds.sort()
    for i in range(0, len(usedSeatIds) - 1):
        if usedSeatIds[i+1] != usedSeatIds[i] + 1:
            return usedSeatIds[i]+1
    return -1

(maxSeatId, idToInt) = part1()
print("Highest seat ID: {}".format(maxSeatId))
mySeatId = part2(idToInt)
print("My seat ID: {}".format(mySeatId))
