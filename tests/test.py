import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print(os.getcwd())
from src.cli.parser import AgendaParser

def read(file):
       # Open the file in read mode ('r')
    with open(file, 'r') as file:
        # Read the contents of the file
        contents = file.readlines()
    
    return contents


def test(file_name):
    
    content = read(file_name)
    agenda_parser = AgendaParser()

    for line in content:
        print('\U0001F4C6 ' + line)
        try:
            agenda_parser.parse_arguments(line.split())
            agenda_parser.act()
        except:
            ...

test(os.getcwd() + '/test_1.txt')