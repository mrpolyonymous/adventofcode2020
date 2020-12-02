# Find the two numbers in the file that add to 2020, and multiply them
# Do not forget: pipenv shell

import pandas

numberFile = pandas.read_csv("day1_input.txt", header=None)
print(numberFile)
sortedNumbers=numberFile.sort_values(0, ignore_index=True)[0]

n1 = 0
n2 = 0
for low in range(0, len(sortedNumbers)):
    for high in range(len(sortedNumbers)-1, low+1, -1):
        if sortedNumbers[low] + sortedNumbers[high] == 2020:
            n1 = sortedNumbers[low]
            n2 = sortedNumbers[high]
            break
    if n1 > 0 and n2 > 0:
        break

print("Found answer for part 1: {} + {} = 2020".format(n1, n2))
print("{} * {} = {}".format(n1, n2, n1*n2))

# Part 2: In your expense report, what is the product of the three entries that sum to 2020?
n1 = n2 = n3 = 0
for low in range(0, len(sortedNumbers) - 2):
    n1 = sortedNumbers[low]
    for mid in range(low + 1, len(sortedNumbers) - 1):
        n2 = sortedNumbers[mid]
        remaining = 2020 - (n1 + n2)
        if remaining < 0:
            break
        
        possibleIndex = sortedNumbers.searchsorted(remaining)
        if possibleIndex > 0 and possibleIndex < len(sortedNumbers) and sortedNumbers[possibleIndex] == remaining:
            n3 = remaining
            break

    if n1 > 0 and n2 > 0 and n3 > 0:
        break

print("Found answer for part 2: {} + {} + {} = 2020".format(n1, n2, n3))
print("{} * {} * {} = {}".format(n1, n2, n3, n1*n2*n3))
