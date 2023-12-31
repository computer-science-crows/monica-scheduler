import argparse
import dictdatabase as DDB
import sys
import os
from datetime import datetime

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from monica.monica import Monica


# Function to convert date string to datetime object
def parse_date(date_string):
    return datetime.strptime(date_string, '%Y-%m-%d')

# Function to convert time string to datetime.time object
def parse_time(time_string):
    return datetime.strptime(time_string, '%H:%M').time()


class AgendaParser:

    def __init__(self, api) -> None:

        self.parser = argparse.ArgumentParser(description='Command-line parser for the Monica Scheduler distributed agenda')
        self.subparsers = self.parser.add_subparsers(dest='command', help='Available commands')
        self._user_subparser()
        self._workspaces_subparsers()     
        self._server_subparsers()   
        self.monica = Monica(api)
        

        self.commands = {'login':lambda args:self.monica.login(args),
                    'register':lambda args:self.monica.register(args),
                    'logout':lambda args:self.monica.logout(args),
                    'inbox':lambda args:self.monica.inbox(args),
                    'workspaces':lambda args:self.monica.workspaces(args),
                    'profile':lambda args:self.monica.user_profile(args),
                    'create_workspace':lambda args:self.monica.create_workspace(args),
                    'add_user':lambda args:self.monica.add_user(args),
                    'remove_user':lambda args:self.monica.remove_user(args),
                    'get_users':lambda args:self.monica.get_user(args),
                    'change_role':lambda args:self.monica.change_role(args),
                    'create_event':lambda args:self.monica.create_event(args),
                    'remove_event':lambda args:self.monica.remove_event(args),
                    'events':lambda args:self.monica.events(args),
                    'set_event':lambda args:self.monica.set_event(args),
                    'change_workspace_type':lambda args:self.monica.change_workspace_type(args),
                    'exit_workspace':lambda args:self.monica.exit_workspace(args),
                    'request_status':lambda args:self.monica.request_status(args),
                    'check_availability':lambda args: self.monica.check_availability(args),
                    'sudo':lambda args:self.monica.sudo(args)}

    def parse_arguments(self, line):
        self.args = self.parser.parse_args(line)

                    
    def act(self):        
        self.commands[f'{self.args.command}'](self.args)

    
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
        inbox.add_argument('--handle', choices=['accept', 'reject'], help='Accept or reject a request in inbox', type=str, default=None)
        inbox.add_argument('--id', help='Identificator of request to handle', type=str, default=None)
        
        # workspaces
        workspaces = self.subparsers.add_parser('workspaces', help='Get list of all workspaces of the user')
        
        # profile
        user_profile = self.subparsers.add_parser('profile', help='User profile', )
        user_profile.add_argument('--name', help='Edit name', type=str, default=None)
        user_profile.add_argument('--change_password',action='store_true', help='Edit password')

        # exit workspace
        exit_workspace = self.subparsers.add_parser('exit_workspace',help='Exit workspace')
        exit_workspace.add_argument('workspace_id',help='if of workspace')
    
    def _workspaces_subparsers(self):
        
        # create workspace
        create_workspace = self.subparsers.add_parser('create_workspace', help='Create new workspace')
        create_workspace.add_argument('title', help='Title of workspace', default=None)
        create_workspace.add_argument('type',choices=['f', 'h'],help='Type of workspace', default=None)
        create_workspace.add_argument('--id',help='id of workspace', default=None)
        
                      
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

        # create event 
        create_event = self.subparsers.add_parser('create_event', help="Create an event in a workspace of the user")
        create_event.add_argument('workspace_id',help='id of workspace',default=None)
        create_event.add_argument('title',help='Title of event', default=None)
        create_event.add_argument('date',help='Date of event (format: YYYY-MM-DD)', default=None, type=parse_date)        
        create_event.add_argument('start_time', help='Start time (format: HH:MM)', default=None, type=parse_time)
        create_event.add_argument('end_time',help='End time (format: HH:MM)', default=None, type=parse_time)
        create_event.add_argument('--place', help='Place of the event', default=None)
        create_event.add_argument('--id',help='id of workspace', default=None)

        # remove event    
        remove_event = self.subparsers.add_parser('remove_event', help='Remove event from workspace')
        remove_event.add_argument('event_id', help='id of event', default=None)
                
        # get events
        events = self.subparsers.add_parser('events', help='Get list of events of a workspace')
        events.add_argument('workspace_id', help='id of workspace', default=None)

        # set event
        set_event = self.subparsers.add_parser('set_event',help='Edit event')
        set_event.add_argument('id', help='id of event', default=None)
        set_event.add_argument('--title',help='Title of event', default=None)
        set_event.add_argument('--date',help='Date of event (format: YYYY-MM-DD)', default=None, type=parse_date)
        set_event.add_argument('--place', help='Place of the event', default=None)
        set_event.add_argument('--start_time', help='Start time (format: HH:MM)', default=None, type=parse_time)
        set_event.add_argument('--end_time',help='End time (format: HH:MM)', default=None, type=parse_time)        

        # change workspace type
        change_workspace = self.subparsers.add_parser('change_workspace_type',help='Change type of a workspace')
        change_workspace.add_argument('workspace_id', help='id of workspace', default=None)
        change_workspace.add_argument('--admins',help='Administrators of workspace',nargs='+',metavar='user', type=str, default=None)

        # request status
        request_status = self.subparsers.add_parser('request_status',help='Status of requests sent')
        request_status.add_argument('workspace_id',help='Id of workspace', default=None)

        # check availability
        check_availability = self.subparsers.add_parser('check_availability',help='Check if there is any event on a given date and time')
        check_availability.add_argument('workspace_id',help='id of workspace', default=None)
        check_availability.add_argument('date', help='Event date (format: YYYY-MM-DD)',default=None, type=parse_date)
        check_availability.add_argument('--start_time', help='Event start time (format: HH:MM)',default=None, type=parse_time)
        check_availability.add_argument('--end_time', help='Event end time (format: HH:MM)',default=None, type=parse_time)

        
    def _server_subparsers(self):

        sudo = self.subparsers.add_parser('sudo', help='Network actions')
        sudo.add_argument('action', choices=[
                          'create', 'remove'], help='Creates or remove servers')
        sudo.add_argument('-n', type=int,
                          help='Number of servers to connect to network')
        
   




    
        
        
    
     