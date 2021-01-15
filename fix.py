import sys
import itertools
import csv


def read_word_list(csvfile):
    reader = csv.reader(csvfile, delimiter=";", quotechar='"')
    return list(reader)


def replace_words(text, word_list):
    # These front and back chars try to ensure that if possible whole words are replaced.
    for front_char, back_char in itertools.product([" ", ".", ""], repeat=2):
        for fixed_word, encoding_error_word in word_list:
            fixed_string = front_char + encoding_error_word + back_char
            if fixed_string in text:
                encoding_error_string = front_char + fixed_word + back_char
                text = text.replace(
                    fixed_string,
                    encoding_error_string,
                )
                print(f"replaced '{encoding_error_string}' with '{fixed_string}'")
    return text


if __name__ == "__main__":
    with open(sys.argv[2], "r") as f:
        text = f.read()

    with open(sys.argv[1], "r") as csvfile:
        word_list = read_word_list(csvfile)

    text = replace_words(text, word_list)

    with open(sys.argv[2], "w") as f:
        f.write(text)
