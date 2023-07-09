import time
from itertools import takewhile
import operator
from collections import OrderedDict
from abc import abstractmethod, ABC
import dictdatabase as DDB

DDB.config.storage_directory = "src/database"
#DDB.config.use_compression = True 

class Storage:
    """
    Local storage for this node.
    Storage implementations of get must return the same type as put in by set
    """

    def __init__(self, file_name):

        self.file_name = file_name
        if not DDB.at(f"{file_name}").exists():
            DDB.at(f"{file_name}").create({})
  
    
    def __setitem__(self, key, value):
        """
        Set a key to the given value.
        """
        with DDB.at(f"{self.file_name}").session() as (session, file):
            file[f"{key}"] = value 
            session.write()     

        

    def __getitem__(self, key):
        """
        Get the given key.  If item doesn't exist, raises C{KeyError}
        """
        if DDB.at(f"{self.file_name}", key=f"{key}").exists():
            return DDB.at(f"{self.file_name}", key=f"{key}").read()
        
    
    def get(self, key, default=None):
        """
        Get given key.  If not found, return default.
        """
        if DDB.at(f"{self.file_name}", key=f"{key}").exists():
            return DDB.at(f"{self.file_name}", key=f"{key}").read()
        return default

    

    @abstractmethod
    def __iter__(self):
        """
        Get the iterator for this storage, should yield tuple of (key, value)
        """



class ForgetfulStorage(Storage):
    def __init__(self, ttl=604800):
        """
        By default, max age is a week.
        """
        self.data = OrderedDict()
        self.ttl = ttl

    def __setitem__(self, key, value):
        if key in self.data:
            del self.data[key]
        self.data[key] = (time.monotonic(), value)
        self.cull()

    def cull(self):
        for _, _ in self.iter_older_than(self.ttl):
            self.data.popitem(last=False)

    def get(self, key, default=None):
        self.cull()
        if key in self.data:
            return self[key]
        return default

    def __getitem__(self, key):
        self.cull()
        return self.data[key][1]

    def __repr__(self):
        self.cull()
        return repr(self.data)

    def iter_older_than(self, seconds_old):
        min_birthday = time.monotonic() - seconds_old
        zipped = self._triple_iter()
        matches = takewhile(lambda r: min_birthday >= r[1], zipped)
        return list(map(operator.itemgetter(0, 2), matches))

    def _triple_iter(self):
        ikeys = self.data.keys()
        ibirthday = map(operator.itemgetter(0), self.data.values())
        ivalues = map(operator.itemgetter(1), self.data.values())
        return zip(ikeys, ibirthday, ivalues)

    def __iter__(self):
        self.cull()
        ikeys = self.data.keys()
        ivalues = map(operator.itemgetter(1), self.data.values())
        return zip(ikeys, ivalues)


storage = Storage('data')

storage['hola'] = 'mar'
storage['pe']={'1':'d','2':'f'}

print(storage['pe'])
 