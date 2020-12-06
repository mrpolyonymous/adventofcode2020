
def read_input():
    answer_groups = []
    answers_for_group = []
    with open('day6_input.txt') as input_file:
        for line in input_file:
            line = line.strip()
            if len(line) == 0:
                answer_groups.append(answers_for_group)
                answers_for_group = []
            else:
                answers_for_group.append(line)

    if len(answers_for_group) > 0:
        answer_groups.append(answers_for_group)

    return answer_groups

# For each group, count the number of questions to which anyone answered "yes".
# What is the sum of those counts?
def part1(answer_groups):
    yes_for_any_answers = 0
    for answer_group in answer_groups:
        answered_by_any = set()
        for answer in answer_group:
            for char in answer:
                answered_by_any.add(char)
        yes_for_any_answers += len(answered_by_any)
    return yes_for_any_answers

# Part 2: do it again, but now only count for groups where each entry gave an answer
def part2(answer_groups):
    yes_for_all_answers = 0
    for answer_group in answer_groups:
        answered_by_all = {c for c in answer_group[0]}
        for i in range(1, len(answer_group)):
            answered_by_all = answered_by_all.intersection({c for c in answer_group[i]})
        yes_for_all_answers += len(answered_by_all)
    return yes_for_all_answers

answer_groups = read_input()
print("Part 1: sum of counts where any person answered yes: {}".format(part1(answer_groups)))
print("Part 2: sum of counts where all people answered yes: {}".format(part2(answer_groups)))
