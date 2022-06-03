from scripts.data_base import DataBase
from cassandra.auth import PlainTextAuthProvider
from cassandra.cluster import Cluster
import pandas as pd
from time import sleep

class CassandraDB(DataBase):
    
    def __init__(self):
        super().__init__()
        self.__cluster:Cluster = None
        self.__protocolVersion:int = 4
        self.__keyspace:str = ''
        self.__session = None
        self.__timeout = 60
        pass
    
    def __authProvider(self):
        return PlainTextAuthProvider(
            username = self.username,
            password = self.password)
    
    @property
    def protocolVersion(self)->int:
        return self.__protocolVersion
    
    @protocolVersion.setter
    def protocolVersion(self, protocolVersion:int):
        self.__protocolVersion = protocolVersion;
    
    @property
    def keyspace(self)->str:
        return self.__keyspace
    
    @keyspace.setter
    def keyspace(self, keyspace):
        self.__keyspace = keyspace        
        
    @property
    def timeout(self)->int:
        return self.__timeout
    
    @timeout.setter
    def timeout(self, timeout):
        self.__timeout = timeout
    
    @property
    def cluster(self) -> Cluster:
        return self.__cluster
    
    @property
    def session(self):
        return self.__session
    
    def connect(self):
        super().connect()
        self.__cluster = Cluster(
            self.hosts,
            protocol_version= self.protocolVersion, 
            auth_provider=self.__authProvider())
        self.__session = self.cluster.connect(self.keyspace)
        self.session.row_factory = lambda columns, rows: pd.DataFrame(rows, columns=columns)
        sleep(5)
        
    def execute(self, sql, timeout=None):      
        return self.session.execute(sql,timeout)._current_rows
        