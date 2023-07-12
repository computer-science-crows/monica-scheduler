from api.api import API
from app.parser import AgendaParser


def handle_command(args, api):
    # Handle the 'monica' command
    if args.command == 'monica':
        print("Running Monica command...")
        # Insert your Monica command code here
    else:
        print(f"Unknown command: {args.command}")


def main():
    # Create the top-level parser
    agenda_parser = AgendaParser()
    agenda_parser.parser.add_argument(
        'command', help='The command to execute')

    # api = API()

    print("\U0001F499 Monica Scheduler \U0001F499")
    print("Enter 'quit' to exit.")
    # print("\U000023F3 Hourglass")
    while True:
        # Read a line of input
        line = input('\U0001F4C6 ')
        if line == 'quit':
            break

        # Parse the arguments
        args = agenda_parser.parser.parse_args(line.split())

        # Handle the command
        # handle_command(args, api)


if __name__ == '__main__':
    main()
