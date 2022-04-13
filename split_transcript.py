import csv
from typing import Dict


def get_party_tweet(filename: str):
    president_to_party = {}
    with open(filename) as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            if line_count > 0:
                president_to_party[row['Tweet']] = row['Party']
            line_count += 1
    return president_to_party


def main():
    res = get_party_tweet('ExtractedTweets.csv')
    print(res)

if __name__ == "__main__":
    main()