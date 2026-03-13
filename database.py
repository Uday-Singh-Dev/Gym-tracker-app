import sqlite3
import json



class ExerciseDatabase:
    def __init__(self):
        self.conn = sqlite3.connect("Exercises.db")
        self.cursor = self.conn.cursor()

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS Exercises (
                            exercise text,
                            image text,
                            muscles_targeted text,
                            intensity_trained text,
                            description text
                            )""")
    def add_exercise(self,exercise,image,muscles_targeted,intensity_trained,description):

        muscles_targeted = json.dumps(muscles_targeted)
        intensity_trained = json.dumps(intensity_trained)

        self.cursor.execute("SELECT * FROM Exercises WHERE exercise = ?", (exercise,))
        data = self.cursor.fetchone()
        if data is not None:
            print("EXERCISE ALREADY EXISTS")
            return
        
        self.cursor.execute("INSERT INTO Exercises VALUES(?,?,?,?,?)",(exercise,image,muscles_targeted,intensity_trained,description))
        self.conn.commit()

    def take_info(self, key, exercise):
        allowed_keys = {"exercise", "image", "muscles_targeted", "intensity_trained", "description"}
        if key not in allowed_keys:
            raise ValueError(f"Invalid column: {key}")
        
        self.cursor.execute(f"SELECT {key} FROM Exercises WHERE exercise = ?", (exercise,))
        data = self.cursor.fetchone()
        
        json_convert_keys = {"muscles_targeted", "intensity_trained"}
        if key in json_convert_keys:
            return json.loads(data[0])
        
        return data[0] if data else None
    
    def take_all_info(self,INPUT):
        self.cursor.execute(f"SELECT * FROM Exercises WHERE exercise LIKE ?", (f"%{INPUT}%",))
        data = self.cursor.fetchall()
        return data
                            
                           


class DataManager:
    def __init__(self):
        #create/connect to the user database
        self.conn = sqlite3.connect("Users.db")
        self.cursor = self.conn.cursor()

        #creates the table if it dosent exist
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS Users (
                            username text,
                            password text,
                            workouts text
                            )""")

        

    def new_save(self,username,password):
        #change username to lowercase
        username = username.lower()
        
        
        #check if inputs are there
        if username == "" or password == "":
            return "Input a username and password"
        self.cursor.execute("SELECT * FROM Users WHERE username = ?",(username,))
        rows = self.cursor.fetchone()
        if rows != None:
            return "Username in use"


        #temporary until i make the workouts editor.

        self.workouts  = {
            "push day": {
                "cable_tricep_pushdown": {
                    "sets": 0,
                    "reps": 0,
                    "weight": 0
                }
            },                          
            "pull day": {
                "weighted_pullups": {
                    "sets": 0,
                    "reps": 0,          
                    "weight": 0
                }
            }
        }

        #convert the data into string so it can be saved
        workouts = json.dumps(self.workouts)

        #write a new row to the database
        self.cursor.execute("INSERT INTO Users VALUES(?,?,?)",(username,password,workouts))
        self.conn.commit()

        self.username = username
        self.password = password

        
        return "account created"
    
    def save_data(self,username,key,data):
        #turns the data in a string file because all the data being saved will be classes
        data_string = json.dumps(data)
        #then finds the row with matching username and sets the keys data to the data string
        self.cursor.execute(f"UPDATE Users SET {key} = ? WHERE username = ?", (data_string,username))
        #save the changes
        self.conn.commit()

    def load_data(self,username,password):
        #checks if null input
        if username == "" or password == "":
            return "input a username or password"

        #converts to lower
        username = username.lower()
        #finds the row where the username column is = the username input
        self.cursor.execute("SELECT * FROM Users WHERE username = ?", (username,))

        #fetches that data
        rows = self.cursor.fetchone()

        #if row is none means didnt find the username
        if rows is None:
            return "Username not found"
        #username found but password incorrect
        if rows[1] != password:
            return "Incorrect password"


        #set all data to vars
        self.username = rows[0]
        self.password = rows[1]
        self.workouts = json.loads(rows[2])

        
        return "logged in successfully"
        
