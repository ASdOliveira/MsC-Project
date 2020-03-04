import sqlite3

#Criar metodos de criar table e delete table

class db():
    def __init__(self,name):
        self.db_name = str(name) + ".db"
        self.table = str(name)

    #create a Db
    def create_db(self):
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()

        sql_command = """
        CREATE TABLE {0}( 
        staff_number INTEGER PRIMARY KEY, 
        lat real, 
        long real, 
        vel real, 
        accel real);""".format(self.table)

        cursor.execute(sql_command)
        connection.close()


    #Lat, Lon, Vel, accel., 
    def insert(self, Lat, Long, Vel, Accel):
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()

        sql_command = """INSERT INTO {0}(staff_number, {1}, {2}, {3}, {4})
            VALUES (NULL, {5}, {6}, {7}, {8});""".format(self.table,'lat','long','vel','accel',str(Lat),str(Long),str(Vel),str(Accel))
        cursor.execute(sql_command)
        connection.commit()
        connection.close()

    def fetch_all(self):
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        sql_command = """SELECT * FROM {0}""".format(self.table)
        cursor.execute(sql_command)
        return cursor.fetchall()

    def fetch_one(self):
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        sql_command = """SELECT * FROM {0}""".format(self.table)
        cursor.execute(sql_command)
        return cursor.fetchone()
        






