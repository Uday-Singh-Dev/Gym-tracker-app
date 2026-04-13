import sqlite3
import json
import bcrypt
from datetime import datetime

class ExerciseDatabase:
    def __init__(self):
        #connect to database
        self.conn = sqlite3.connect("Exercises.db")
        self.cursor = self.conn.cursor()
        #creates the table if it dosent exists
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS Exercises (
                            exercise text,
                            image text,
                            muscles_targeted text,
                            intensity_trained text,
                            description text,
                            built_in text
                            )""")
    def add_exercise(self,exercise,image,muscles_targeted,intensity_trained,description,built_in):
        #function to add exercise
        muscles_targeted= json.dumps(muscles_targeted)
        intensity_trained = json.dumps(intensity_trained)
        #select an exercise with the exercise name given. If it exists already will then return
        self.cursor.execute("SELECT * FROM Exercises WHERE exercise = ?", (exercise,))
        data = self.cursor.fetchone()
        if data is not None:
            print("EXERCISE ALREADY EXISTS")
            return
        #If no entry in then we can add all the values
        self.cursor.execute("INSERT INTO Exercises VALUES(?,?,?,?,?,?)",(exercise,image,muscles_targeted,intensity_trained,description,built_in))
        #save
        self.conn.commit()
    def delete_exercise(self,exercise):
        #delete all the fields where the exercise = exercise input given
        self.cursor.execute("DELETE FROM Exercises WHERE exercise = ?",(exercise,))
        self.conn.commit()

    def take_info(self, key, exercise):
        #takes a single key from an exercise
        allowed_keys = {"exercise", "image", "muscles_targeted", "intensity_trained", "description","built_in"}
        if key not in allowed_keys:
            raise ValueError(f"Invalid column: {key}")
        
        self.cursor.execute(f"SELECT {key} FROM Exercises WHERE exercise = ?", (exercise,))
        data = self.cursor.fetchone()
        #if keys are arrays then will convert back into array from strings
        json_convert_keys = {"muscles_targeted", "intensity_trained"}
        if key in json_convert_keys:
            return json.loads(data[0])
        
        return data[0] if data else None
    
    def take_all_info(self,INPUT):
        #takes all info where the input is in the exercise name
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
                            workouts text,
                            workout_data text,
                            workout_history text
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
        #scrambles the password
        scrambled = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        #set workouts,history,data to dictionary
        self.workouts  = {}
        self.workout_data = {}
        self.workout_history = {}
        #convert to strings so it can be stored
        workouts = json.dumps(self.workouts)
        workout_data = json.dumps(self.workout_data)
        workout_history = json.dumps(self.workout_history)


        #write a new row to the database
        self.cursor.execute("INSERT INTO Users VALUES(?,?,?,?,?)",(username,scrambled,workouts,workout_data,workout_history))
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
        login_success = bcrypt.checkpw(password.encode(),rows[1].encode())
        if login_success == False:
            return "Incorrect password"


        #set all data to vars
        self.username = rows[0]
        self.password = rows[1]
        self.workouts = json.loads(rows[2])
        self.workout_data = json.loads(rows[3])
        self.workout_history = json.loads(rows[4])
        
        return "logged in successfully"
        
    def get_progression(self, exercise_name,key):
        # returns list of (date_string, max_weight) sorted by date
        progression = []
        print(self.workout_history)
        for date, session in self.workout_history.items():
            if exercise_name not in session:
                continue
            weights = session[exercise_name].get(key, [])
            try:
                max_w = max(int(w) for w in weights if w != 0)
            except ValueError:
                continue
            progression.append((date, max_w))
        # sort by parsed date
        progression.sort(key=lambda x: datetime.strptime(x[0], "%A %d %B %Y, %H:%M"))
        return progression

