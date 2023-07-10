import argparse
from user import get_user, set_user

class AgendaParser:

    def __init__(self) -> None:

        self.parser = argparse.ArgumentParser(description='Command-line parser for the Monica Scheduler distributed agenda')
        self.subparsers = self.parser.add_subparsers(dest='command', help='Available commands')
        self._user_subparser()
        self._workspaces_subparsers()
        self.logged_user=None

        self.commands = {'login':lambda:self._login(),
                    'register':lambda:self._register(),
                    'logout':lambda:self._logout(),
                    'inbox':lambda:self._inbox(),
                    'workspace':lambda:self._workspaces(),
                    'edit_user':lambda:self._edit_user(),
                    'create_workspace':lambda:self._create_workspace(),
                    'remove_workspace':lambda:self._remove_workspace(),
                    'add_user':lambda:self._add_user(),
                    'remove_user':lambda:self._remove_user(),
                    'get_user':lambda:self._get_user(),
                    'change_role':lambda:self._change_role(),
                    'remove_event':lambda:self._remove_event(),
                    'event':lambda:self._event(),
                    'set_event':lambda:self._set_event(),
                    'change_wokspace_type':lambda:self._change_workspace_type()}

    def parse_arguments(self):
        self.args = self.parser.parse_args()

        return self.args
    
    def act(self):
        self.commands[self.args.command]



        
        

        if self.args.command == 'create-event':
            event_name = self.args.event_name
            # Perform the 'create-event' action
            print(f"Creating event: {event_name}")

        elif self.args.command == 'create-workspace':
            workspace_name = self.args.workspace_name
            users = self.args.users
            events = self.args.events if self.args.events else []
            # Perform the 'create-workspace' action
            print(f"Creating workspace: {workspace_name}")
            print(f"Users: {users}")
            print(f"Events: {events}")


    def _login(self):
        alias = self.alias
        password = self.password

        if alias == None or password == None:
            print(f'Missing username or password')
            return
        
        user = get_user(alias)


        if user == None:
            print('You are not register into the app.')
            return
        
        if user.alias == alias and user.password:
            user.logged



    def _register(self):
        pass

    def _logout(self):
        pass

    def _inbox(self):
        pass

    def _workspaces(self):
        pass

    def _edit_user(self):
        pass

    def _create_workspace(self):
        pass

    def _remove_workspace(self):
        pass

    def _add_user(self):
        pass

    def _remove_user(self):
        pass

    def _get_user(self):
        pass

    def _change_role(self):
        pass

    def _remove_event(self):
        pass

    def _event(self):
        pass

    def _set_event(self):
        pass

    def _change_workspace_type(self):
        pass



    

    

    def _user_subparser(self):
        # login
        login = self.subparsers.add_parser('login', help='User login')
        login.add_argument('alias', help='Alias', type=str)
        login.add_argument('password', help='Password', type=str)

        # register
        register = self.subparsers.add_parser('register', help='User registration', type=str)
        register.add_argument('alias', help='Alias', type=str)
        register.add_argument('full_name', help='Full name', type=str)
        register.add_argument('password', help='Password', type=str)
        register.add_argument('confirmation', help='Confirm password', type=str)

        # logout
        logout = self.subparsers.add_parser('logout', help='Logout')

        # inbox
        inbox = self.subparsers.add_parser('inbox', help='Get inbox with notifications and requests', type=str)
        inbox.add_argument('--handle_request', choices=['accept', 'reject'], help='Accept or reject a request in inbox', type=str)
        inbox.add_argument('--req_id', help='Identificator of request to handle', type=str)
        
        # workspaces
        workspaces = self.subparsers.add_parser('workspaces', help='Get list of all workspaces of the user', type=str)
        
        # edit profile
        edit_user = self.subparsers.add_parser('edit_user', help='Edit user profile')
        edit_user.add_argument('--alias', help='Edit alias', type=str)
        edit_user.add_argument('--name', help='Edit name', type=str)
        edit_user.add_argument('--password', help='Edit password', type=str)
    
    def _workspaces_subparsers(self):
        
        # create workspace
        create_workspace = self.subparsers.add_parser('create_workspace', help='Create new workspace')
        create_workspace.add_argument('title', help='Title of workspace')
        create_workspace.add_argument('type',choices=['flat', 'hierarchical'],help='Type of workspace')
        
        # remove workspace
        remove_workspace = self.subparsers.add_parser('remove_workspace',help='Remove workspace')
        remove_workspace.add_argument('id',help="id of workspace. You can run command 'workspaces' to see id.")
                
        # add user
        add_user = self.subparsers.add_parser('add_user',help='Add user to workspace')
        add_user.add_argument('workspace_id',help='Id of workspace')
        add_user.add_argument('user_alias',help='Alias of user to add')
                        
        # remove user
        remove_user = self.subparsers.add_parser('remove_user', help='Remove user from workspace')
        remove_user.add_argument('workspace_id',help='Id of workspace')
        remove_user.add_argument('user_alias',help='Alias of user to remove')
        
        # get users
        get_users = self.subparsers.add_parser('get_users',help='Get users from workspace')
        get_users.add_argument('workspace_id',help='id of workspace')

        # change_role
        change_role = self.subparsers.add_parser('change_role', help='Change role of user in workspace')
        change_role.add_argument('user_alias', help='Alias of user')
        change_role.add_argument('workspace_id',help='id of workspace')

        # remove event    
        remove_event = self.subparsers.add_parser('remove_event', help='Remove event from workspace')
        remove_user.add_argument('event_id', help='id of event')
        remove_event.add_argument('workspace_id', help='id of workspace')
        
        # get events
        events = self.subparsers.add_parser('event', help='Get list of events of a workspace')
        events.add_argument('workspace_id', help='id of workspace')

        # set event
        set_event = self.subparsers.add_parser('set_event',help='Edit event')
        set_event.add_argument('--id', help='id of event')
        set_event.add_argument('--title',help='Title of event')
        set_event.add_argument('--date',help='Date of event')
        set_event.add_argument('--start_time', help='Start time')
        set_event.add_argument('--end_time',help='End time')        

        # change workspace type
        change_workspace = self.subparsers.add_parser('change_workspace_type',help='Change type of a workspace')
        change_workspace.add_argument('workspace_id', help='id of workspace')
        change_workspace.add_argument('--admins',help='Administrators of workspace',type=list)



def main():
    # Step 1: Create an ArgumentParser object
    parser = argparse.ArgumentParser(description='A simple program')

    # Step 2: Define the command-line arguments
    parser.add_argument('name', help='Your name')
    parser.add_argument('--age', help='Your age', type=int)

    # Step 3: Parse the command-line arguments
    args = parser.parse_args()

    # Step 4: Access the values of the arguments
    name = args.name
    age = args.age

    # Step 5: Print the values
    print(f"Hello, {name}!")
    if age:
        print(f"You are {age} years old.")

if __name__ == "__main__":
    main()



    
        
        
    
     