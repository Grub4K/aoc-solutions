def filter_data(data, bit_count, is_co2=False):
    for bit_offset in reversed(range(bit_count)):
        ones, zeros = [], []
        for number in data:
            if (number >> bit_offset) & 1:
                ones.append(number)
            else:
                zeros.append(number)

        data = ones if (len(ones) >= len(zeros)) ^ is_co2 else zeros
        if len(data) == 1:
            return data[0]

    assert False


def process_data(input_data):
    return [int(line, 2) for line in input_data], len(input_data[0])


def run(input_data):
    data, bit_count = input_data
    threshold = len(data) // 2

    one_counts = [
        sum(1 for number in data if (number >> bit_offset) & 1)
        for bit_offset in reversed(range(bit_count))
    ]
    gamma = epsilon = 0
    for one_count in one_counts:
        gamma <<= 1
        epsilon <<= 1
        if one_count >= threshold:
            gamma += 1
        else:
            epsilon += 1

    yield gamma * epsilon

    oxygen = filter_data(data, bit_count)
    co2 = filter_data(data, bit_count, is_co2=True)
    yield oxygen * co2
