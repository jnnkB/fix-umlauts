import sys
import itertools

with open(sys.argv[2], "r") as f:
    text = f.read()

print(text)

for front_char, back_char in itertools.product([" ", ".", ""], repeat=2):
    with open(sys.argv[1], "r") as f2:
        for line in f2.readlines():
            if ";" in line:
                i, j = line[:-1].split(";")
                if front_char + i + back_char in text:
                    text = text.replace(
                        front_char + i + back_char, front_char + j + back_char
                    )
                    print("replaced", i, j)
        f2.seek(0)

with open(sys.argv[2], "w") as f:
    f.write(text)
