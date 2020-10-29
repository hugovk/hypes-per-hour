# Chat downloaded with https://github.com/PetterKraabol/Twitch-Chat-Downloader:
# tcd --video 608349943

import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="TODO", formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("-v", "--video", default="785714223", help="Video ID")
    parser.add_argument("-w", "--word", default="hype", help="Word to search for")
    args = parser.parse_args()

    with open(f"{args.video}.txt") as f:
        lines = f.readlines()

    search_word = args.word

    def get_hour(line):
        elapsed = line[1:].split("]")[0]
        elapsed = elapsed.replace("1 day, 0", "24")
        elapsed_hour = elapsed.split(":")[0]

        return int(elapsed_hour)

    hypes_per_hour = [0]
    hour = 0

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

    print(f"hour\t{search_word}s per hour ({search_word[0].upper()}PH)")
    # print(f"{search_word}s per hour ({search_word[0].upper()}PH)")
    for i, thing in enumerate(hypes_per_hour):
        print(f"{i+1}\t{thing}")
        # print(f"{thing}")
