import sqlite3


# allows for data to be selected from our main table 
class Database:

    def __init__(self , filename):
        if filename:
            self.fname = filename
        else:
            return None
        
    def get_data(self):
        con = sqlite3.connect(self.fname)
        cur = con.cursor()
        res = cur.execute("SELECT * FROM CoordinatesTable")
        data = res.fetchall()
        fields = [x[0] for x in cur.description]
        return data, fields
    
        

