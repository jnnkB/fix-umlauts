import sys
import unicodedata
from string import punctuation
import tempfile
from zipfile import ZipFile, is_zipfile

UMLAUTS = list(map(lambda x: x.encode(), "äöüßÄÖÜ"))
UMLAUTS += list(map(lambda x: unicodedata.normalize("NFD", x).encode(), "äöüßÄÖÜ"))
words = []

source_file = sys.argv[1]
utf8_file = tempfile.mkstemp()
extracted_dict_file = tempfile.mkstemp()

BLOCKSIZE = 1048576

if is_zipfile(source_file):
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

        file_content = myzip.read(dict_file)
else:
    with open(source_file, "rb") as f:
        file_content = f.read()


file_content = file_content.decode("iso-8859-1")
file_content = file_content.encode()


for line in file_content.split(b"\n")[1:]:
    if line.startswith(b"#") or line == "\t":
        continue

    word = line.split(b"/", maxsplit=1)[0]
    if punctuation.encode() in word or len(word.decode()) < 2:
        continue

    for umlaut in UMLAUTS:
        if umlaut in word:
            words.append(word)
            break

with open(sys.argv[2], "wb") as f:
    for word in words:
        new_word = word
        for umlaut in UMLAUTS:
            new_word = new_word.replace(umlaut, "�".encode())
        f.write(new_word.strip() + b";" + word + b"\n")
