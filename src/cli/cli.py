import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from parser import AgendaParser

def main():    

   agenda_parser = AgendaParser()

#    line = 'change_workspace_type 968376b8-0040-475f-879c-28af2c3b1a84'
#    agenda_parser.parse_arguments(line.split())
#    agenda_parser.act()



   while True:
        # Read a line of input
        line = input('\U0001F4C6 ')
        if line == 'quit':
            break

        # Parse the arguments
        
        # try:
        #     agenda_parser.parse_arguments(line.split())
        #     agenda_parser.act()
        # except:
        #     ...

        # try:
        #     agenda_parser.parse_arguments(line.split())
        #     agenda_parser.act()
        # except Exception as e:
        #     print(e)

        agenda_parser.parse_arguments(line.split())
        agenda_parser.act()
             

        
        
           

        # Handle the command
        # handle_command(args, api)
   
   

if __name__ == "__main__":
    main()