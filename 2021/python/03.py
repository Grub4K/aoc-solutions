from itertools import groupby



with open('../input/03.txt') as file:
    data = list(file)


number_of_bits = len(data[0]) - 1
number_of_items = len(data)
threshold = number_of_items // 2

counts = list(map(sum, map(lambda x: map(int, x), zip(*data))))

accumulator = 0
additor = 1 << number_of_bits
for count in counts:
    additor >>= 1
    if count > threshold:
        accumulator += additor

bitmask = (1 << number_of_bits) - 1
print(accumulator * (~accumulator & bitmask))

def filter_data(data, is_co2=False):
    predicate_one = lambda item: item[position] == '1'
    predicate_zero = lambda item: item[position] == '0'
    filtered_data = data.copy()

    for position in range(number_of_bits):
        count_one = sum(map(predicate_one, filtered_data))
        count_zero = len(filtered_data) - count_one

        predicate = (count_one >= count_zero) ^ is_co2
        if predicate:
            filtered_data = [*filter(predicate_one, filtered_data)]
        else:
            filtered_data = [*filter(predicate_zero, filtered_data)]

        if len(filtered_data) == 1:
            break

    return int(filtered_data[0], 2)

oxygen, co2 = filter_data(data), filter_data(data, is_co2=True)
print(oxygen * co2)
