def read_input(file_name):
    player1 = []
    player2 = []
    add_to = player1
    with open(file_name) as input_file:
        for line in input_file:
            line = line.strip()
            if len(line) == 0:
                add_to = player2
            elif not line.startswith("Player"):
                add_to.append(int(line))

    print(player1)
    print(player2)
    return (player1, player2)

def part1(player1, player2):
    player1_deck = player1.copy()
    player2_deck = player2.copy()

    while len(player1_deck) > 0 and len(player2_deck) > 0:
        p1 = player1_deck[0]
        p2 = player2_deck[0]
        del player1_deck[0]
        del player2_deck[0]
        if p1 > p2:
            player1_deck.append(p1)
            player1_deck.append(p2)
        else:
            # no ties, I guess?
            player2_deck.append(p2)
            player2_deck.append(p1)

    if len(player1_deck) > 0:
        return compute_score(player1_deck)
    else:
        return compute_score(player2_deck)        

def compute_score(deck):
    score = 0
    mul = 1
    while len(deck) > 0:
        score += mul * deck.pop()
        mul += 1
    return score

def part2(player1, player2):
    (_, winning_deck) = recursive_combat(player1, player2)
    return compute_score(winning_deck)

PLAYER1_WINS = 0
PLAYER2_WINS = 1

def recursive_combat(player1_deck, player2_deck):
    previous_configs = set()
    player1_deck = player1_deck.copy()
    player2_deck = player2_deck.copy()

    while len(player1_deck) > 0 and len(player2_deck) > 0:
        p1_config = ",".join(map(lambda i: str(i), player1_deck))
        p2_config = ",".join(map(lambda i: str(i), player2_deck))
        if p1_config in previous_configs or p2_config in previous_configs:
            return (PLAYER1_WINS, player1_deck)
        previous_configs.add(p1_config)
        previous_configs.add(p2_config)

        p1 = player1_deck[0]
        p2 = player2_deck[0]
        del player1_deck[0]
        del player2_deck[0]
        winner = PLAYER1_WINS
        if len(player1_deck) >= p1 and len(player2_deck) >= p2:
            (winner, _) = recursive_combat(player1_deck[0:p1], player2_deck[0:p2])
        elif p2 > p1:
            winner = PLAYER2_WINS

        if winner == PLAYER1_WINS:
            player1_deck.append(p1)
            player1_deck.append(p2)
        else:
            player2_deck.append(p2)
            player2_deck.append(p1)

    if len(player1_deck) > 0:
        return (PLAYER1_WINS, player1_deck)
    else:
        return (PLAYER2_WINS, player2_deck)        

(player1, player2) = read_input('day22_input.txt')
# (player1, player2) = read_input('day22_example_input.txt')
# print(player1)
# print(player2)

part1_answer = part1(player1, player2)
print(f"Part 1: {part1_answer}")
# My answer to part 1: 32783
part2_answer = part2(player1, player2)
print(f"Part 2: {part2_answer}")
# My answer to part 2: 33455
