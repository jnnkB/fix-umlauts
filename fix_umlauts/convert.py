import argparse
import csv
import unicodedata
from itertools import chain
from string import punctuation
from zipfile import is_zipfile
from zipfile import ZipFile


def umlaut_variations(umlaut):
    return (
        unicodedata.normalize("NFC", umlaut),
        unicodedata.normalize("NFD", umlaut),
    )


def read_zipfile(source_file):
    with ZipFile(source_file) as myzip:
        possible_files = list(
            filter(lambda x: x.filename.endswith("_frami.dic"), myzip.infolist())
        )

        if len(possible_files) > 1:
            print("There are the following files that good be the dictionary:")
            for i, file in enumerate(possible_files):
                print(f"{i+1}. {file.filename}")
            print("To choose one enter the corresponding number:")
            user_input = input("> ")
            if not (user_input.isdigit()):
                print("Please enter a number.")
                exit(1)
            user_number = int(user_input) - 1

            if user_number < 0 or user_number > len(possible_files):
                print("Please enter a number is the correct range.")
                exit(1)

            dict_file = possible_files[user_number]

        elif len(possible_files) == 1:
            dict_file = possible_files[0]
        else:
            print("No matching file found!")
            exit(1)

        print(f"Using file {dict_file.filename}")

        return myzip.read(dict_file)


def read_file(file_path):
    with open(file_path, "rb") as f:
        return f.read()


def file_content_parser(file_content):
    for line in file_content.split("\n")[1:]:
        if line.startswith("#") or not line.strip():
            continue

        yield line.split("/", maxsplit=1)[0]


def generate_word_list(iterator):
    for word in iterator:
        if punctuation in word or len(word) < 2:
            continue

        for umlaut in UMLAUTS:
            if umlaut in word:
                new_word = word
                for umlaut in UMLAUTS:
                    new_word = new_word.replace(umlaut, "�")
                yield (word, new_word)
                break


def write_word_list(words, filepath):
    with open(filepath, "w") as csvfile:
        for word in words:
            writer = csv.writer(
                csvfile, delimiter=";", quotechar='"', quoting=csv.QUOTE_MINIMAL
            )
            writer.writerow((word[0], word[1]))


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate the CSV for later fixing missing umlauts."
    )
    parser.add_argument(
        "source_dictionary",
        type=str,
        help="the dictionary to use for generating the CSV file",
    )
    parser.add_argument(
        "output_file", type=str, help="where the generated csv file should be saved",
    )
    parser.add_argument(
        "-e", "--encoding", default="utf-8", help="the encoding of the dictionary",
    )

    return parser.parse_args()


UMLAUTS = tuple(chain.from_iterable(map(umlaut_variations, "äöüßÄÖÜ")))

if __name__ == "__main__":
    args = parse_args()

    read_dictionary = read_zipfile if is_zipfile(args.source_dictionary) else read_file
    file_content = read_dictionary(args.source_dictionary)
    file_content = file_content.decode(args.encoding)
    words = generate_word_list(file_content_parser(file_content))
    write_word_list(words, args.output_file)
