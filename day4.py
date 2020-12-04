import re

with open('day4_input.txt') as inputFile:
    Lines = inputFile.readlines() 

# parse the input data into individual records
unparsedEntries = []
currentEntry = ""
for line in Lines:
    currentLine = line.strip()
    if currentLine == "":
        unparsedEntries.append(currentEntry.strip())
        currentEntry = ""
    else:
        currentEntry += " " + currentLine

if len(currentEntry) > 0:
    unparsedEntries.append(currentEntry.strip())

requiredEntries = set({"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"})
validForPart1 = []
for currentEntry in unparsedEntries:
    parsedEntries = {k:v for k, v in map(lambda x: x.split(":"), currentEntry.split(" "))}
    if {k for k in parsedEntries.keys()}.issuperset(requiredEntries):
        validForPart1.append(parsedEntries)

print("Number of valid entries for part 1 is: {}".format(len(validForPart1)))

# part 2 - add validation. How tedious.
# byr (Birth Year) - four digits; at least 1920 and at most 2002.
# iyr (Issue Year) - four digits; at least 2010 and at most 2020.
# eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
# hgt (Height) - a number followed by either cm or in:
# If cm, the number must be at least 150 and at most 193.
# If in, the number must be at least 59 and at most 76.
# hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
# ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
# pid (Passport ID) - a nine-digit number, including leading zeroes.

isNumberPattern = re.compile(r"\d+")
isHexPattern = re.compile(r"#[0-9a-f]{6}")
numValid = 0
allowedEyeColors = {"amb", "blu", "brn", "gry", "grn", "hzl", "oth"}

def isValidNum(inputStr, minInclusive, maxInclusive, requiredDigits):
    if len(inputStr) != requiredDigits:
        return False
    if isNumberPattern.match(inputStr):
        parsedNum = int(inputStr)
        if minInclusive != None and maxInclusive != None:
            return parsedNum >= minInclusive and parsedNum <= maxInclusive
        else:
            return True
    return False

for entry in validForPart1:
    if not isValidNum(entry["byr"], 1920, 2002, 4):
        print("Invalid birth year " + entry["byr"])
        continue
    if not isValidNum(entry["iyr"], 2010, 2020, 4):
        print("Invalid issue year " + entry["iyr"])
        continue
    if not isValidNum(entry["eyr"], 2020, 2030, 4):
        print("Invalid expiry year " + entry["eyr"])
        continue

    height = entry["hgt"]
    if not height.endswith("in") and not height.endswith("cm"):
        print("Invalid height " + height)
        continue
    elif height.endswith("cm") and not isValidNum(height[:-2], 150, 193, 3):
        print("Invalid height " + height)
        continue
    elif height.endswith("in") and not isValidNum(height[:-2], 59, 76, 2):
        print("Invalid height " + height)
        continue

    if not isHexPattern.match(entry["hcl"]):
        print("Invalid hair color " + entry["hcl"])
        continue
    if entry["ecl"] not in allowedEyeColors:
        print("Invalid eye color " + entry["ecl"])
        continue
    if not isValidNum(entry["pid"], None, None, 9):
        print("Invalid passport ID " + entry["pid"])
        continue
    numValid += 1

print("Number of valid entries for part 2 is: {}".format(numValid))
