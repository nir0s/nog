import os

from tinydb import TinyDB, Query

NOG_HOME = os.path.join(os.path.expanduser('~'), '.nog')
NOG_FILE = os.path.join(NOG_HOME, 'nog.json')


class TinyDBStorage(object):
    def __init__(self, db_path=NOG_FILE):
        self.db_path = os.path.expanduser(db_path)
        self._db = None

    @property
    def db(self):
        if self._db is None:
            self._db = TinyDB(
                self.db_path,
                indent=4,
                sort_keys=True,
                separators=(',', ': '))
        return self._db

    def init(self):
        dirname = os.path.dirname(self.db_path)
        if dirname and not os.path.isdir(dirname):
            os.makedirs(os.path.dirname(self.db_path))
        self.db.insert({'data': 'null'})
        return self.db_path

    def put(self, key):
        """Insert the key and return its database id
        """
        return self.db.insert(key)

    def list(self):
        """Return a list of all keys (not just key names, but rather the keys
        themselves).

        e.g.
         {u'created_at': u'2016-10-10 08:31:53',
          u'description': None,
          u'metadata': None,
          u'modified_at': u'2016-10-10 08:31:53',
          u'name': u'aws',
          u'uid': u'459f12c0-f341-413e-9d7e-7410f912fb74',
          u'value': u'the_value'},
         {u'created_at': u'2016-10-10 08:32:29',
          u'description': u'my gcp token',
          u'metadata': {u'owner': u'nir'},
          u'modified_at': u'2016-10-10 08:32:29',
          u'name': u'gcp',
          u'uid': u'a51a0043-f241-4d52-93c1-266a3c5de15e',
          u'value': u'the_value'}]

        """
        # TODO: Return only the key names from all storages
        return self.db.search(Query().name.matches('.*'))

    def get(self, key_name):
        """Return a dictionary consisting of the key itself

        e.g.
        {u'created_at': u'2016-10-10 08:31:53',
         u'description': None,
         u'metadata': None,
         u'modified_at': u'2016-10-10 08:31:53',
         u'name': u'aws',
         u'uid': u'459f12c0-f341-413e-9d7e-7410f912fb74',
         u'value': u'the_value'}

        """
        result = self.db.search(Query().name == key_name)
        if not result:
            return {}
        return result[0]

    def delete(self, key_name):
        """Delete the key and return true if the key was deleted, else false
        """
        return self.db.remove(Query().name == key_name)


def init():
    storage = TinyDBStorage()
    return storage.init()


def load(table=None):
    storage = TinyDBStorage()
    return storage.db.table(table) if table else storage.db
