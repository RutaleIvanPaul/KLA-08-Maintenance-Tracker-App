from .DatabaseConnection import DatabaseConnection
from werkzeug.security import generate_password_hash, check_password_hash
conn = DatabaseConnection()
class Request():
    #Class to model the behaviour of a request
    def __init__(self,id,userID,title,description,status):
        self.id = id
        self.userID = userID
        self.title = title
        self.description = description
        self.status = status
    
    def getRequest(self):
        return { 
        'id': self.id,
        'userID':self.userID,
        'title':self.title,
        'description':self.description
        }

    @staticmethod
    def _get_request(id):
        '''Get user request basing on request id'''
        if id == "get_all":
            return conn.genericSelectQuery('request','true')
        else:
            return conn.genericSelectQuery('request','id='+str(id))

    @staticmethod
    def _get_all_user_requests(userID):
        '''Get user requests basing on user id'''
        return conn.genericSelectQuery('request','userid='+str(userID))        

    @staticmethod
    def _record_exists(title):
        '''Check whether request exists'''
        return conn.genericSelectQuery('request',"title='"+title+"'")

    @staticmethod
    def _create_request(current_user,title,description):
        '''Post new request into the database'''
        conn.InsertQueryforRequest(current_user,title,description)
        return conn.genericSelectQuery("request",'userid='+str(current_user))[-1]

    @staticmethod
    def _modify_request(requestid,field,newinput):
        '''Modify a request basing on given field'''
        conn.genericUpdateQueryforRequest(requestid,field,newinput)


    def __repr__(self):
        return 'the string is {} {} {} {}  '.format(self.id,self.userID,self.title,self.description)
    
class User():
    #Class to model the behaviour of a User
    def __init__(self,userID,username,usertype,status,password=None):
        self.userID = userID
        self.username = username
        self.password = password
        self.type = usertype
        self.status = status
    
    @staticmethod
    def getUser(userid):
        '''Get the user basing on userid'''
        return conn.genericSelectQuery("user","id="+str(userid))

    @staticmethod
    def getUserbyEmail(email):
        '''Get the user basing on email'''
        return conn.genericSelectQuery("user","email='"+email+"'")

    @staticmethod
    def createUser(email,password,usertype):
        '''Create User when given email, password and usertype'''
        conn.InsertQueryforUser(email,password,usertype)


    @staticmethod
    def login(userid,password):
        '''Change user status to logged in'''
        row = conn.genericSelectQuery("user","id="+str(userid))[0]
        if(check_password_hash(row["password"],password)):
            conn.genericUpdateQueryforUser(userid,"status","loggedin")
            return True

    @staticmethod
    def logout(current_user,logout):
        '''change user status to logged out'''
        conn.genericUpdateQueryforUser(current_user,"status","loggedout")
        return True

    
    @staticmethod
    def is_logged_in(id):
        '''Check if user is logged in'''
        if (conn.genericSelectQuery("user","id="+str(id)+" AND status='loggedin'")):
            return True

