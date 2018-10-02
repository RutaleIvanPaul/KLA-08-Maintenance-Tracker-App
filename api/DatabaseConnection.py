import psycopg2
from pprint import pprint
from urllib.parse import urlparse
import os


class DatabaseConnection():
    # Class concerned with setting up a database connection
    # and all methods connecting and interacting with the database
    def __init__(self):
        parsed_url = urlparse(os.getenv('DATABASE_URL'))
        dbname = parsed_url.path[1:]
        username = parsed_url.username
        hostname = parsed_url.hostname
        pwd = parsed_url.password
        port_number = parsed_url.port
        try:
            self.connection = psycopg2.connect(
                host=hostname, database=dbname, user=username, password=pwd)
            self.connection.autocommit = True
            self.cursor = self.connection.cursor()
        except:
            pprint("Cannot Connect to Database")

    def createTableUser(self):
        '''Create the user table'''
        createTableUserquery = "CREATE TABLE public.user(id SERIAL PRIMARY KEY NOT NULL,email CHAR(50) NOT NULL UNIQUE,password CHAR(100) NOT NULL,type CHAR(50) NOT NULL,status CHAR(50) NOT NULL)"
        self.cursor.execute(createTableUserquery)

    def createTableRequest(self):
        '''Create the request table'''
        createTableRequestquery = "CREATE TABLE public.request(id SERIAL PRIMARY KEY NOT NULL,userid INT NOT NULL references public.user(id),title CHAR(50) NOT NULL,description CHAR(50) NOT NULL,status CHAR(50) NOT NULL)"
        self.cursor.execute(createTableRequestquery)

    def genericSelectQuery(self, table, clause):
        '''Serves as any kind of select query once given the table and clause'''
        if table == "user":
            selectQuery = "SELECT * From public.user WHERE "+clause
            self.cursor.execute(selectQuery)
            result = self.cursor.fetchall()
            result_list = []
            for record in result:
                result_list.append({
                    'id': record[0],
                    'email': record[1].strip(),
                    'password': record[2].strip(),
                    'type': record[3].strip(),
                    'status': record[4].strip()
                })
            # print result_list
            return result_list
        if table == "request":
            selectQuery = "SELECT * From public.request WHERE "+clause
            self.cursor.execute(selectQuery)
            result = self.cursor.fetchall()
            result_list = []
            for record in result:
                result_list.append({
                    'id': record[0],
                    'userid': record[1],
                    'title': record[2].strip(),
                    'description': record[3].strip(),
                    'status': record[4].strip()
                })
            return result_list

    def InsertQueryforUser(self, email, password, usertype, status='loggedout'):
        '''Generic insert query for user'''
        insertQuery = "INSERT INTO public.user (email,password,type,status) VALUES ('" + \
            email+"','"+password+"','"+usertype+"','"+status+"')"
        self.cursor.execute(insertQuery)

    def InsertQueryforRequest(self, current_user, title, description, status='pending'):
        '''Generic insert query for Request'''
        print(type(current_user))
        print(str(current_user))
        insertQuery = "INSERT INTO public.request (userid,title,description,status) VALUES ("+str(
            current_user)+",'"+title+"','"+description+"','"+status+"')"
        self.cursor.execute(insertQuery)

    def genericUpdateQueryforRequest(self, requestid, field, newinput):
        '''Generic update for request'''
        updateQuery = "UPDATE public.request SET "+field + \
            " = '"+newinput+"' WHERE id="+str(requestid)
        self.cursor.execute(updateQuery)

    def genericUpdateQueryforUser(self, current_user, field, newinput):
        '''Generic update query for user'''
        updateQuery = "UPDATE public.user SET "+field + \
            " = '"+newinput+"' WHERE id="+str(current_user)
        self.cursor.execute(updateQuery)

    def clearTables(self):
        self.cursor.execute("DELETE FROM public.request")
        self.cursor.execute("DELETE FROM public.user")
