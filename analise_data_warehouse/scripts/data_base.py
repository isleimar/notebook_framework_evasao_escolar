class DataBase:
    def __init__(self):
        self.__hosts = []
        self.__username:str = ''
        self.__password:str = ''        
        
    @property
    def hosts(self)->str:
        return self.__hosts
    
    @hosts.setter
    def hosts(self, hosts):
        self.__hosts = hosts
    
    @property
    def username(self)->str:
        return self.__username
    
    @username.setter
    def username(self, username:str):
        self.__username = username
    
    @property
    def password(self)->str:
        return self.__password
    
    @password.setter
    def password(self, password:str):
        self.__password = password        
    
    def connect(self):pass
    def execute(self, sql, timeout=None): pass
        