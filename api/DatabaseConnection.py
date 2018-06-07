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
        createTableUserquery = "CREATE TABLE public.user(id SERIAL PRIMARY KEY NOT NULL,email CHAR(50) NOT NULL UNIQUE,password CHAR(100) NOT NULL,type CHAR(50) NOT NULL,status CHAR(50) NOT NULL)"
        self.cursor.execute(createTableUserquery)

    def createTableRequest(self):
        createTableRequestquery = "CREATE TABLE public.request(id SERIAL PRIMARY KEY NOT NULL,userid INT NOT NULL references public.user(id),title CHAR(50) NOT NULL,description CHAR(50) NOT NULL,status CHAR(50) NOT NULL)"
        self.cursor.execute(createTableRequestquery)

    # def createTestTableUser(self):
    #     createTableUserquery = "CREATE TABLE public.testuser(id SERIAL PRIMARY KEY NOT NULL,email CHAR(50) NOT NULL UNIQUE,password CHAR(100) NOT NULL,type CHAR(50) NOT NULL,status CHAR(50) NOT NULL)"
    #     self.cursor.execute(createTableUserquery)

    # def createTestTableRequest(self):
    #     createTableRequestquery = "CREATE TABLE public.testrequest(id SERIAL PRIMARY KEY NOT NULL,userid INT NOT NULL references public.user(id),title CHAR(50) NOT NULL,description CHAR(50) NOT NULL UNIQUE,status CHAR(50) NOT NULL)"
    #     self.cursor.execute(createTableRequestquery)

    # def deleteTestTableUser(self):
    #     deleteTestTableUserquery = "DELETE FROM public.testuser"

    def genericSelectQuery(self,table,clause):
        if table=="user":
            selectQuery = "SELECT * From public.user WHERE "+clause
            self.cursor.execute(selectQuery)
            result = self.cursor.fetchall()
            result_list = []
            for record in result:
                result_list.append({
                    'id':record[0],
                    'email':record[1].strip(),
                    'password':record[2].strip(),
                    'type':record[3].strip(),
                    'status':record[4].strip()
                })
            # print result_list
            return result_list
        if table=="request":
            selectQuery = "SELECT * From public.request WHERE "+clause
            self.cursor.execute(selectQuery)
            result = self.cursor.fetchall()
            result_list = []
            for record in result:
                result_list.append({
                    'id':record[0],
                    'userid':record[1],
                    'title':record[2].strip(),
                    'description':record[3].strip(),
                    'status':record[4].strip()
                })
            return result_list

    def InsertQueryforUser(self,email,password,usertype,status='loggedout'):
        insertQuery = "INSERT INTO public.user (email,password,type,status) VALUES ('"+email+"','"+password+"','"+usertype+"','"+status+"')"
        self.cursor.execute(insertQuery)

    def InsertQueryforRequest(self,current_user,title,description,status='pending'):
        print (type(current_user))
        print(str(current_user))
        insertQuery = "INSERT INTO public.request (userid,title,description,status) VALUES ("+str(current_user)+",'"+title+"','"+description+"','"+status+"')"
        self.cursor.execute(insertQuery)

    def genericUpdateQueryforRequest(self,requestid,field,newinput):
        updateQuery = "UPDATE public.request SET "+field+" = '"+newinput+"' WHERE id="+str(requestid)
        self.cursor.execute(updateQuery)

    def genericUpdateQueryforUser(self,current_user,field,newinput):
        updateQuery = "UPDATE public.user SET "+field+" = '"+newinput+"' WHERE id="+str(current_user)
        self.cursor.execute(updateQuery)


# if __name__ == '__main__':
#     from werkzeug.security import generate_password_hash, check_password_hash
#     conn = DatabaseConnection()
#     conn.createTableUser()
#     conn.createTableRequest()
#     x=0
#     password = generate_password_hash("password")
#     while x<10:
#         x=x+1
#         if x%2 == 0:
#             conn.InsertQueryforUser("test@admin.com"+str(x),password,"admin")
#         else:
#             conn.InsertQueryforUser("test@user.com"+str(x),password,"user")