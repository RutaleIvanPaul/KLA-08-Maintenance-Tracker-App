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
        return conn.genericSelectQuery('request','id='+str(id))

    @staticmethod
    def _get_all_user_requests(userID):
        '''Get user requests basing on user id'''
        return conn.genericSelectQuery('request','userid='+str(userID))        

    @staticmethod
    def _record_exists(title):
        '''Check whether request exists'''
        return [user_request for user_request in user_requests if user_request.title == title]


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
    def is_logged_in(id):
        '''Check if user is logged in'''
        if (conn.genericSelectQuery("user","id="+str(id)+" AND status='loggedin'")):
            return True

    


#create list of users
users = [User(1,'Ivan','admin','loggedin'),User(2,'Paul','user','loggedout'),User(3,'Ruts','user','loggedin')]

#logged in users
loggedIn = [2,4]

#user requests
user_requests = [Request(1,2,'laptop screen','the screen just suddenly blacked out','pending'),
                    Request(2,1,'phone screen cracked','the phone fell down','approved'),
                    Request(3,3,'pc over heat','pc over heats even on low activity','rejected')]
   
