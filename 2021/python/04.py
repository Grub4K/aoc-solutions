with open('../input/04.txt') as file:
    draws, *data = file

def grouped(iterable, n):
    return zip(*[iter(iterable)]*n)

def is_winning(board, drawn):
    lines = (*grouped(board, 5), *zip(*grouped(board, 5)))
    return any(
        all(number in drawn for number in line)
        for line in lines
    )

draws = list(map(int, draws.split(',')))

boards = [
    [*map(int, ' '.join(data).split())]
    for data in grouped(data, 6)
]

drawn = set()
win_values = []
for draw in draws:
    if not boards:
        break
    drawn.add(draw)
    for board in boards:
        if is_winning(board, drawn):
            board_without_drawn = {*board} -drawn
            board_value = sum(board_without_drawn) * draw
            win_values.append(board_value)
            boards.remove(board)

print(win_values[0])
print(win_values[-1])
