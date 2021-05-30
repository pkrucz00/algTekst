import random

with open("testy/random_10kB.txt", "w", encoding="utf-8") as file:
    for _ in range(10):
        file.writelines(''.join(map(str, [chr(random.randint(128, 1000)) for _ in range(500)])))