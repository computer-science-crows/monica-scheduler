import argparse
from app.user import get_user, set_user
from app.workspace import get_workspace, set_workspace
from app.domain.user import User
import json
import dictdatabase as DDB
from app.request import get_request,set_request
from app.event import get_event, set_event


class AgendaParser:

    def __init__(self) -> None:

        self.parser = argparse.ArgumentParser(description='Command-line parser for the Monica Scheduler distributed agenda')
        self.subparsers = self.parser.add_subparsers(dest='command', help='Available commands')
        self._user_subparser()
        self._workspaces_subparsers()
        self.logged_user=None
        self._last_user_logged()

        self.commands = {'login':lambda:self._login(),
                    'register':lambda:self._register(),
                    'logout':lambda:self._logout(),
                    'inbox':lambda:self._inbox(),
                    'workspaces':lambda:self._workspaces(),
                    'edit_profile':lambda:self._edit_user(),
                    'create_workspace':lambda:self._create_workspace(),
                    'remove_workspace':lambda:self._remove_workspace(),
                    'add_user':lambda:self._add_user(),
                    'remove_user':lambda:self._remove_user(),
                    'get_users':lambda:self._get_user(),
                    'change_role':lambda:self._change_role(),
                    'create_event':lambda:self._create_event(),
                    'remove_event':lambda:self._remove_event(),
                    'events':lambda:self._events(),
                    'set_event':lambda:self._set_event(),
                    'change_wokspace_type':lambda:self._change_workspace_type(),
                    'exit_workspace':lambda:self._exit_workspace()}

    def parse_arguments(self):
        self.args = self.parser.parse_args()

                    
    def act(self):        
        self.commands[f'{self.args.command}']()

    def _last_user_logged(self):

        DDB.config.storage_directory = "log"
        database = DDB.at(f"log")
        if not database.exists():
            database.create({})

        data = database.read()
        if len(list(data.keys())) > 0:
            self.logged_user = data[list(data.keys())[0]]

    def _update_user_logger(self, user):
        DDB.config.storage_directory = "log"
        with DDB.at("log").session() as (session, file):
            file[f"{user.alias}"] = user.dicc()
            session.write()
     
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
        if user.alias == alias and user.password == password:
            user.logged()
            set_user(user.alias, user.dicc())
            self.logged_user = user

            self._update_user_logger(user)
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

        self._update_user_logger(new_user)
       
        print("Succesfully register")

    def _logout(self):

        print('logout')
        print(self._already_logged())
        print(self.logged_user)
        
        if not self._already_logged():
            print("There is no user logged")
            return
        
        user = get_user(self.logged_user["alias"])
        print(f"User {user}")
        user.active = False
        set_user(user.alias,user.dicc())
        self.logged_user = None

        DDB.config.storage_directory = "log"
        DDB.at("log").delete()

        print("Bye!")

   
    def _inbox(self):

        if not self._already_logged():
            print("There is no user logged")
            return
        
        handle_request = self.args.handle_request
        req_id = self.args.req_id

        user = get_user(self.logged_user['alias'])
        requests = {}

        for req in user.requests:
            requests[req] = get_request(req)
        
        if handle_request == None and req_id == None:
            print(f"Inbox:")
            for r in requests.values():
                print(f"- {r}")
            
        elif handle_request == None and req_id != None:
            print(f"{requests[req_id]}")
        elif handle_request != None and req_id != None:

            workspace = get_workspace(requests[req_id].workspace_id)

            if handle_request == 'accept':                
                new = user.accept_request(requests[req_id],workspace)
                if requests[req_id].get_type() == 'workspace' and new:
                    workspace = new
            else:
                user.reject_request(requests[req_id],workspace)

            set_user(user.alias, user.dicc())
            set_workspace(workspace.workspace_id, workspace.dicc())
            set_request(req_id, requests[req_id].dicc())

    def _workspaces(self):
        
        if not self._already_logged():
            print("There is no user logged")
            return
        
        user = get_user(self.logged_user['alias'])

        workspaces = []

        for w in user.workspaces:
            workspaces.append(get_workspace(w))

        print(f"Workspaces:")
        for i,w in enumerate(workspaces):
            print(f"{i+1}. {w}")

    def _edit_user(self):

        if not self._already_logged():
            print("There is no user logged")
            return
        
        alias = self.args.alias
        name = self.args.name
        password = self.args.password

        if alias == None and name == None and password == None:
            return
        
                
        user = get_user(self.logged_user['alias'])

        same_alias_user = None

        if alias != None:
            same_alias_user = get_user(alias)
        
        if same_alias_user != None:
            print(f"User with alias {alias} already exists")
            return
        

        new_user = User(alias or user.alias, name or user.full_name, password or user.password)
        new_user.requests = user.requests
        new_user.active = user.active
        new_user.workspaces = user.workspaces

        set_user(new_user.alias,new_user.dicc())

        DDB.config.storage_directory = "log"

        # se puede hacer mejor
        DDB.at("log").delete()

        self._last_user_logged()

        self._update_user_logger(new_user)

        print(f'Profile edited.')

    def _create_workspace(self):

        if not self._already_logged():
            print("There is no user logged")
            return
        
        title = self.args.title
        type = self.args.type

        if type == 'f':
            type = 'flat'
        else:
            type = 'hierarchical'

        user = get_user(self.logged_user['alias'])

        new_workspace = user.create_workspace(title,type)
        set_user(user.alias,user.dicc())
        set_workspace(new_workspace.workspace_id,new_workspace.dicc())

        self._update_user_logger(user)

        print(f"Worspace {new_workspace.workspace_id} was created.")

    def _remove_workspace(self):

        if not self._already_logged():
            print("There is no user logged")
            return
        
        workspace_id = self.args.id

        user = get_user(self.logged_user['alias'])
        remove = user.remove_workspace(workspace_id)

        if remove:
            set_user(user.alias,user.dicc())
            self._update_user_logger(user)
            print(f"Succesfully removed workspace")
        else:
            print(f"User {user} does not belong to worksoace {workspace_id}")

    def _add_user(self):
        
        if not self._already_logged():
            print("There is no user logged")
            return
        
        workspace_id = self.args.workspace_id
        user_alias = self.args.user_alias

        user = get_user(self.logged_user['alias'])
        user_to_add = get_user(user_alias)
        workspace = get_workspace(workspace_id)
        
        if user_to_add == None:
            print(f"User {user_alias} is not register into the app")
            return
        if workspace == None or workspace_id not in user.workspaces:
            print(f"User {user.alias} does not belong to workspace {workspace_id}")
            return
        

        request = workspace.add_user(user.alias, user_to_add)

        if request:
            set_request(request.request_id,request.dicc())

        set_user(user.alias,user.dicc())
        set_user(user_to_add.alias,user_to_add.dicc())
        set_workspace(workspace_id,workspace.dicc())

    def _remove_user(self):

        if not self._already_logged():
            print("There is no user logged")
            return
        
        workspace_id = self.args.workspace_id
        user_alias = self.args.user_alias

        user = get_user(self.logged_user['alias'])
        user_to_remove = get_user(user_alias)
        workspace = get_workspace(workspace_id)
        
        if user_to_remove == None:
            print(f"User {user_alias} is not register into the app")
            return
        if workspace == None or workspace_id not in user.workspaces:
            print(f"User {user.alias} does not belong to workspace {workspace_id}")
            return
        
        remove = workspace.remove_user(user.alias, user_to_remove)

        if remove:
            set_user(user.alias,user.dicc())
            set_user(user_to_remove.alias,user_to_remove.dicc())
            set_workspace(workspace_id,workspace.dicc())

    def _get_user(self):
        
        if not self._already_logged():
            print("There is no user logged")
            return
        
        workspace_id = self.args.workspace_id

        user = get_user(self.logged_user['alias'])

        if workspace_id in user.workspaces:
            workspace = get_workspace(workspace_id)
            print(f"Users of workspace {workspace_id}:")
            for u in workspace.users:
                print(f"- {u}")
            return

        print(f"User {user.alias} does not belong to workspace {workspace_id}")

    def _change_role(self):

        if not self._already_logged():
            print("There is no user logged")
            return
        
        user_alias = self.args.user_alias
        workspace_id = self.args.workspace_id

        user = get_user(self.logged_user['alias'])
        
        if workspace_id not in user.workspaces:
            print(f"User {user.alias} does not belong to workspace {workspace_id}")
            return
        
        user_to_change = get_user(user_alias)
        workspace = get_workspace(workspace_id)

        if workspace.get_type() == 'flat':
            print(f"Workspace {workspace_id} does not have roles")
            return

        workspace.change_role(user.alias,user_alias)

        set_user(user.alias,user.dicc())
        set_user(user_to_change.alias,user_to_change.dicc())
        set_workspace(workspace.workspace_id,workspace.dicc())

    def _create_event(self):
        
        if not self._already_logged():
            print("There is no user logged")
            return
        
        workspace_id = self.args.workspace_id
        title = self.args.title
        date = self.args.date
        place = self.args.place
        start_time = self.args.start_time
        end_time = self.args.end_time

        user_get = get_user(self.logged_user['alias'])

        if workspace_id not in user_get.workspaces:
            print(f"User {user_get.alias} does not belong to workspace {workspace_id}")

        workspace_get = get_workspace(workspace_id)
        users = []

        for u in workspace_get.users:
            users.append(get_user(u))
        
        users_collision = []
        print(f"DATE {date}")
        for user in users:
            for workspace_id in user.workspaces:    
                workspace = get_workspace(workspace_id)            
                for event_id in workspace.events:
                    event = get_event(event_id)
                    print(event)
                    if date == event.date and (start_time <= event.start_time or end_time >= event.end_time):
                        users_collision.append(user)
                
        if users_collision != []:
            print(f"WARNING: User {users_collision[0]} has an event that collides with the new event.")
            while True:
                confirmation = input("Do you want to continue? (y/n): ")
                if confirmation.lower() == 'y':
                    break
                if confirmation.lower() == 'n':
                    return 

        event, request = user_get.create_event(workspace_get, title, date,place, start_time, end_time,users)

        print(f"EVENT {event}")
        if event != None:
            set_event(event.event_id, event.dicc())

        print(f"REQUEST {request}")
        if request != None:
            set_request(request.request_id, request.dicc())

        set_user(user_get.alias,user_get.dicc())

        for u in users:
            set_user(u.alias,u.dicc())

        set_workspace(workspace_get.workspace_id,workspace_get.dicc())

    def _remove_event(self):
        
        if not self._already_logged():
            print("There is no user logged")
            return
        
        event_id = self.args.event_id


        user = get_user(self.logged_user['alias'])
        event = get_event(event_id)        
        workspace= get_workspace(event.workspace_id)

        user.remove_event(workspace,event)

        set_user(user.alias,user.dicc())
        set_workspace(workspace.workspace_id,workspace.dicc())
 
    def _events(self):
        
        if not self._already_logged():
            print("There is no user logged")
            return
        
        workspace_id = self.args.workspace_id

        user = get_user(self.logged_user['alias'])

        if workspace_id not in user.workspaces:
            print(f"User {user.alias} does not belong to workspace {workspace_id}")
            return
        
        
        workspace = get_workspace(workspace_id)

        print(f"Events of workspace {workspace_id}:")
        for i,e in enumerate(workspace.events):
            print(f"{i+1}. {get_event(e)}")
    
    def _set_event(self):

        if not self._already_logged():
            print("There is no user logged")
            return
        
        event_id = self.args.id
        title = self.args.title
        date = self.args.date
        place = self.args.place
        start_time = self.args.start_time
        end_time = self.args.end_time

        user = get_user(self.logged_user['alias'])

        event = get_event(event_id)
        
        workspace= get_workspace(event.workspace_id)
        
        
        new_event = user.set_event(
            event=event, 
            workspace=workspace,
            title = title,
            date = date,
            place = place,
            end_time = end_time,
            start_time = start_time
        )

        if new_event != None:
            set_event(new_event.event_id, new_event.dicc())

    def _change_workspace_type(self):
        
        if not self._already_logged():
            print("There is no user logged")
            return
        


    def _exit_workspace(self):
        
        if not self._already_logged():
            print("There is no user logged")
            return
        
        workspace_id = self.args.workspace_id

        user = get_user(self.logged_user['alias'])
        workspace = get_workspace(workspace_id) 

        user.exit_workspace(workspace)

        set_user(user.alias, user.dicc())
        set_workspace(workspace.workspace_id, workspace.dicc())

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
        edit_user = self.subparsers.add_parser('edit_profile', help='Edit user profile', )
        edit_user.add_argument('--alias', help='Edit alias', type=str, default=None)
        edit_user.add_argument('--name', help='Edit name', type=str, default=None)
        edit_user.add_argument('--password', help='Edit password', type=str, default=None)

        # exit workspace
        exit_workspace = self.subparsers.add_parser('exit_workspace',help='Exit workspace')
        exit_workspace.add_argument('workspace_id',help='if of workspace')

    
    def _workspaces_subparsers(self):
        
        # create workspace
        create_workspace = self.subparsers.add_parser('create_workspace', help='Create new workspace')
        create_workspace.add_argument('title', help='Title of workspace', default=None)
        create_workspace.add_argument('type',choices=['f', 'h'],help='Type of workspace', default=None)
        
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

        # create event 
        create_event = self.subparsers.add_parser('create_event', help="Create an event in a workspace of the user")
        create_event.add_argument('workspace_id',help='id of workspace',default=None)
        create_event.add_argument('title',help='Title of event', default=None)
        create_event.add_argument('date',help='Date of event', default=None)
        create_event.add_argument('place', help='Place of the event', default=None)
        create_event.add_argument('start_time', help='Start time', default=None)
        create_event.add_argument('end_time',help='End time', default=None)

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
        set_event.add_argument('--date',help='Date of event', default=None)
        set_event.add_argument('--place', help='Place of the event', default=None)
        set_event.add_argument('--start_time', help='Start time', default=None)
        set_event.add_argument('--end_time',help='End time', default=None)        

        # change workspace type
        change_workspace = self.subparsers.add_parser('change_workspace_type',help='Change type of a workspace')
        change_workspace.add_argument('workspace_id', help='id of workspace', default=None)
        change_workspace.add_argument('--admins',help='Administrators of workspace',type=list, default=None)



def main():    

   parser = AgendaParser()
   parser.parse_arguments()
   parser.act()
   

if __name__ == "__main__":
    main()



    
        
        
    
     