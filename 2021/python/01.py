def nwise(iterable, n):
    iterable = list(iterable)
    return (tuple(iterable[i:i+n])
        for i in range(len(iterable) - n + 1))


def process_data(data, grouplength):
    sum_of_n = list(map(sum, nwise(data, grouplength)))

    count = 0
    for first, second in nwise(sum_of_n, 2):
        if second > first:
            count += 1

    return count


with open('../input/01.txt') as file:
    data = list(map(int, file))

print(process_data(data, 1))
print(process_data(data, 3))
