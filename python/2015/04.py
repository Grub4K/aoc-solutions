from hashlib import md5
from itertools import count


def run(input_data):
    secret = input_data[0].encode()

    found_five = False
    for number in count():
        data = secret + str(number).encode()
        digest = md5(data).hexdigest()
        if not found_five and digest.startswith("00000"):
            found_five = True
            yield number

        if digest.startswith("000000"):
            yield number
            return
