from .DatabaseConnection import DatabaseConnection
conn = DatabaseConnection()
class Request():
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
    def _create_request(userid,title,description):
        '''Post new request into the database'''
        conn.InsertQueryforRequest(userid,title,description)

    @staticmethod
    def _modify_request(requestid,field,newinput):
        '''Modify a request basing on given field'''
        conn.genericUpdateQueryforRequest(requestid,field,newinput)


    def __repr__(self):
        return 'the string is {} {} {} {}  '.format(self.id,self.userID,self.title,self.description)
    
class User():
    def __init__(self,userID,username,usertype,status,password=None):
        self.userID = userID
        self.username = username
        self.password = password
        self.type = usertype
        self.status = status

    def getUser(self):
        return {
        'userID':self.userID,
        'username':self.username,
        'type':self.usertype,
        'status':self.status
        }

    @staticmethod
    def createUser(email,password,usertype):
        conn.InsertQueryforUser(email,password,usertype)


    @staticmethod
    def login(email,password):
        if(conn.genericSelectQuery("user","email='"+email+"' AND password='"+password+"'")):
            conn.genericUpdateQueryforUser(email,password,"status","loggedin")
            return True

    @staticmethod
    def is_logged_in(id):
        '''Check if user is logged in'''
        if (conn.genericSelectQuery("user","id="+str(id)+" AND status='loggedin'")):
            return True

