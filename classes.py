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

class Recipe(object):
    def __init__(self, name, description, picture_path, cooking_time = 0, product_list=[], confirmed=False):
        self.__name = name
        self.__description = description
        self.__cooking_time = cooking_time
        self.__product_list = product_list
        self.__confirmed = confirmed
        self.__pciture_path = picture_path

    def getName(self):
        return self.__name

    def getDescription(self):
        return self.__description

    def getCookingTime(self):
        return self.__cooking_time

    def getProductList(self):
        return self.__product_list

    def setName(self, name):
        self.__name = name

    def setDescription(self, description):
        self.__description = description

    def setCookingTime(self, cooking_time):
        self.__cooking_time = cooking_time

    def setProductList(self, product_list):
        self.__product_list = product_list

    def getConfirmed(self):
        return self.__confirmed

    def setConfirmed(self, confirmed):
        self.__confirmed = confirmed

    def getPciturePath(self):
        return self.__pciture_path

    def setPciturePath(self, pciture_path):
        self.__pciture_path = pciture_path