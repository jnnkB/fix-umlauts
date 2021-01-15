import sys
import unicodedata
from string import punctuation
from zipfile import ZipFile, is_zipfile
from itertools import chain
import csv


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


UMLAUTS = tuple(chain.from_iterable(map(umlaut_variations, "äöüßÄÖÜ")))

if __name__ == "__main__":
    source_file = sys.argv[1]

    if is_zipfile(source_file):
        read_zipfile(source_file)
    else:
        with open(source_file, "rb") as f:
            file_content = f.read()

    file_content = file_content.decode("iso-8859-1")
    words = generate_word_list(file_content_parser(file_content))
    write_word_list(words, sys.argv[2])
