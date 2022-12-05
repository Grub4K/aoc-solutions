def process_line(line):
    LOOKUP = {"A": 0, "B": 1, "C": 2, "X": 0, "Y": 1, "Z": 2}

    a, _, b = line.partition(" ")
    return LOOKUP[a], LOOKUP[b]


def get_result(own_hand, other_hand):
    return (own_hand - other_hand + 1) % 3


def get_own_hand(other_hand, result):
    return (result + other_hand - 1) % 3


def run(moves):
    yield sum(
        (own_hand + 1) + (get_result(own_hand, other_hand) * 3)
        for other_hand, own_hand in moves
    )

    yield sum(
        (get_own_hand(other_hand, result) + 1) + (result * 3)
        for other_hand, result in moves
    )
