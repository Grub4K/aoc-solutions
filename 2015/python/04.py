from hashlib import md5
from itertools import count

with open("../input/04.txt") as file:
    secret = file.read().strip()

found_five = False
for number in count():
    data = f"{secret}{number}".encode()
    digest = md5(data).hexdigest()
    if not found_five and digest.startswith("00000"):
        found_five = True
        print(number)

    if digest.startswith("000000"):
        print(number)
        break
