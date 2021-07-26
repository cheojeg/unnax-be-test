import sys
import argparse
from banking.scripts import Scraping

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--username", "-u", help="set username")
    parser.add_argument("--password", "-p", help="set password")

    args = parser.parse_args()

    if args.username and args.password:
        ws = Scraping(args.username, args.password)
        ws.print_data()
    else:
        print("Please set username and password as params")
