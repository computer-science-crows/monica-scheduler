import sys
import os
import time

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print(os.getcwd())
from cli.parser import AgendaParser
from api.api import API

def read(file):
       # Open the file in read mode ('r')
    with open(file, 'r') as file:
        # Read the contents of the file
        contents = file.readlines()
    
    return contents


def test(file_name):
    
    content = read(file_name)
    api = API()
    agenda_parser = AgendaParser(api)

    print("\U0001F499 Monica Scheduler \U0001F499")
    print("Enter 'quit' to exit.")
    for line in content:
        print('\U0001F4C6 ' + line)

        if line == 'quit':
            break

        # try:
        #     agenda_parser.parse_arguments(line.split())
        #     agenda_parser.act()
        # except:
        #     ...

        agenda_parser.parse_arguments(line.split())
        agenda_parser.act()

        # time.sleep(30)
        print()

path = os.getcwd() +'/tests'


# test register - login - logout
# test(path +'/test_register_login_logout.txt')

# test profile
# test(path +'/test_profile.txt')

# test create_workspace
# test(path +'/test_create_workspace.txt')

# test exit_workspace
# test(path +'/test_exit_workspace.txt')

# test create_event
# test(path +'/test_create_event.txt')

# test remove_event
# test(path +'/test_remove_event.txt')

# test set_event
# test(path +'/test_set_events.txt')

# test events
# test(path +'/test_events.txt')

# test check_availability
# test(path +'/test_check_availability.txt')

# test add_user
# test(path +'/test_add_user.txt')

# test remove_user
# test(path +'/test_remove_user.txt')

# test get_users
# test(path +'/test_get_users.txt')

# test change_role
# test(path +'/test_change_role.txt')

# test change_workspace_type
# test(path +'/test_change_workspace_type.txt')

# test request_status
test(path +'/test_request_status.txt')




