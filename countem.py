# Chat downloaded with https://github.com/PetterKraabol/Twitch-Chat-Downloader:
# tcd --video 608349943

import argparse

from prettytable import PrettyTable


def get_hour(line):
    elapsed = line[1:].split("]")[0]
    elapsed = elapsed.replace("1 day, 0", "24")
    # for "date time"
    if " " in elapsed:
        elapsed = elapsed.split(" ")[1]
    elapsed_hour = elapsed.split(":")[0]

    return int(elapsed_hour)


def do_word(search_word: str, lines: list) -> list:
    hypes_per_hour = [0]
    hour = get_hour(lines[0])

    for line in lines:
        line = line.strip()
        elapsed_hour = get_hour(line)

        line_lower = line.lower()
        hypes = line_lower.count(search_word)

        if elapsed_hour == hour:
            hypes_per_hour[-1] += hypes
        else:
            hour += 1
            hypes_per_hour.append(hypes)

    return hypes_per_hour


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="TODO", formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("-i", "--infile", default="data/chat.txt", help="Input file")
    parser.add_argument("-v", "--video", help="Video ID")
    parser.add_argument("-w", "--words", default="hype", help="CSV words to search for")
    args = parser.parse_args()

    if args.video:
        args.infile = f"data/{args.video}.txt"

    with open(args.infile) as f:
        lines = f.readlines()

    results = dict()
    for search_word in args.words.split(","):

        words_per_hour = do_word(search_word, lines)
        results[search_word] = words_per_hour

    table = PrettyTable()
    first_thing = next(iter(results))
    # Start from first hour
    first_hour = get_hour(lines[0])

    hours = []
    for hour in range(len(results[first_thing])):
        out = first_hour + hour
        if out >= 24:
            out -= 24
        hours.append(out)

    table.add_column("hour", hours)

    for word, counts in results.items():
        table.add_column(word, counts)

    print(table)

    with open("data/output.csv", "w") as f:
        print(table.get_csv_string(), file=f)

    with open("data/output.tsv", "w") as f:
        print(table.get_csv_string(delimiter="\t"), file=f)
