import argparse
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


def parse_args():
    parser = argparse.ArgumentParser(
        description="Fix missing umlauts that occurred do to encoding errors "
    )
    parser.add_argument(
        "csv_file",
        type=str,
        help="the CSV file to use for fixing",
    )
    parser.add_argument(
        "file_to_fix",
        type=str,
        help="the file that should be fixed",
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    with open(args.file_to_fix, "r") as f:
        text = f.read()

    with open(args.csv_file, "r") as csvfile:
        word_list = read_word_list(csvfile)

    text = replace_words(text, word_list)

    with open(args.file_to_fix, "w") as f:
        f.write(text)
