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
        
        if len(line) > 1:

            print('\U0001F4C6 ' + line)
            # try:
            #     agenda_parser.parse_arguments(line.split())
            #     agenda_parser.act()
            # except:
            #     ...

            agenda_parser.parse_arguments(line.split())
            agenda_parser.act()

            print()

path = os.getcwd() +'/tests'

# test register - login - logout
# test(path +'/test_register_login_logout.txt')

# test create_workspace
# test(path +'/test_create_workspace.txt')

# test create_event
# test(path +'/test_create_event.txt')

# test exit_workspace
# test(path +'/test_exit_workspace.txt')

# test add_user
# test(path +'/test_add_user.txt')

# test change_role
# test(path +'/test_change_role.txt')

# test change_workspace_type
# test(path +'/test_change_workspace_type.txt')

# test check_availability
# test(path +'/test_check_availability.txt')

# test events
# test(path +'/test_events.txt')

# test get_users
# test(path +'/test_get_users.txt')

# test profile
# test(path +'/test_profile.txt')

# test remove_event
# test(path +'/test_remove_event.txt')

# test remove_user
# test(path +'/test_remove_user.txt')

# test request_status
#test(path +'/test_request_status.txt')

# test set_event
# test(path +'/test_set_events.txt')

# test_collisions
# test(path +'/test_event_collisions.txt')

# test_sudo_1
# test(path +'/test_sudo_1.txt')

# test_sudo_2
# test(path +'/test_sudo_2.txt')

# test_sudo_3
# test(path +'/test_sudo_3.txt')

# test_sudo_4
# test(path +'/test_sudo_4.txt')

# test_sudo_5
# test(path +'/test_sudo_5.txt')




