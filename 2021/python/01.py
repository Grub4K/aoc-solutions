try:
    from itertools import pairwise
except ImportError:
    # for py <3.10
    def pairwise(iterable):
        return nwise(iterable, 2)
from itertools import tee



def nwise(iterable, n):
    iterators = list(map(iter, tee(iterable, n)))

    for count, iterator in enumerate(iterators):
        for _ in range(count):
            next(iterator)

    return zip(*iterators)


def process_data(data, grouplength):
    sum_of_n = list(map(sum, nwise(data, grouplength)))

    count = 0
    for first, second in pairwise(sum_of_n):
        if second > first:
            count += 1

    return count


with open('../input/01.txt') as file:
    data = list(map(int, file))

print(process_data(data, 1))
print(process_data(data, 3))
