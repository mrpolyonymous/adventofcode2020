from functools import reduce

class Rule:
    def __init__(self, id, rule):
        self.id = id
        self.rule = rule
        if len(rule) == 1:
            self.is_resolved = True
            self.min_length = 1
            self.max_length = 1
            self.sub_rule_groups = None
        else:
            self.is_resolved = False
            self.min_length = 100000
            self.max_length = 0


    def __str__(self):
        return f"{self.id}: {self.rule}"

    def __repr__(self):
        return f"{self.id}: {self.rule}"

    def try_resolve(self, all_rules):
        if self.is_resolved:
            return True

        self.sub_rule_groups = []
        has_loops = False
        for sub_rule_group in self.rule.split(" | "):
            sub_rules = []
            for sub_rule_id in sub_rule_group.split(" "):
                sub_rule = all_rules[sub_rule_id]
                if not sub_rule.is_resolved:
                    if sub_rule == self:
                        has_loops = True
                    else:
                        return False
                sub_rules.append(sub_rule)
            self.sub_rule_groups.append(sub_rules)

        min_length = 111111111
        max_length = -1

        # Something bigger than any input
        if has_loops:
            self.max_length = 1000000

        for sub_rule_group in self.sub_rule_groups:
            min_group_length = 0
            max_group_length = 0
            for sub_rule in sub_rule_group:
                min_group_length += sub_rule.min_length
                max_group_length += sub_rule.max_length
            min_length = min(min_group_length, min_length)
            max_length = max(max_group_length, max_length)

        self.is_resolved = True
        self.min_length = min_length
        self.max_length = max_length
        return True
        
    def matches(self, message):
        if self.sub_rule_groups == None:
            return message == self.rule
        if len(message) < self.min_length or len(message) > self.max_length:
            return False

        for sub_rule_group in self.sub_rule_groups:
            if len(sub_rule_group) == 1:
                if sub_rule_group[0].matches(message):
                    return True
            elif len(sub_rule_group) == 2:
                for i in range(sub_rule_group[0].min_length, min(sub_rule_group[0].max_length + 1, len(message))):

                    sub_rule_group_matches = sub_rule_group[0].matches(message[0:i])
                    if sub_rule_group_matches:
                        sub_rule_group_matches = sub_rule_group[1].matches(message[i:])
                    if sub_rule_group_matches:
                        return True
            elif len(sub_rule_group) == 3:
                i_min = sub_rule_group[0].min_length
                i_max = min(sub_rule_group[0].max_length + 1, len(message))
                for i in range(i_min, i_max):
                    first_group_matches = sub_rule_group[0].matches(message[0:i])
                    if first_group_matches:
                        j_min = i + sub_rule_group[1].min_length
                        j_max = len(message) - sub_rule_group[2].min_length + 1
                        for j in range(j_min, j_max):

                            sub_rule_group_matches = sub_rule_group[1].matches(message[i:j])
                            if sub_rule_group_matches:
                                sub_rule_group_matches = sub_rule_group[2].matches(message[j:])
                            if sub_rule_group_matches:
                                return True

            else:
                raise RuntimeError("I wasnt made for this")
        return False


def read_input(file_name):
    reading_rules = True
    rules = dict()
    messages = []
    with open(file_name) as input_file:
        for line in input_file:
            line = line.strip()
            if len(line) == 0:
                reading_rules = False
            elif reading_rules:
                p = line.split(": ")
                if p[1][0] == "\"":
                    rules[p[0]] = Rule(p[0], p[1][1])
                else:
                    rules[p[0]] = Rule(p[0], p[1])
            else:
                messages.append(line)

    return (rules, messages)

def resolve_rules(rules):
    while True:
        all_resolved = True
        for rule in rules.values():
            rule.try_resolve(rules)
            all_resolved &= rule.is_resolved
        if all_resolved:
            break

def part1(rules, messages):
    num = 0
    rule0 = rules["0"]
    for message in messages:
        # print(f"Testing message {message}")
        if rule0.matches(message):
            num += 1
    return num

# Fun but will run out of memory and won't work for part 2
def expand_rule(rules, rule_id):
    rule = rules[rule_id]
    if len(rule) == 1:
        return [rule]

    expanded = []
    for sub_rule in rule.split(" | "):
        sub_expanded = []
        for sub_rule_id in sub_rule.split(" "):
            if len(sub_expanded) == 0:
                sub_expanded = expand_rule(rules, sub_rule_id)
            else:
                new_sub = expand_rule(rules, sub_rule_id)
                ns = []
                for s in sub_expanded:
                    for n in new_sub:
                        ns.append(s + n)
                sub_expanded = ns

            
        expanded += sub_expanded

    return expanded

(rules, messages) = read_input('day19_input.txt')

# (rules, messages) = read_input('day19_example2_input.txt')
resolve_rules(rules)
print(rules)
print(messages)

part1_answer = part1(rules, messages)
print(f"Part 1: {part1_answer}")
# My answer to part 1: 142

(rules, messages) = read_input('day19_input.txt')
rule8 = Rule("8", "42 | 42 8")
rule11 = Rule("11", "42 31 | 42 11 31")
rules["8"] = rule8
rules["11"] = rule11
resolve_rules(rules)
part2_answer = part1(rules, messages)
print(f"Part 2: {part2_answer}")
# My answer to part 2: 294
