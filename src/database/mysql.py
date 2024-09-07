from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import mysql.connector


class ConnectMySQL:
    def __init__(self, user, password, host, dbname):
        self._dbName = dbname
        self._conn = None
        self._cursor = None

        try:
            # Connecting to the MySQL server to create the database if it does not exist
            self._conn = mysql.connector.connect(
                user=user,
                password=password,
                host=host
            )
            self._cursor = self._conn.cursor(buffered=True)

            self.createDatabase()
        except mysql.connector.Error as err:
            print(f"Error connecting or creating database: {err}")
        finally:
            if self._cursor is not None:
                self._cursor.close()
            if self._conn is not None:
                self._conn.close()

        # Create SQLAlchemy engine for the database
        self._engine = create_engine(
            f'mysql+mysqlconnector://{user}:{password}@{host}/{dbname}')
        self.createSession()

    def createDatabase(self):
        # Execute the SQL command to create the database
        try:
            if self._cursor is not None:
                sql = f"CREATE DATABASE IF NOT EXISTS {self._dbName}"
                self._cursor.execute(sql)
                self._conn.commit()
        except mysql.connector.Error as err:
            print(f"Error creating database: {err}")

    def createSession(self):
        # Create the SQLAlchemy session
        Session = sessionmaker(bind=self._engine)
        self._session = Session()

    def closeConnection(self):
        # Close the SQLAlchemy session
        if hasattr(self, '_session'):
            print(f"Disconnecting MySQL `{self._dbName}`")
            self._session.close()
