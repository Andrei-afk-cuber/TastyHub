class User(object):
    def __init__(self, username, password, admin=False):
        self.__username = username
        self.__password = password
        self.__admin = admin

    def getUsername(self):
        return self.__username

    def getPassword(self):
        return self.__password

    def getAdmin(self):
        return self.__admin

    def setUsername(self, login):
        self.__username = login

    def setPassword(self, password):
        self.__password = password

    def setAdmin(self, admin):
        self.__admin = admin