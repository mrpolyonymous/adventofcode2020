# For example, suppose you have the following list:
# 1-3 a: abcde
# 1-3 b: cdefg
# 2-9 c: ccccccccc
# Each line gives the password policy and then the password. 
# The password policy indicates the lowest and highest number of
# times a given letter must appear for the password to be valid.
# For example, 1-3 a means that the password must contain a at
# least 1 time and at most 3 times.

import pandas

# 3 columns: range, required character, password
df = pandas.read_csv("day2_input.txt", sep=" ", header=None)
# print(df)
ranges = df[0].str.split("-")
requiredCharacter=df[1].str[0]
passwords=df[2]

numValid = 0
for i in range(0, len(passwords)):
    low=int(ranges[i][0])
    high=int(ranges[i][1])
    occurrences = passwords[i].count(requiredCharacter[i])
    if occurrences >= low and occurrences <= high:
        numValid += 1

print("Number of valid passwords for part 1: {}".format(numValid))

# Part 2
# Each policy actually describes two positions in the password, where
# 1 means the first character, 2 means the second character, and so on.
# Exactly one of these positions must contain the given letter.
# Other occurrences of the letter are irrelevant for the purposes
# of policy enforcement.
#
# Examples:
# 1-3 a: abcde is valid: position 1 contains a and position 3 does not.
# 1-3 b: cdefg is invalid: neither position 1 nor position 3 contains b.
# 2-9 c: ccccccccc is invalid: both position 2 and position 9 contain c.
# How many passwords are valid according to the new interpretation of the policies?
numValid = 0

for i in range(0, len(passwords)):
    lowIndex = int(ranges[i][0]) - 1
    highIndex = int(ranges[i][1]) - 1

    passwordToTest = passwords[i]
    if (passwordToTest[lowIndex] == requiredCharacter[i] or passwordToTest[highIndex] == requiredCharacter[i]) and passwordToTest[lowIndex] != passwordToTest[highIndex]:
        numValid += 1

print("Number of valid passwords for part 2: {}".format(numValid))
