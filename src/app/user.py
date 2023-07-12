import dictdatabase as DDB
from app.domain.user import User
import hashlib


def get_user(alias, api):

    data = api.get_value(alias)[1]
    # print(data)

    if data == None:
        # print("seras mongo?")
        return

    try:
        # print('try')
        data = eval(eval(data)[1])
        # print(f"first try {data}")
    except:
        # print('except')
        data = eval(data)
        # print(f"second try {data}")

    # print(f"DATA {data}")
    # print(f"DICC {data['alias']}")
    user = User(data['alias'], data['full_name'], data['password'])
    user.active = data['logged']
    user.requests = data['inbox']
    user.workspaces = data['workspaces']

    return user


def set_user(alias, dicc, api):
    # print("SET")
    res = api.set_value(alias, dicc)
    # print(res[1])
