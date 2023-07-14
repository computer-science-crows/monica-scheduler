from parser import AgendaParser
import argparse

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def get_args():
    parser = argparse.ArgumentParser()

    # Optional arguments
    parser.add_argument(
        "-ground", help="Specifies whether to show the CLI or send it to background as a kad node", type=str)
    return parser.parse_args()


def main():
    args = get_args()
    send = True if args.ground == 'back' else False
    
    agenda_parser = AgendaParser(args.send_bckgrnd)

    print("\U0001F499 Monica Scheduler \U0001F499")
    print("Enter 'quit' to exit.")
    while True:
        # Read a line of input
        line = input('\U0001F4C6 ')
        if line == 'quit':
            break

        # Parse the arguments

        try:
            agenda_parser.parse_arguments(line.split())
            agenda_parser.act()
        except:
            ...

        # try:
        #     agenda_parser.parse_arguments(line.split())
        #     agenda_parser.act()
        # except Exception as e:
        #     print(e)

        # agenda_parser.parse_arguments(line.split())
        # agenda_parser.act()

        # Handle the command
        # handle_command(args, api)


if __name__ == "__main__":
    main()
