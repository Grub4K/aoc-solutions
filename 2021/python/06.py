from collections import Counter

with open("../input/06.txt") as file:
    line = file.readline()

counter_dict = Counter(map(int, line.split(",")))
fish_counter = [counter_dict.get(index, 0) for index in range(9)]


from_ = 0
to = 6

for _ in range(80):
    to = (to + 1) % 9
    fish_counter[to] += fish_counter[from_]
    from_ = (from_ + 1) % 9

print(sum(fish_counter))


for _ in range(256 - 80):
    to = (to + 1) % 9
    fish_counter[to] += fish_counter[from_]
    from_ = (from_ + 1) % 9

print(sum(fish_counter))
