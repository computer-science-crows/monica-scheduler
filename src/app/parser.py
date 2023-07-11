import argparse
from user import get_user, set_user
from domain.user import User


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

                    
    def act(self):
        
        self.commands[f'{self.args.command}']()



        
        

        # if self.args.command == 'create-event':
        #     event_name = self.args.event_name
        #     # Perform the 'create-event' action
        #     print(f"Creating event: {event_name}")

        # elif self.args.command == 'create-workspace':
        #     workspace_name = self.args.workspace_name
        #     users = self.args.users
        #     events = self.args.events if self.args.events else []
        #     # Perform the 'create-workspace' action
        #     print(f"Creating workspace: {workspace_name}")
        #     print(f"Users: {users}")
        #     print(f"Events: {events}")


    def _login(self):

        print("login")

        if self._already_logged():
            print(f"There is a user logged already.")
            return 
        
        alias = self.args.alias
        password = self.args.password

        # if empty alias or password, error
        if alias == None or password == None:
            print(f'Missing username or password')
            return
        
        user = get_user(alias)
        print(user)
        
        # if user not in DB, register
        if user == None:
            print('You are not register into the app.')
            return
        
                
        # if alias and password match with user's, logged
        if user.alias == alias and user.password:
            user.logged()
            set_user(user)
            self.logged_user = user
            print(f"Welcome to Monica Scheduler {user.alias}!")
            
        else:
            print(f"Incorrect username or password. Try again.")
            
        return
            
   
    def _register(self):

        print("register")

        if self._already_logged():
            print(f"There is a user logged. You cannot register.")
            return 
        
        alias = self.args.alias
        full_name = self.args.full_name
        password=self.args.password
        confirmation = self.args.confirmation

        # Missing args
        if alias == None or full_name == None or password == None or confirmation == None:
            print(f'Missing arguments')
            return
        
        # Password and confirmation not matching
        if password != confirmation:
            print("Wrong password.")
            return
        
        user = get_user(alias)

        if user != None:
            print(f"User with alias {alias} already exists")
            return
        
        new_user = User(alias,full_name, password)
        new_user.logged()
        self.logged_user = new_user
        set_user(new_user.alias,new_user.dicc())


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

    def _already_logged(self):
        return self.logged_user != None

    

    

    def _user_subparser(self):
        # login
        login = self.subparsers.add_parser('login', help='User login')
        login.add_argument('alias', help='Alias', type=str, default=None)
        login.add_argument('password', help='Password', type=str, default=None)

        # register
        register = self.subparsers.add_parser('register', help='User registration')
        register.add_argument('alias', help='Alias', type=str, default=None)
        register.add_argument('full_name', help='Full name', type=str, default=None)
        register.add_argument('password', help='Password', type=str, default=None)
        register.add_argument('confirmation', help='Confirm password', type=str, default=None)

        # logout
        logout = self.subparsers.add_parser('logout', help='Logout')

        # inbox
        inbox = self.subparsers.add_parser('inbox', help='Get inbox with notifications and requests')
        inbox.add_argument('--handle_request', choices=['accept', 'reject'], help='Accept or reject a request in inbox', type=str, default=None)
        inbox.add_argument('--req_id', help='Identificator of request to handle', type=str, default=None)
        
        # workspaces
        workspaces = self.subparsers.add_parser('workspaces', help='Get list of all workspaces of the user')
        
        # edit profile
        edit_user = self.subparsers.add_parser('edit_user', help='Edit user profile', )
        edit_user.add_argument('--alias', help='Edit alias', type=str, default=None)
        edit_user.add_argument('--name', help='Edit name', type=str, default=None)
        edit_user.add_argument('--password', help='Edit password', type=str, default=None)
    
    def _workspaces_subparsers(self):
        
        # create workspace
        create_workspace = self.subparsers.add_parser('create_workspace', help='Create new workspace')
        create_workspace.add_argument('title', help='Title of workspace', default=None)
        create_workspace.add_argument('type',choices=['flat', 'hierarchical'],help='Type of workspace', default=None)
        
        # remove workspace
        remove_workspace = self.subparsers.add_parser('remove_workspace',help='Remove workspace')
        remove_workspace.add_argument('id',help="id of workspace. You can run command 'workspaces' to see id.", default=None)
                
        # add user
        add_user = self.subparsers.add_parser('add_user',help='Add user to workspace')
        add_user.add_argument('workspace_id',help='Id of workspace', default=None)
        add_user.add_argument('user_alias',help='Alias of user to add', default=None)
                        
        # remove user
        remove_user = self.subparsers.add_parser('remove_user', help='Remove user from workspace')
        remove_user.add_argument('workspace_id',help='Id of workspace', default=None)
        remove_user.add_argument('user_alias',help='Alias of user to remove', default=None)
        
        # get users
        get_users = self.subparsers.add_parser('get_users',help='Get users from workspace')
        get_users.add_argument('workspace_id',help='id of workspace', default=None)

        # change_role
        change_role = self.subparsers.add_parser('change_role', help='Change role of user in workspace')
        change_role.add_argument('user_alias', help='Alias of user', default=None)
        change_role.add_argument('workspace_id',help='id of workspace', default=None)

        # remove event    
        remove_event = self.subparsers.add_parser('remove_event', help='Remove event from workspace')
        remove_user.add_argument('event_id', help='id of event', default=None)
        remove_event.add_argument('workspace_id', help='id of workspace', default=None)
        
        # get events
        events = self.subparsers.add_parser('event', help='Get list of events of a workspace')
        events.add_argument('workspace_id', help='id of workspace', default=None)

        # set event
        set_event = self.subparsers.add_parser('set_event',help='Edit event')
        set_event.add_argument('--id', help='id of event', default=None)
        set_event.add_argument('--title',help='Title of event', default=None)
        set_event.add_argument('--date',help='Date of event', default=None)
        set_event.add_argument('--start_time', help='Start time', default=None)
        set_event.add_argument('--end_time',help='End time', default=None)        

        # change workspace type
        change_workspace = self.subparsers.add_parser('change_workspace_type',help='Change type of a workspace')
        change_workspace.add_argument('workspace_id', help='id of workspace', default=None)
        change_workspace.add_argument('--admins',help='Administrators of workspace',type=list, default=None)



def main():    

    # # Step 1: Create an ArgumentParser object
    # parser = argparse.ArgumentParser(description='Command-line parser for creating events and workspaces')

    # # Step 2: Define the command-line arguments
    # subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # # Create the 'create-event' command
    # create_event_parser = subparsers.add_parser('create-event', help='Create a new event')
    # create_event_parser.add_argument('event_name', help='Name of the event')

    # # Create the 'create-workspace' command
    # create_workspace_parser = subparsers.add_parser('create-workspace', help='Create a new workspace')
    # create_workspace_parser.add_argument('workspace_name', help='Name of the workspace')
    # create_workspace_parser.add_argument('users', nargs='+', help='List of users (separated by spaces)')
    # create_workspace_parser.add_argument('--events', nargs='+', help='List of events (separated by spaces)')

    # # Step 3: Parse the command-line arguments
    # args = parser.parse_args()

    # # Step 4: Access the values of the arguments and perform the corresponding actions
    # if args.command == 'create-event':
    #     event_name = args.event_name
    #     # Perform the 'create-event' action
    #     print(f"Creating event: {event_name}")

    # elif args.command == 'create-workspace':
    #     workspace_name = args.workspace_name
    #     users = args.users
    #     events = args.events if args.events else []
    #     # Perform the 'create-workspace' action
    #     print(f"Creating workspace: {workspace_name}")
    #     print(f"Users: {users}")
    #     print(f"Events: {events}")

   
   parser = AgendaParser()
   parser.parse_arguments()
   parser.act()
   



if __name__ == "__main__":
    main()



    
        
        
    
     