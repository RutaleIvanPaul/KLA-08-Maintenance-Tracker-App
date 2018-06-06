import psycopg2
from pprint import pprint

class DatabaseConnection():
    def __init__(self):
        try:
            self.connection = psycopg2.connect(host="localhost",database="maintenance_tracker", user="postgres", password="RIp0772466608*")
            self.connection.autocommit = True
            self.cursor = self.connection.cursor()
        except:
            pprint("Cannot Connect to Database")
    
    def createTableUser(self):
        createTableUserquery = "CREATE TABLE public.user(id SERIAL PRIMARY KEY NOT NULL,email CHAR(50) NOT NULL UNIQUE,password CHAR(50) NOT NULL,type CHAR(50) NOT NULL,status CHAR(50) NOT NULL)"
        self.cursor.execute(createTableUserquery)

    def createTableRequest(self):
        createTableRequestquery = "CREATE TABLE public.request(id SERIAL PRIMARY KEY NOT NULL,userid INT NOT NULL references public.user(id),title CHAR(50) NOT NULL,description CHAR(50) NOT NULL UNIQUE,status CHAR(50) NOT NULL)"
        self.cursor.execute(createTableRequestquery)

    def genericSelectQuery(self,table,clause):
        if table=="user":
            selectQuery = "SELECT * From public.user WHERE "+clause
            self.cursor.execute(selectQuery)
            result = self.cursor.fetchall()
            result_list = []
            for record in result:
                result_list.append({
                    'id':record[0],
                    'email':record[1],
                    'type':record[3],
                    'status':record[4]
                })
            return result_list
        if table=="request":
            selectQuery = "SELECT * From public.request WHERE "+clause
            self.cursor.execute(selectQuery)
            result = self.cursor.fetchall()
            result_list = []
            for record in result:
                result_list.append({
                    'userid':record[1],
                    'title':record[2],
                    'description':record[3],
                    'status':record[4]
                })
            return result_list

    def InsertQueryforUser(self,email,password,usertype,status='loggedout'):
        insertQuery = "INSERT INTO public.user (email,password,type,status) VALUES ('"+email+"','"+password+"','"+usertype+"','"+status+"')"
        self.cursor.execute(insertQuery)

    def InsertQueryforRequest(self,userid,title,description,status='pending'):
        insertQuery = "INSERT INTO public.request (userid,title,description,status) VALUES ('"+userid+"','"+title+"','"+description+"','"+status+"')"
        self.cursor.execute(insertQuery)

    def genericUpdateQueryforRequest(self,requestid,field,newinput):
        updateQuery = "UPDATE public.request SET "+field+" = '"+newinput+"' WHERE id="+str(requestid)
        self.cursor.execute(updateQuery)

    def genericUpdateQueryforUser(self,email,password,field,newinput):
        updateQuery = "UPDATE public.user SET "+field+" = '"+newinput+"' WHERE email='"+email+"'AND password='"+password+"'"
        self.cursor.execute(updateQuery)
