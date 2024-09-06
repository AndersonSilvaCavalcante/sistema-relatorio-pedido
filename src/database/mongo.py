from pymongo import MongoClient

class ConnectMongo:
    def __init__(self, dbname):
        self._dbName = dbname
        self._conn = MongoClient("mongodb://localhost")
        self._db = self._conn[dbname]

    def createCollection(self, name):
        return self._db[name]

    def useCollection(self, name):
        return self._db[name]

    def closeConnection(self):
        print(f"disconnecting MongoDB `{self._dbName}`")
        self._conn.close()
