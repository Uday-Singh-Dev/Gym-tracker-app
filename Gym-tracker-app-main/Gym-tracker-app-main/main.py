import customtkinter as ctk
from datetime import datetime,timedelta
from PIL import Image
from database import DataManager
from database import ExerciseDatabase
import os
import json
import time
from fpdf import FPDF
import matplotlib.pyplot as plt
 
 
 
#Setting appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
 
#Default app size
APP_SIZE = "800x800"
APP_WIDTH, APP_HEIGHT = 800, 800
 
#'setting app title and geometry
app = ctk.CTk()
app.title("Rep Registry")
app.geometry(APP_SIZE)
 
#COLOUR USED
TEXT_COLOR = "#000000"
TEXT_COLOR2 = "#4C5156"
TEXT_COLOR3 = "#333844"
TEXT_COLOR4 = "#8D8E93"
POSITIVE_COLOR = "#698876"
NEGATIVE_COLOR = "#C0ACAB"
APP_BG = "#FFFFFF"
PANEL_BG = "#F0F0F0"
PRIMARY_BLUE = "#4B709D"
BUTTON_BG_NORMAL = "#2C2C2C"
BUTTON_BG_HOVER = "#1F1F1F"
BUTTON_BG_CLICKED = "#0F0F0F"
 
 
class Objects():
    #Static method class used to simplify lengthy code allowing for consistant design throughout the program.
    @staticmethod
    def label(parent, text, x, y, w, h, size, text_color=TEXT_COLOR, bold=True, panel_color=APP_BG):
        #Creates a label taking in the parameters
        font_styles = "bold" if bold else "normal"
        font = ("Arial", size, font_styles)
        
        label = ctk.CTkLabel(
            parent,
            text=text,
            font=font,
            text_color=text_color,
            bg_color=panel_color
        )
        #Modifys width and height if inputed into the function
        if w is not None:
            label.configure(width=w)
        if h is not None:
            label.configure(height=h)
 
        #Use x and y placing if it is not None
        if x is not None and y is not None:
            label.place(x=x, y=y)
        #returns the label so extra modifcations can be made or needed for another use
        return label
 
    @staticmethod
    def panel(parent, x, y, w, h, bg_color=PANEL_BG):
        #Creates a CTK panel to hold information
        panel = ctk.CTkFrame(
            parent,
            width=w,
            height=h,
            fg_color=bg_color,
            corner_radius=0,
            border_width=2.5,
            border_color="black"
        )
        if x is not None and y is not None:
            panel.place(x=x, y=y)
 
        return panel
 
    @staticmethod
    def button(parent, x, y, w, h, text, text_size, corner_radius, bg_color, text_color="#FFFFFF", bg_normal=BUTTON_BG_NORMAL, bg_hover=BUTTON_BG_HOVER, bg_clicked=BUTTON_BG_CLICKED, bold=True, callback=None):
 
        #Creates a CTK button 
        font_style = "bold" if bold else "normal"
        font = ("arial", text_size, font_style)
 
        button = ctk.CTkButton(parent, text=text, width=w, height=h, fg_color=bg_normal, hover_color=bg_hover, bg_color=bg_color, text_color=text_color, font=font, corner_radius=corner_radius, command=callback)
 
        #Animates the button so the color is changed once the button is pressed
        def on_press(event):
            button.configure(fg_color=bg_clicked)
        #Returns the original color once the button isnt pressed
        def on_release(event):
            button.configure(fg_color=bg_normal)
 
        #Binds the functions to the button
        button.bind("<ButtonPress-1>", on_press)
        button.bind("<ButtonRelease-1>", on_release)
 
        
        if x is not None and y is not None:
            button.place(x=x, y=y)
        return button
 
    @staticmethod
    def graphical_button(parent, w, h, x, y, image, image_hover, image_clicked, callback=None):
        #A button except can use a PNG
 
        #Create the images for all three states
        image = ctk.CTkImage(Image.open(image), size=(w, h))
        image_hover = ctk.CTkImage(Image.open(image_hover), size=(w, h)) if image_hover else image
        image_clicked = ctk.CTkImage(Image.open(image_clicked), size=(w, h)) if image_clicked else image
        
        button = ctk.CTkButton(parent, image=image, text="", width=w, height=h, command=callback)
 
        # Checks if other images were given.
        if image_hover and image_clicked is None:
            button.configure(fg_color="white", hover_color="black")
        else:
            # If other images are given, keep background transparent
            button.configure(fg_color="transparent")
 
        def on_press(event):
            button.configure(image=image_clicked)
 
        def revert(event):
            button.configure(image=image)
        #When mouse enters button image changes image.
        def on_hover(event):
            button.configure(image=image_hover)
 
        button.bind("<Enter>", on_hover)
        button.bind("<Leave>", revert)
        button.bind("<ButtonPress-1>", on_press)
        button.bind("<ButtonRelease-1>", revert)
 
        if x is not None and y is not None:
            button.place(x=x, y=y)
 
        return button
 
    @staticmethod
    def graphic(parent, x, y, w, h, image):
        #Creates an image on the screen
        graphic = ctk.CTkImage(dark_image=Image.open(image), size=(w, h))
        graphic_label = ctk.CTkLabel(parent, image=graphic, text="")
        if x is not None and y is not None:
            graphic_label.place(x=x, y=y)
        return graphic_label
 
    @staticmethod
    def text_box(parent, x, y, w, h, p_text):
        #Text box is used to get user input. A box where the user can type into
        text_box = ctk.CTkEntry(parent, placeholder_text=p_text, width=w, height=h)
        if x is not None and y is not None:
            text_box.place(x=x, y=y)
        return text_box
 
    @staticmethod
    def info_panel(parent, w, h, text, text_color):
        #Used just for long sentences that need to be indented
        words = text.split()
        quarter = len(words) // 4
        line1 = " ".join(words[:quarter])
        line2 = " ".join(words[quarter:quarter*2])
        line3 = " ".join(words[quarter*2:quarter*3])
        line4 = " ".join(words[quarter*3:])
        text = line1 + "\n" + line2 + "\n" + line3 + "\n" + line4
        panel1 = Objects.panel(parent=parent, x=None, y=None, w=w, h=h)
        text1 = Objects.label(parent=panel1, x=None, y=None, w=None, h=None, size=10, text_color=text_color, text=text)
        text1.pack()
        return panel1
 
    @staticmethod
    def workout_box(parent, workout, w, h, sets, relx, rely, workout_start, timer_location, workout_name):
        #specific method used for the workout section of the code. This code gathers the data and builds the sets according to the data
 
        #Create empty arrays to eventually store all the weight and rep entrys given
        weight_arr = []
        reps_arr = []
        for i in range(sets):
            #Make a panel
            bg = Objects.panel(parent=parent, x=None, y=None, w=w, h=h, bg_color=PANEL_BG)
            bg.clicked = False
            bg.pack(fill="x", pady=3, padx=5)
 
            #To determine which set is which
            frame_count_circle = ctk.CTkFrame(bg, width=30, height=30, fg_color=APP_BG, corner_radius=0)
            frame_count_circle.pack(side="left", padx=5, pady=5)
            frame_count_text = Objects.label(parent=frame_count_circle, text=i+1, x=None, y=None, w=30, h=30, size=12)
            frame_count_text.place(relx=0.5, rely=0.5, anchor="center")
 
            #Input box for receving data
            weight_input_box = Objects.text_box(bg, x=None, y=None, w=80, h=30, p_text="weight")
            weight_input_box.pack(side="left", padx=5, pady=5)
            #input box for receving reps data
            rep_input_box = Objects.text_box(bg, x=None, y=None, w=80, h=30, p_text="reps")
            rep_input_box.pack(side="left", padx=5, pady=5)
 
 
            
            def workout_completed(object1, weight_input, reps_input, turn, workout_name):
                #This function is called when the user presses the tick button indicating the set has been finished
 
                #Prevents the user from clicking the button twice
                if object1.clicked:
                    return
                object1.clicked = True
 
                
                object1.configure(fg_color="#90EE90")
 
                #When workout is completed Rest timer must start
                APP.start_timer(timer_location, workout_name)
 
                #Gets the input
                weight = weight_input.get()
                #If 0 input given sets to 0
                if weight == "":
                    weight = 0
                weight_arr.append(weight)
 
                reps = reps_input.get()
                if reps == "":
                    reps = 0
                reps_arr.append(reps)
 
                
                #Checks for the PRS in the users personal best for that exercise comparing them with weight and reps.
                PRS = APP.compare_values(workout_name, weight, reps)
                parent = APP.secoundary_window("GOAL REACHED", 200, 300)
                if PRS[0] == True:
                    #Checks if weight for that exercise has been surpassed and displays a message for the user
                    text1 = Objects.label(parent=parent, x=None, y=None, w=None, h=None, size=12, text_color=TEXT_COLOR, text="Weight Surpassed")
                    text1.pack(pady=2)
                if PRS[1] == True:
                    text2 = Objects.label(parent=parent, x=None, y=None, w=None, h=None, size=12, text_color=TEXT_COLOR, text="Reps Surpassed")
                    text2.pack(pady=2)
                if PRS[2] == True:
                    text3 = Objects.label(parent=parent, x=None, y=None, w=None, h=None, size=12, text_color=TEXT_COLOR, text="Volume Surpassed")
                    text3.pack(pady=2)
                if int(reps) >= 12:
                    #Checks if the user has gotten 12 or more reps which means they can increase the weight.
                    new_weight = int(weight) + 2.5
                    text4 = Objects.label(parent=parent, x=None, y=None, w=None, h=None, size=12, text_color=TEXT_COLOR, text=f"Reps mastered increase the weight to {new_weight})")
                    text4.pack(pady=2)
                #Destroys the secoundary screen because no PRS have been or the reps havent hit 0 so no message needs to be displayed   
                if not any(PRS) and int(reps) < 12:
                    parent.destroy()
            #Only display tick button once the workout has been started   
            if workout_start:
                tick_button = Objects.graphical_button(bg, w=40, h=40, x=None, y=None, image="Graphics/tick.png", image_hover="Graphics/tick_hover.png", image_clicked="Graphics/tick_pressed.png", callback=lambda bg_=bg, w=weight_input_box, r=rep_input_box, turn=i, wn=workout_name: workout_completed(bg_, w, r, turn, wn))
                tick_button.pack(side="right", padx=5, pady=5)
        #Return all the weight and reps that have been logged.
        return weight_arr, reps_arr
 
 
 
    
 
    @staticmethod
    def scrollable_frame(parent, w, h):
        #A scrollable frame to scroll through items put on the frame
        scrollable_frame = ctk.CTkScrollableFrame(parent, width=w, height=h)
        return scrollable_frame
 
 
class Running:
    def __init__(self):
        #Main class
 
        #Initialize to prevent errors
        self.current_screen = None
        self.current_workout = None
 
        #Call classes from sqlite3 py file
        self.datamanager = DataManager()
        self.exercisedatabase = ExerciseDatabase()
 
        #Initialise workout
        self.WORKOUT_START = False
 
        #Create all the different screens in the app
        self.mainmenu_screen = ctk.CTkFrame(app, width=APP_WIDTH, height=APP_HEIGHT, fg_color=APP_BG)
        self.entry_screen = ctk.CTkFrame(app, width=500, height=700, fg_color=APP_BG)
        self.signup_screen = ctk.CTkFrame(app, width=400, height=500, fg_color=APP_BG)
        self.login_screen = ctk.CTkFrame(app, width=400, height=500, fg_color=APP_BG)
        self.workout_screen = ctk.CTkFrame(app, width=520, height=800, fg_color="#2B2B2B")
        self.workout_history_screen = ctk.CTkFrame(app,width=350,height =500,fg_color=APP_BG)
        self.custom_screen = ctk.CTkFrame(app,width=350,height=500,fg_color = APP_BG)
        self.muscle_analysis_screen = ctk.CTkFrame(app,width=350,height=500,fg_color = APP_BG)
        #Builds the entry screen
        self.build_entry(self.entry_screen)
 
        #Dictionary storing data about screen and information to call functions for them. Used to easily loop through screens and calling specific functions to avoid extra code
        self.screen_dictionary = {
            "mainmenu": [self.mainmenu_screen, 800, 800, "dashboard", app, self.build_mainmenu],
            "entry": [self.entry_screen, 500, 700, "entry", app, self.build_entry],
            "signup": [self.signup_screen, 400, 500, "signup", app, self.build_signup],
            "login": [self.login_screen, 400, 500, "login", app, self.build_login],
            "workout": [self.workout_screen, 520, 800, "workout", app, self.build_workout],
            "workout_history":[self.workout_history_screen, 350, 500, "workout_history", app, self.build_workout_history],
            "custom":[self.custom_screen, 350, 500, "custom", app, self.build_custom],
            "muscle_analysis":[self.muscle_analysis_screen, 350, 500, "muscle_analysis", app, self.build_muscle_analysis]
        }
 
        
    #Function to change the screen
    def update_screen(self, screen):
        #Checks if current screen is on and removes it
        if self.current_screen:
            self.current_screen.place_forget()
 
        #Loops through all the items in the dictionary
        for screen_list in self.screen_dictionary.values():
            #gets the screen
            frame = screen_list[0]
            #checks and then calls the function to destroy all the items in that screen
            if frame is not None:
                self.destroy_widgets(frame)
        #Loops through all the names of screen and then has the corresponding items
        for name, screen_list in self.screen_dictionary.items():
            #Loops through all screen names till it matches the input given
            if name == screen:
                #Configures the window based on that screen. the screen, Width,Height,Title
                self.window_configure(screen_list[4], screen_list[1], screen_list[2], screen_list[3])
                # Call the build function if it exists
                if screen_list[5] is not None:
                    #Builds the screen
                    screen_list[5](screen_list[0])
                #Places the screen
                screen_list[0].place(x=0, y=0)
                #Sets current screen to the screen being displayed
                self.current_screen = screen_list[0]
 
    def window_configure(self, screen, w, h, name):
        #Configures name width and height of screen
        screen.geometry(str(w) + "x" + str(h))
        screen.title(name)
 
    def secoundary_window(self, title, w, h):
        #A secoundary window to display extra information, errors
 
        #Try to destroy the popup if it exists
        try:
            self.popup.destroy()
        except:
            pass
        #Create popup
        self.popup = ctk.CTkToplevel(app)
        #Puts popup above
        self.popup.attributes('-topmost', True)
        #Change popup geometry and title
        self.window_configure(self.popup, w, h, title)
        self.popup.geometry(f"{w}x{h}+960+540")
        return self.popup
 
    def handle_signup(self):
        #Gets the inputs 
        username = self.signup_username_input.get()
        password = self.signup_password_input.get()
 
        #calls new save which returns strings to determine whether sign up was successfull or not
        error = self.datamanager.new_save(username, password)
 
        #If account creation was successfull takes the user to the mainmenu
        if error == "account created":
            self.update_screen("mainmenu")
            return
        #Creates popup and displays the error message is sign in wasnt successfull
        self.popup = self.secoundary_window("ERROR", 300, 200)
        text1 = Objects.label(parent=self.popup, x=None, y=None, w=None, h=None, size=14, text_color=TEXT_COLOR, text=error)
        text1.place(relx=0.5, rely=0.5, anchor="center")
 
    def handle_login(self):
        #Same concept as handle signup 
        username = self.login_username_input.get()
        password = self.login_password_input.get()
 
        error = self.datamanager.load_data(username, password)
 
        if error == "logged in successfully":
            self.build_mainmenu(self.mainmenu_screen)
            self.build_workout_history(self.workout_history_screen)
            self.build_muscle_analysis(self.muscle_analysis_screen)
            self.update_screen("mainmenu")
            return
        self.popup = self.secoundary_window("ERROR", 200, 200)
        text1 = Objects.label(parent=self.popup, x=None, y=None, w=None, h=None, size=14, text_color=TEXT_COLOR, text=error)
        text1.place(relx=0.5, rely=0.5, anchor="center")
 
    def destroy_widgets(self, parent):
        #Destroys all the widgets of a screen
        for widget in parent.winfo_children():
            widget.destroy()
            
    def check_plateau(self, progression, window=3):
        #extracts all the secound items of progression and if all three are the same plateau is true
        if len(progression) < window:
            return False
        recent = [w for _, w in progression[-window:]]
        return max(recent) == min(recent)
    
    def calculate_strength_increase(self, progression):
        #checks if enough sessions to compare
        if len(progression) < 2:
            return 0  
 
        # Gets the number of items in progression
        total = len(progression)
        # Finds the latest weight
        latest = progression[total - 1][1]
        # Finds the weight for previous session
        previous = progression[total - 2][1]
        
        #guard
        if previous == 0:
            return 0
 
        # Calculate the percentage increase of weight for that exercise since the last session
        percentage_increase = ((latest - previous) / previous) * 100
        return percentage_increase
    
    def calculate_muscles_worked(self):
        #Calculates which muscles are being worked and to what extent
        monthly_exercises = {}
        now = datetime.now()
        #Gets all the dates in the dictionary       
        for date_string, session in self.datamanager.workout_history.items():
            #strptime date in order to compare
            date = datetime.strptime(date_string, "%A %d %B %Y, %H:%M")
            #Finds all the data for the muscles worked in the current month
            if date.month == now.month and date.year == now.year:
                #Then takes the exercise and the exercise data from sessions
                for exercise, data in session.items():
                    #Passes on duration
                    if exercise == "duration":
                        continue
                    #adds the exercise and its data to the months exercise dict
                    if exercise not in monthly_exercises:
                        monthly_exercises[exercise] = []
                    monthly_exercises[exercise].append(data)
        #Creates arrays for the muscles and intensitys worked
        muscles_worked = []
        intensity_worked = []
 
        #Now gets the exercise in the monthly_exercise dictionary
        for exercise in monthly_exercises.keys():
            #Then stores the result of the muscles targeted from that exercise and the intensity those muscles are trained from that exercise
            muscles_worked.append(self.exercisedatabase.take_info("muscles_targeted", exercise))
            intensity_worked.append(self.exercisedatabase.take_info("intensity_trained", exercise))
 
        #Returns these two arrays
        return muscles_worked, intensity_worked
 
    
    def workout_frequency(self):
        #Gets current time
        now = datetime.now()
        #Intialise training sessions being down per week and month
        week_count = 0
        month_count = 0
 
        for date_string in self.datamanager.workout_history:
            date = datetime.strptime(date_string, "%A %d %B %Y, %H:%M")
 
            #Checks if month is same as current month and the year
            if date.month == now.month and date.year == now.year:
                #Adds one session to the month count
                month_count +=1
            #Checks if week is the same
            if date.isocalendar().week == now.isocalendar().week:
                week_count += 1 
 
 
        return week_count, month_count  # return both counters
 
    
    def check_workout_fatigue(self):
        #Current time
        now = datetime.now()
        #Initialise the workouts done today
        workouts_today = 0
 
        #Loops throuhh all the dates in workout_history
        for date_string in self.datamanager.workout_history:
            date = datetime.strptime(date_string, "%A %d %B %Y, %H:%M")
            #If the day the session was recorded is the same day as today workouts today is increased by 1
            if date.day == now.day and date.month == now.month and date.year == now.year:
                workouts_today += 1
        #If workouts above 3 Warning message will be displayed to the user
        if workouts_today >= 3:
            return True
        return False
 
    def workout_streak(self):
        #Intialise streak
        streak = 1
 
        #Gets all the dates from sessions that have been recorded
        dates_worked = [
            datetime.strptime(d, "%A %d %B %Y, %H:%M")
            for d in self.datamanager.workout_history
        ]
        #sorts them chronologically
        dates_worked.sort()
        #Checks if the gap between two workout days
        for i in range(1, len(dates_worked)):
            if dates_worked[i] - dates_worked[i-1] <= timedelta(days=3):
                #If gap is less than will increase the streak
                streak += 1
            else:
                #Else streak gets reset
                streak = 1
 
        return streak
 
    def weight_graph(self,progression):
        #intialise the arays
        date_list = []
        weight_list = []
        #Checks the items in progression
        for item in progression:
            #Splits the dates so its just the number and the month.
            date_list.append(" ".join(item[0].split(" ")[1:3]))
            #adds the weight to the weight list
            weight_list.append(item[1])
            #Uses both those list to display a graphical diagram to display how weight is progressing over time
            plt.plot(date_list, weight_list, marker="o")
            plt.show(block=False)
            
    def attendance_graph(self):
        #Workout frequency returns sesssions done in a week and a month
        week,month = self.workout_frequency()
        #Get the lables for the bar chart
        labels = ["This Week","This month"]
        #Values are the sessions done this week and month
        values = [week,month]
 
        #Plot the graph
        plt.bar(labels,values)
        plt.ylabel("Workouts")
        plt.title("Workout Frequency")
        plt.show()
            
    
    def open_workout(self, day):
        #Set current workout to the day of the button being clicked. EG push day has been clicked so set current workout to push day.
        self.current_workout = day
        self.update_screen("workout")
 
    def change_set(self, workout_name, s):
        #Gets current sets
        sets = self.datamanager.workouts[self.current_workout][workout_name]["sets"]
        #prevents sets from being less than 0 and greater than 6
        if sets < 1 and s == "decrease":
            parent = self.secoundary_window("ERROR", 300, 400)
            text1 = Objects.label(parent=self.popup, x=None, y=None, w=None, h=None, size=14, text_color=TEXT_COLOR, text="ERROR: sets at 0")
            text1.place(relx=0.5, rely=0.5, anchor="center")
            return
        if sets >= 6 and s == "increase":
            parent = self.secoundary_window("ERROR", 300, 400)
            text1 = Objects.label(parent=self.popup, x=None, y=None, w=None, h=None, size=14, text_color=TEXT_COLOR, text="ERROR: sets at max")
            text1.place(relx=0.5, rely=0.5, anchor="center")
            return
        #If s increase, increase the sets else decrease the amount of sets
        if s == "increase":
            self.datamanager.workouts[self.current_workout][workout_name]["sets"] += 1
        else:
            self.datamanager.workouts[self.current_workout][workout_name]["sets"] -= 1
        #Update the screen to show the new amount of sets visually
        self.update_screen("workout")
 
    def change_workout(self, command, workout_name=None):
        #Functions to remove exercises (called change workout but meant to be called change_exercise)
 
        #Checks if input for command given was remove
        if command == "remove":
            #Goes into the current workout and remove the exercise from it
            self.datamanager.workouts[self.current_workout].pop(workout_name, None)
            #Saves the data
            self.datamanager.save_data(self.datamanager.username, "workouts", self.datamanager.workouts)
 
        #Adding a new exercise to the workout day
        if command == "add":
            #Seperate screen to search for the workout
            parent = self.secoundary_window("SEARCH WORKOUT", 300, 400)
            #Textbox for input
            workout_search = Objects.text_box(parent=parent, x=None, y=None, w=200, h=25, p_text="type here")
            workout_search.place(relx=0.5, rely=0.2, anchor="center")
            #Scrollable frame to show all the exercises that match what the user typed
            results_frame = Objects.scrollable_frame(parent, w=200, h=100)
            results_frame.place(relx=0.5, rely=0.65, anchor="center")
            pass
 
            def add_workout(exercise):
                #if an exercise clicked will then set the default parameters for the exercise
                self.datamanager.workouts[self.current_workout][exercise] = {"sets": 0,"rest time": 2}
                #Saves the new data
                self.datamanager.save_data(self.datamanager.username, "workouts", self.datamanager.workouts)
                #updates the screen
                self.update_screen("workout")
                #Destroys the secounday screen  used to search for the exercise
                parent.destroy()
 
            def on_type(event):
                #Destroys all the previous widgets
                self.destroy_widgets(results_frame)
                #replaces any spaces with _ because thats how the data for exercise names was stored
                typed = workout_search.get().replace(" ", "_")
                #Gets all the exercises that have letters that were typed in them
                results = self.exercisedatabase.take_all_info(typed)
                #displays all the exercises that match the input given and display them as button that can be picked
                for key in results:
                    #Name of workout
                    name = key[0]
                    #Makes the button with the exercise name and if the button is clicked will then add that workout taking in that exercise name
                    button1 = Objects.button(parent=results_frame, x=None, y=None, w=200, h=35, text=name, text_size=12, corner_radius=0, bg_color=PANEL_BG, callback=lambda n=name: add_workout(n))
                    button1.pack()
            #Bind the function to when the user types
            workout_search.bind("<KeyRelease>", on_type)
            return
 
        self.update_screen("workout")
 
    def add_rest_time(self, workout_name):
        #Function for setting the rest time of the exercise
        parent = self.secoundary_window("ADD REST TIME", 300, 400)
        #Display current rest time for exercise
        text1 = Objects.label(parent=parent, x=None, y=None, w=None, h=None, size=12, text_color=TEXT_COLOR, text=f"CURRENT REST TIME:{self.datamanager.workouts[self.current_workout][workout_name]['rest time']} MINS")
        text1.place(relx=0.1, rely=0.1)
        #Makes a scrollable frame
        time_choice_frame = Objects.scrollable_frame(parent, w=200, h=100)
        time_choice_frame.place(relx=0.5, rely=0.65, anchor="center")
 
        def set_time(t):
            #Sets rest time to t which is time of the butotn clicked
            self.datamanager.workouts[self.current_workout][workout_name]["rest time"] = t
            #save the data
            self.datamanager.save_data(self.datamanager.username, "workouts", self.datamanager.workouts)
            #configure label to display new rest time
            text1.configure(text=f"CURRENT REST TIME:{self.datamanager.workouts[self.current_workout][workout_name]['rest time']} MINS")
        #Creates minuties all the way up to 10
            #which ever button clicked is what the new rest time is set to
        for i in range(1, 11):
            button1 = Objects.button(parent=time_choice_frame, x=None, y=None, w=200, h=35, text=f"{i} Minuites", text_size=12, corner_radius=0, bg_color=PANEL_BG, callback=lambda i=i: set_time(i))
            button1.pack()
 
    def start_workout(self):
        #Set workout_start to true. Will change the build_workout screen
        self.WORKOUT_START = True
        self.update_screen("workout")
        #Start stopwatch which calculates the time the session lasted for
        self.start_stopwatch()
 
    def update_stopwatch(self):
        #Elapsed time is = to the current time - the start time
        elapsed_time = int(time.time() - self.start_time)
        #coverts the elapsed time into min and sec  #60 sec
        mins, secs = divmod(elapsed_time, 60)
        #Updates the stopwatch label  {:02 is used so number can always be displayed as two digiits}
        self.stopwatch_label.configure(text=f"{mins:02}:{secs:02}")
        #Uses an after statement to recal the function every 1000ms = 1 sec
        self.timer_i = self.stopwatch_label.after(1000, self.update_stopwatch)
        self.current_time = f"{mins:02}:{secs:02}"
 
    def start_stopwatch(self):
        #Gets current time
        self.start_time = time.time()
        #Calls update stopwatch
        self.update_stopwatch()
 
    def update_timer(self, start_time, workout_name):
        #same concept as stopwatch
        elapsed_time = int(time.time() - start_time)
        #gets the rest time for that exercise
        timer_duration = self.datamanager.workouts[self.current_workout][workout_name]["rest time"] * 60
        if elapsed_time >= timer_duration:
            #If the time passed if greater than the duration stop the stopwatch
            self.timer_label.configure(text="00:00")
            #cancel after loop
            self.timer_label.after_cancel(self.timer_j)
            #Create a reminder saying rest time is over
            parent = self.secoundary_window("REST TIME", 300, 100)
            message = Objects.label(parent=parent, x=None, y=None, w=None, h=None, size=12, text_color=TEXT_COLOR, text="REST TIME IS OVER\nMake sure to drink water!")
            message.pack()
            return
        mins, secs = divmod(timer_duration - elapsed_time, 60)
        self.timer_label.configure(text=f"{mins:02}:{secs:02}")
        self.timer_j = self.timer_label.after(
            1000,
            lambda: self.update_timer(start_time, workout_name)
        )
 
    def start_timer(self, parent, workout_name):
        try:
            #Destroy any previous timers
            self.timer_label.after_cancel(self.timer_j)
            self.timer_label.destroy()
        except:
            pass
        #Same concept as stopwatch
        start_time = time.time()
        self.timer_label = Objects.label(parent=parent, x=None, y=None, w=None, h=None, size=12, text_color=TEXT_COLOR, text=f"{self.datamanager.workouts[self.current_workout][workout_name]['rest time']}:00")
        self.timer_label.pack(side="left", padx=6)
        self.update_timer(start_time, workout_name)
 
    def compare_values(self, workout_name, weights, reps_list):
        #Workout data stores data for PRs of specific exercises
        workout_data = self.datamanager.workout_data
 
        #Intialise wether a PR was hit
        weight_pr = False
        reps_pr   = False
        volume_pr = False
        #Defensive list to make sure data is lists
        if not isinstance(weights,   list): weights   = [weights]
        if not isinstance(reps_list, list): reps_list = [reps_list]
        try:
            saved = workout_data[workout_name]
        except KeyError:
            #Creates the exercise and the PRs if it wasnt already inside of workout data
            workout_data[workout_name] = {"weight": [0, ""], "reps": [0, ""], "volume": [0, ""]}
            saved = workout_data[workout_name]
        #These vars are the original PRs
        weight_r = saved["weight"][0]
        reps_r   = saved["reps"][0]
        volume_r = saved["volume"][0]
        for weight, reps in zip(weights, reps_list):
            try:
                #gets the weight and the reps
                weight = int(weight)
                reps   = int(reps)
            except:
                continue
            #finds volume
            volume = weight * reps
            
            #compares data and if greater than the other will then replace the current PRs and be the new PRs
            if weight > weight_r: weight_r = weight; weight_pr = True
            if reps   > reps_r:   reps_r   = reps;   reps_pr   = True
            if volume > volume_r: volume_r = volume;  volume_pr = True
 
        #gets key from dictionary without crashing it
        old = workout_data.get(workout_name, {"weight": [0,""], "reps": [0,""], "volume": [0,""]})
        old_weight_date = old["weight"][1] if isinstance(old.get("weight"), list) else ""
        old_reps_date   = old["reps"][1]   if isinstance(old.get("reps"),   list) else ""
        old_volume_date = old["volume"][1] if isinstance(old.get("volume"), list) else ""
 
        workout_data[workout_name] = {
            "weight": [weight_r, old_weight_date],
            "reps":   [reps_r,   old_reps_date],
            "volume": [volume_r, old_volume_date]
        }
        #Get current time which is when the new PR occured and then add the date next to the weight
        now = datetime.today()
        nice = now.strftime("%A %d %B %Y, %H:%M")
        if weight_pr: workout_data[workout_name]["weight"][1] = nice
        if reps_pr:   workout_data[workout_name]["reps"][1]   = nice
        if volume_pr: workout_data[workout_name]["volume"][1] = nice
 
        #Save the data
        self.datamanager.save_data(self.datamanager.username, "workout_data", workout_data)
 
        return [weight_pr, reps_pr, volume_pr]
 
    def save_workout_results(self, stats):
        #List all the days in the dictionary
        keys = list(self.datamanager.workouts[self.current_workout].keys())
 
        #Gets all the workout days in the exercise
        for workout_name in keys:
            weights   = stats[workout_name]["weight"]
            reps_list = stats[workout_name]["reps"]
            #final compare
            self.compare_values(workout_name, weights, reps_list)
        workout_history = self.datamanager.workout_history
        #gets current time to store when session happened
        now = datetime.today()
        nice = now.strftime("%A %d %B %Y, %H:%M")
        #Now store the stats into workout history
        workout_history[nice] = stats
        #save the data
        self.datamanager.save_data(self.datamanager.username, "workout_history", workout_history)
 
    def end_workout(self, stats):
        #Stop the stopwatch
        try:
            self.stopwatch_label.after_cancel(self.timer_i)
        except:
            pass
        #stop the timer
        try:
            self.timer_label.after_cancel(self.timer_j)
            self.timer_label.destroy()
        except:
            pass
        #Add the workout duration to stats
        stats["duration"] = self.current_time
        #call func to save data to workout history and update the workout data
        self.save_workout_results(stats)
        #return to mainmenu
        self.update_screen("mainmenu")
        self.WORKOUT_START = False
 
        
        parent = self.secoundary_window("WORKOUT RESULTS", 400, 700)
        #button to export the workout results
        button1 = Objects.button(parent=parent, x=None, y=None, w=200, h=35, text="Export workout", text_size=12, corner_radius=0, bg_color=PANEL_BG,callback = lambda:self.export_pdf(self.current_workout,stats))
        button1.pack(side="bottom")
        #scrollable frame to store all the workout results
        scrollable_frame = Objects.scrollable_frame(parent, w=400, h=700)
        scrollable_frame.pack()
 
        text1 = Objects.label(parent=scrollable_frame, x=None, y=None, w=None, h=None, size=16, text_color=TEXT_COLOR, text="WORKOUT RESULTS")
        text1.pack(pady=5)
 
        text1 = Objects.label(parent=scrollable_frame, x=None, y=None, w=None, h=None, size=16, text_color=TEXT_COLOR, text=f"DURATION: {stats['duration']}")
        text1.pack(pady=15)
 
        keys = list(self.datamanager.workouts[self.current_workout].keys())
        #loop through all the works displaying all the sets weights reps
        for workout_name in keys:
            sets = self.datamanager.workouts[self.current_workout][workout_name]["sets"]
 
            text2 = Objects.label(parent=scrollable_frame, x=None, y=None, w=None, h=None, size=16, text_color=TEXT_COLOR, text=workout_name)
            text2.pack(pady=10)
            #if the weight is 0 then its written as __
            for i in range(sets):
                w = stats[workout_name]["weight"][i] if i < len(stats[workout_name]["weight"]) else "—"
                r = stats[workout_name]["reps"][i]   if i < len(stats[workout_name]["reps"])   else "—"
 
                text3 = Objects.label(parent=scrollable_frame, x=None, y=None, w=None, h=None, size=12, text_color=TEXT_COLOR, text=f"Set {i+1}  weight:{w}  reps:{r}")
                text3.pack(pady=1)
    
    def add_day(self):
        #method to add a workout day (pushday, pullday, back and biceps day)
        parent = self.secoundary_window("ADD DAY", 400, 200)
        #title
        text1 = Objects.label(parent=parent, x=None, y=None, w=None, h=None, size=16, text_color=TEXT_COLOR, text="CREATE WORKOUT NAME")
        text1.pack(pady=5)
        #Input the name of the workout
        workout_name_input = Objects.text_box(parent=parent, x=None, y=None, w=200, h=25, p_text="type workout name")
        workout_name_input.pack(pady=5)
 
        def handle_adding(s):
            #Gets the workout name from the input given
            workout_name = workout_name_input.get()
 
            #Checks in current workouts if a workout day with the same name exists. If so display error
            for day in self.datamanager.workouts:
                if day == workout_name:
                    parent = self.secoundary_window("ERROR", 250, 50)
                    error = Objects.label(parent=parent, x=None, y=None, w=None, h=None, size=16, text_color=TEXT_COLOR, text="Duplicate workout name")
                    error.pack(pady=5)
                    return
                else:
                    parent = self.secoundary_window("!", 250, 50)
                    error = Objects.label(parent=parent, x=None, y=None, w=None, h=None, size=16, text_color=TEXT_COLOR, text="workout created")
                    error.pack(pady=5)
            #adds the new workout to the workouts dictionary
            self.datamanager.workouts[workout_name] = {}
            #save data
            self.datamanager.save_data(self.datamanager.username, "workouts", self.datamanager.workouts)
            self.update_screen("mainmenu")
            #destroy secoundary screen
            s.destroy()
        #Button to confirm input given if pressed will call handle_adding
        button1 = Objects.button(parent=parent, x=None, y=None, w=100, h=35, text="CONFIRM", text_size=12, corner_radius=0, bg_color=PANEL_BG, callback=lambda: handle_adding(parent))
        button1.pack(pady=5)
 
    def configure_day(self, day):
        #Function to configure day
        parent = self.secoundary_window("CONFIGURE DAY", 400, 400)
        text1 = Objects.label(parent=parent, x=None, y=None, w=None, h=None, size=16, text_color=TEXT_COLOR, text=f"CONFIGURING {day}")
        text1.pack(pady=5)
 
        def edit_name(parent, new):
            #function to edit name
            #pops the day and replaces with new meaning it just changes the name
            self.datamanager.workouts[new] = self.datamanager.workouts.pop(day)
            #save the new data
            self.datamanager.save_data(self.datamanager.username, "workouts", self.datamanager.workouts)
            self.update_screen("mainmenu")
            parent.destroy()
 
        def pull_input():
            #Get the input for the new name of the day being edited
            parent = self.secoundary_window("EDIT NAME", 250, 200)
            text1 = Objects.label(parent=parent, x=None, y=None, w=None, h=None, size=16, text_color=TEXT_COLOR, text=f"edit workout name ({day})")
            text1.pack(pady=5)
            new_name = Objects.text_box(parent=parent, x=None, y=None, w=200, h=25, p_text="input new workout name")
            new_name.pack(pady=5)
 
            button3 = Objects.button(parent=parent, x=None, y=None, w=100, h=35, text="CONFIRM", text_size=12, corner_radius=0, bg_color=PANEL_BG, callback=lambda: edit_name(parent, new_name.get()))
            button3.pack(pady=5)
 
        def delete_day():
            #delete the day
            parent = self.secoundary_window("WORKOUT RESULTS", 250, 50)
            self.datamanager.workouts.pop(day)
            self.datamanager.save_data(self.datamanager.username, "workouts", self.datamanager.workouts)
            text1 = Objects.label(parent=parent, x=None, y=None, w=None, h=None, size=16, text_color=TEXT_COLOR, text="WORKOUT DELETED")
            text1.pack(pady=5)
            self.update_screen("mainmenu")
 
        #button to edit the name of the workout day
        button1 = Objects.button(parent=parent, x=None, y=None, w=100, h=35, text="EDIT NAME", text_size=12, corner_radius=0, bg_color=PANEL_BG, callback=pull_input)
        button1.pack(pady=5)
        #Button to completely delete the workout day and the contents inside it
        button2 = Objects.button(parent=parent, x=None, y=None, w=100, h=35, text="DELTE WORKOUT", text_size=12, corner_radius=0, bg_color=PANEL_BG, callback=delete_day)
        button2.pack(pady=5)
 
    def show_info(self, parent, workout_name, button):
        #function to show the info of the workout
 
        #Checks if already up
        if hasattr(self, "info_panel") and self.info_panel.winfo_exists():
            #Removes it
            self.info_panel.pack_forget()
            #Deletes it
            del self.info_panel
            return
        #The text is take from the exercise database given the explanation
        text = self.exercisedatabase.take_info("description", workout_name)
 
        #call info panel and display the text
        self.info_panel = Objects.info_panel(
            parent=parent,
            w=350,
            h=30,
            text=text,
            text_color=TEXT_COLOR
        )
 
        #calculating and updating button position
        button.update_idletasks()
        parent.update_idletasks()
 
        abs_x = button.winfo_rootx()
        abs_y = button.winfo_rooty()
 
        parent_x = parent.winfo_rootx()
        parent_y = parent.winfo_rooty()
 
        x = abs_x - parent_x
        y = abs_y - parent_y
        self.info_panel.pack(side="left", padx=5)
 
    def export_pdf(self, workout_day, stats):
        #Function to export a PDF with the data of workout
        pdf = FPDF()
        #make the PDF and write the workout day and stats
        pdf.add_page()
        pdf.set_font("Helvetica", "B", size=16)
        pdf.cell(200, 10, text=f"Workout - {workout_day}")
        pdf.ln(12)
 
        pdf.set_font("Helvetica", size=12)
        pdf.cell(200, 10, text=f"Duration: {stats['duration']}")
        pdf.ln(12)
 
        for exercise, data in stats.items():
            if exercise == "duration":
                continue
            pdf.set_font("Helvetica", "B", size=12)
            pdf.cell(200, 10, text=exercise.replace("_", " ").title())
            pdf.ln(8)
            for i, (weight, reps) in enumerate(zip(data["weight"], data["reps"])):
                pdf.set_font("Helvetica", size=11)
                pdf.cell(200, 8, text=f"  Set {i+1}: {weight}kg x {reps} reps")
                pdf.ln(6)
            pdf.ln(4)
        
        safe_name = workout_day.replace(":", "-").replace(",", "")
        pdf.output(f"{safe_name} results.pdf")
 
    def view_workout(self, exercise,command,edit):
        #function to view workout details, PRS, Small Progression advice
        
        parent = self.secoundary_window("Edit exercise", 500, 550)
        exercise_name = self.exercisedatabase.take_info("exercise", exercise)
        description = self.exercisedatabase.take_info("description", exercise)
        text1 = Objects.label(parent=parent, x=None, y=None, w=None, h=None, size=20, text_color=TEXT_COLOR, text=exercise)
        text1.pack()
        text1 = Objects.info_panel(parent, 250, 50, description, TEXT_COLOR)
        text1.pack(pady=6)
        
        def delete_exercise(exercise):
            #Delete the exercise. Can only be deleted if its an exercise added by the user
            self.exercisedatabase.delete_exercise(exercise)
            parent = self.secoundary_window("WORKOUT RESULTS", 250, 50)
            text1 = Objects.label(parent=parent, x=None, y=None, w=None, h=None, size=16, text_color=TEXT_COLOR, text="WORKOUT DELETED")
            text1.pack()
 
            
        try:
            #Get all the PRs for the exercise
            weight = self.datamanager.workout_data[exercise]["weight"]
            reps   = self.datamanager.workout_data[exercise]["reps"]
            volume = self.datamanager.workout_data[exercise]["volume"]
        except:
            return
        #display the PRS
        text1 = Objects.label(parent=parent, x=None, y=None, w=None, h=None, size=20, text_color=TEXT_COLOR, text=f"PR WEIGHT: {weight[0]}  ({weight[1]})")
        text1.pack(pady=3)
        text1 = Objects.label(parent=parent, x=None, y=None, w=None, h=None, size=20, text_color=TEXT_COLOR, text=f"PR REPS: {reps[0]}  ({reps[1]})")
        text1.pack(pady=3)
        text1 = Objects.label(parent=parent, x=None, y=None, w=None, h=None, size=20, text_color=TEXT_COLOR, text=f"PR VOLUME: {volume[0]}  ({volume[1]})")
        text1.pack(pady=3)
        #calculate the progression for weight reps and volume
        progression = self.datamanager.get_progression(exercise,"weight")
        progression_reps =self.datamanager.get_progression(exercise,"reps")
        progression_volume = []
        #Find volume
        for w, r in zip(progression, progression_reps):
            volume = w[1] * r[1]
            progression_volume.append((w[0], volume))
 
        #From the last 5 sessions  display the weight
        for date, max_w in progression[-5:]:
                text = Objects.label(parent=parent, x=None, y=None, w=None, h=None,size=11, text_color=TEXT_COLOR, text=f"{date[:10]}  →  {max_w}kg")
                text.pack(pady=1)
        #If plateau is true(weight has stayed the same for 3 sessions) then it will display this message.
        if self.check_plateau(progression):
            plateau_label = Objects.label(parent=parent, x=None, y=None, w=None, h=None,size=11, text_color=NEGATIVE_COLOR, text="Plateau detected, Weight isnt going up")
            plateau_label.pack(pady=3)
 
        #Calculates weight percentage increase from last session
        weight_percentage_increase = self.calculate_strength_increase(progression)
        text = Objects.label(parent=parent, x=None, y=None, w=None, h=None,size=11, text_color=TEXT_COLOR, text=f"weight has gone up by {weight_percentage_increase}% since last session")
        text.pack(pady=1)
        #Buttons to view progression on graphs
        button1 = Objects.button(parent=parent, x=None, y=None, w=250, h=35, text="View Weight Progresion Graph", text_size=12, corner_radius=0, bg_color=PANEL_BG, callback=lambda: self.weight_graph(progression))
        button1.pack(pady=5)
        button1 = Objects.button(parent=parent, x=None, y=None, w=250, h=35, text="View volume Progresion Graph", text_size=12, corner_radius=0, bg_color=PANEL_BG, callback=lambda: self.weight_graph(progression_volume))
        button1.pack(pady=5)
        button1 = Objects.button(parent=parent, x=None, y=None, w=250, h=35, text="View reps Progresion Graph", text_size=12, corner_radius=0, bg_color=PANEL_BG, callback=lambda: self.weight_graph(progression_reps))
        button1.pack(pady=5)
        if command == 1:
            pass
        else:
            return
    
 
        if edit != "true":
            #Only able to delete personal exercise which means edit has to be "false" to be able to delete.
            button1 = Objects.button(parent=parent, x=None, y=None, w=200, h=35, text="delete exercise", text_size=12, corner_radius=0, bg_color=PANEL_BG, callback=lambda:delete_exercise(exercise))
            button1.pack(pady=2)
 
 
    def build_mainmenu(self, parent):
        #BUILDS THE MAINMENU
        panel1 = Objects.panel(parent=parent, x=None, y=None, w=150, h=45)
        panel1.place(relx=0.001,rely=0.001)
 
        #Places streak icon(fire symbol)
        streak = Objects.graphic(parent=parent, x=None, y=None, w=40, h=40, image="Graphics/streak.png")
        streak.place(relx=0.94,rely=0.005)
        #calculate the amount of sessions without skipping 3 days.
        streak_num = self.workout_streak()
        #display streak
        text1 = Objects.label(parent=parent, x=None, y=None, w=None, h=None, size=20, text_color=TEXT_COLOR, text=f"{streak_num}")
        text1.place(relx=0.92,rely=0.01)
        #display user
        text1 = Objects.label(parent=parent, x=None, y=None, w=None, h=None, size=14, text_color=TEXT_COLOR, text=f"USER:{self.datamanager.username}")
        text1.place(relx=0.01,rely=0.01)
        #calculate the amount of sessions did in one day. If above threshhold then workout fatigue is true
        workout_fatigue = self.check_workout_fatigue()
        #Prints message telling user to rest
        if workout_fatigue:
            text1 = Objects.label(parent=parent, x=None, y=None, w=None, h=None, size=14, text_color=NEGATIVE_COLOR, text="Workout over training detected\n stop working out for the day\n3 Sessions or higher has been done")
            text1.place(relx=0.45,rely=0.01)
        rely = 0.5
        #Loop through all the days in workouts to make buttons for each workout day
        for day in self.datamanager.workouts:
            button2 = Objects.button(parent=parent, x=None, y=None, w=200, h=35, text=day, text_size=12, corner_radius=0, bg_color=PANEL_BG, callback=lambda d=day: self.open_workout(d))
            button2.place(relx=0.5, rely=rely, anchor="center")
            #Button to configure the day
            edit_button = Objects.graphical_button(parent, w=25, h=33, x=None, y=None, image="Graphics/edit.png", image_hover=None, image_clicked=None, callback=lambda d=day: self.configure_day(d))
            edit_button.place(relx=0.65, rely=rely, anchor="center")
            #indent to make gap between buttons
            rely += 0.05
        #Button to add new workout day
        button1 = Objects.button(parent=parent, x=None, y=None, w=200, h=35, text="Add Workout Day", text_size=12, corner_radius=0, bg_color=PANEL_BG, callback=self.add_day)
        button1.place(relx=0.5, rely=rely, anchor="center")
        #Button to analyse which muscles have been trained the most this month
        button5 = Objects.button(parent=parent, x=None, y=None, w=200, h=35, text="Muscle Analysis", text_size=12, corner_radius=0, bg_color=PANEL_BG, callback=lambda:self.update_screen("muscle_analysis"))
        button5.place(relx=0.025, rely=0.85)
        #Button to view workout history
        button3 = Objects.button(parent=parent, x=None, y=None, w=200, h=35, text="View Workout History", text_size=12, corner_radius=0, bg_color=PANEL_BG, callback=lambda: self.update_screen("workout_history"))
        button3.place(relx=0.025, rely=0.95)
        #Button to view all the exercises. (able to add new exercises and delete them and view PRs and other data
        button4 = Objects.button(parent=parent, x=None, y=None, w=200, h=35, text="View Exercises", text_size=12, corner_radius=0, bg_color=PANEL_BG, callback=lambda: self.update_screen("custom"))
        button4.place(relx=0.025, rely=0.9)
        button6 = Objects.button(parent=parent, x=None, y=None, w=100, h=35, text="EXIT", text_size=12, corner_radius=10, bg_color=PANEL_BG, callback=lambda: exit())
        button6.place(relx=0.88, rely=0.95)
        
    def build_entry(self, parent):
        #Build the title screen letting the user go to login 
        logo = Objects.graphic(parent=parent, x=None, y=None, w=400, h=400, image="Graphics/RepRegistry.png")
        logo.place(relx=0.5, rely=0.25, anchor=("center"))
 
        #panel
        panel1 = Objects.panel(parent=parent, x=None, y=None, w=300, h=150)
        panel1.place(relx=0.5, rely=0.66, anchor="center")
        text1 = Objects.label(parent=parent, x=None, y=None, w=None, h=None, size=16, text_color=TEXT_COLOR, text="©RepRegistry")
        text1.place(relx=0.99, rely=0.99, anchor="se")
        #put buttons inside panel
        button1 = Objects.button(parent=parent, x=None, y=None, w=200, h=35, text="LOG IN", text_size=12, corner_radius=10, bg_color=PANEL_BG, callback=lambda: self.update_screen("login"))
        button1.place(relx=0.5, rely=0.6, anchor="center")
        button2 = Objects.button(parent=parent, x=None, y=None, w=200, h=35, text="SIGN UP", text_size=12, corner_radius=10, bg_color=PANEL_BG, callback=lambda: self.update_screen("signup"))
        button2.place(relx=0.5, rely=0.66, anchor="center")
        button3 = Objects.button(parent=parent, x=None, y=None, w=200, h=35, text="EXIT", text_size=12, corner_radius=10, bg_color=PANEL_BG, callback=lambda: exit())
        button3.place(relx=0.5, rely=0.72, anchor="center")
 
    def build_signup(self, parent):
        
        text1 = Objects.label(parent=parent, x=None, y=None, w=None, h=None, size=20, text_color=TEXT_COLOR, text="SignUp")
        text1.place(relx=0.1, rely=0.05, anchor="center")
 
        text2 = Objects.label(parent=parent, x=None, y=None, w=None, h=None, size=16, text_color=TEXT_COLOR2, text="Create Username")
        text2.place(relx=0.2, rely=0.15, anchor="center")
        #input the username input
        self.signup_username_input = Objects.text_box(parent=parent, x=None, y=None, w=200, h=25, p_text="type here")
        self.signup_username_input.place(relx=0.27, rely=0.2, anchor="center")
 
        text3 = Objects.label(parent=parent, x=None, y=None, w=None, h=None, size=16, text_color=TEXT_COLOR2, text="Create Password")
        text3.place(relx=0.2, rely=0.3, anchor="center")
        #password input
        self.signup_password_input = Objects.text_box(parent=parent, x=None, y=None, w=200, h=25, p_text="type here")
        self.signup_password_input.place(relx=0.27, rely=0.35, anchor="center")
        #confirm button
        button1 = Objects.button(parent=parent, x=None, y=None, w=100, h=35, text="Confirm", text_size=12, corner_radius=10, bg_color=PANEL_BG, callback=lambda: self.handle_signup())
        button1.place(relx=0.15, rely=0.45, anchor="center")
        #button to go back to entry screen
        button2 = Objects.button(parent=parent, x=None, y=None, w=100, h=35, text="Back", text_size=12, corner_radius=10, bg_color=PANEL_BG, callback=lambda: self.update_screen("entry"))
        button2.place(relx=0.15, rely=0.95, anchor="center")
 
    def build_login(self, parent):
        #same concept as signup
        text1 = Objects.label(parent=parent, x=None, y=None, w=None, h=None, size=20, text_color=TEXT_COLOR, text="Login")
        text1.place(relx=0.1, rely=0.05, anchor="center")
 
        text2 = Objects.label(parent=parent, x=None, y=None, w=None, h=None, size=16, text_color=TEXT_COLOR2, text="Type Username")
        text2.place(relx=0.2, rely=0.15, anchor="center")
 
        self.login_username_input = Objects.text_box(parent=parent, x=None, y=None, w=200, h=25, p_text="type here")
        self.login_username_input.place(relx=0.27, rely=0.2, anchor="center")
 
        text3 = Objects.label(parent=parent, x=None, y=None, w=None, h=None, size=16, text_color=TEXT_COLOR2, text="Type Password")
        text3.place(relx=0.2, rely=0.3, anchor="center")
 
        self.login_password_input = Objects.text_box(parent=parent, x=None, y=None, w=200, h=25, p_text="type here")
        self.login_password_input.place(relx=0.27, rely=0.35, anchor="center")
 
        button1 = Objects.button(parent=parent, x=None, y=None, w=100, h=35, text="Confirm", text_size=12, corner_radius=10, bg_color=PANEL_BG, callback=lambda: self.handle_login())
        button1.place(relx=0.15, rely=0.45, anchor="center")
 
        button2 = Objects.button(parent=parent, x=None, y=None, w=100, h=35, text="Back", text_size=12, corner_radius=10, bg_color=PANEL_BG, callback=lambda: self.update_screen("entry"))
        button2.place(relx=0.15, rely=0.95, anchor="center")
        
    def build_workout_history(self, parent):
        #screen to build workout history
        text1 = Objects.label(parent=parent, x=None, y=None, w=None, h=None, size=20, text_color=TEXT_COLOR, text="Workout History")
        text1.place(relx=0.25, rely=0.025, anchor="center")
        button2 = Objects.button(parent=parent, x=None, y=None, w=100, h=25, text="back", text_size=12, corner_radius=0, bg_color=PANEL_BG, callback=lambda: self.update_screen("mainmenu"))
        button2.place(relx=0.7, rely=0.01)
        #input box to type date to find workout by date
        type_date = Objects.text_box(parent=parent, x=None, y=None, w=200, h=25, p_text="type here")
        type_date.place(relx=0.1, rely=0.075)
        results_frame = Objects.scrollable_frame(parent, w=200, h=100)
        results_frame.place(relx=0.37, rely=0.35, anchor="center")
        
        button1 = Objects.button(parent=parent, x=None, y=None, w=200, h=35, text="view workout frequency", text_size=12, corner_radius=0, bg_color=PANEL_BG,callback = lambda: self.attendance_graph())
        button1.place(relx=0.37,rely=0.9)
 
        def view_workout(workout):
            #get the stats for that workout
            stats = self.datamanager.workout_history[workout]
            parent = self.secoundary_window(f"[workout] statistics", 400, 700)
            scrollable_frame = Objects.scrollable_frame(parent, w=400, h=700)
            scrollable_frame.pack()
            #display all the workout results
            text1 = Objects.label(parent=scrollable_frame, x=None, y=None, w=None, h=None, size=16, text_color=TEXT_COLOR, text="Workout Results")
            text1.pack(pady=5)
            text1 = Objects.label(parent=scrollable_frame, x=None, y=None, w=None, h=None, size=16, text_color=TEXT_COLOR, text=f"DURATION: {stats['duration']}")
            text1.pack(pady=15)
            for workout_name in stats:
                if workout_name == "duration":
                    continue
                text2 = Objects.label(parent=scrollable_frame, x=None, y=None, w=None, h=None, size=16, text_color=TEXT_COLOR, text=workout_name)
                text2.pack(pady=10)
                for i in range(len(stats[workout_name]["weight"])):
                    w = stats[workout_name]["weight"][i]
                    r = stats[workout_name]["reps"][i]
                    text3 = Objects.label(parent=scrollable_frame, x=None, y=None, w=None, h=None, size=12, text_color=TEXT_COLOR, text=f"Set {i+1}  weight:{w}  reps:{r}")
                    text3.pack(pady=1)
            #button to export workout
            button1 = Objects.button(parent=scrollable_frame, x=None, y=None, w=200, h=35, text="Export workout", text_size=12, corner_radius=0, bg_color=PANEL_BG,callback = lambda:self.export_pdf(workout,stats))
            button1.pack(side="bottom")
 
        def on_type(event):
            #Same concept as the other but checks replaces spaces with / and then checks if any dates match that
            self.destroy_widgets(results_frame)
            typed = type_date.get().replace(" ", "/")
            for date in self.datamanager.workout_history:
                if typed.lower() in date.lower():
                    name = date
                    button1 = Objects.button(parent=results_frame, x=None, y=None, w=200, h=35, text=name, text_size=12, corner_radius=0, bg_color=PANEL_BG, callback=lambda workout=name: view_workout(name))
                    button1.pack()
        #bind each type to finding a similar date
        type_date.bind("<KeyRelease>", on_type)
 
    def create_custom_exercise(self):
        #function to create custom exercise
        parent = self.secoundary_window("New exercise",500,600)
 
        
        def check_values(parent, e, m, i, d, error):
            #Simply check all the values for the new workout are correct
            exercise_name = e.get()
            if exercise_name.strip() == "":
                error.configure(text="Exercise name cannot be empty")
                return
 
            # check if already in database
            existing = self.exercisedatabase.take_info("exercise", exercise_name)
            if existing is not None:
                error.configure(text="Exercise already exists in database")
                return
 
            muscles = m.get()
            muscles_arr = [muscle.strip() for muscle in muscles.split(",")]
 
            intensitys = i.get()
            intensitys_arr = [val.strip() for val in intensitys.split(",")]
            for val in intensitys_arr:
                try:
                    int(val)
                except ValueError:
                    error.configure(text="Intensities must be numbers from 1 to 3")
                    return
 
            if len(muscles_arr) != len(intensitys_arr):
                error.configure(text="Muscles and intensities do not match\nlengths must match and be separated by commas")
                return
 
            description = d.get()
            built_in = "false"
            #add the exercise to the exercise database but sets built in to false so you can later delete it
            self.exercisedatabase.add_exercise(exercise_name, "Graphics/NoImage.png", muscles_arr, intensitys_arr, description, built_in)
 
        #title
        text1 = Objects.label(parent=parent, x=None, y=None, w=None, h=None, size=20, text_color=TEXT_COLOR, text="Create new exercise")
        text1.place(relx=0.35, rely=0.01)
        #title2
        text1 = Objects.label(parent=parent, x=None, y=None, w=None, h=None, size=15, text_color=TEXT_COLOR, text="Exercise name")
        text1.place(relx=0.05, rely=0.03)
 
        #input for exercise name
        Exercise_name = Objects.text_box(parent=parent, x=None, y=None, w=200, h=25, p_text="type exercise name")
        Exercise_name.place(relx=0.27, rely=0.1, anchor="center")
        #title2
        text1 = Objects.label(parent=parent, x=None, y=None, w=None, h=None, size=15, text_color=TEXT_COLOR, text="Muscles Targeted")
        text1.place(relx=0.05, rely=0.13)
 
        #input for muscles targeted
        Muscles_targeted = Objects.text_box(parent=parent, x=None, y=None, w=200, h=25, p_text="type muscles worked (seperate by ,)")
        Muscles_targeted.place(relx=0.27, rely=0.2, anchor="center")
        
        text1 = Objects.label(parent=parent, x=None, y=None, w=None, h=None, size=15, text_color=TEXT_COLOR, text="Intensity Targeted")
        text1.place(relx=0.05, rely=0.23)
 
        #input for intensity trained
        Intensity_trained = Objects.text_box(parent=parent, x=None, y=None, w=200, h=25, p_text="type intensity targeted (seperate by ,)")
        Intensity_trained.place(relx=0.27, rely=0.3, anchor="center")
                
        text1 = Objects.label(parent=parent, x=None, y=None, w=None, h=None, size=15, text_color=TEXT_COLOR, text="type description")
        text1.place(relx=0.05, rely=0.33)
 
        #input for description
        Description = Objects.text_box(parent=parent, x=None, y=None, w=200, h=25, p_text="type description")
        Description.place(relx=0.27, rely=0.4, anchor="center")
 
        error = Objects.label(parent=parent, x=None, y=None, w=None, h=None, size=16, text_color=TEXT_COLOR, text="")
        error.place(relx=0.05, rely=0.5)
        button1 = Objects.button(parent=parent, x=None, y=None, w=100, h=25, text="Confirm", text_size=12, corner_radius=0, bg_color=PANEL_BG, callback=lambda e=Exercise_name,m=Muscles_targeted,i=Intensity_trained,d=Description,error=error: check_values(parent,e,m,i,d,error))
        button1.place(relx=0.05, rely=0.45)
 
 
    def build_custom(self, parent):
        #View exercises and create a new exercise here
        text1 = Objects.label(parent=parent, x=None, y=None, w=None, h=None, size=20, text_color=TEXT_COLOR, text="Exercises")
        text1.place(relx=0.35, rely=0.01)
        button1 = Objects.button(parent=parent, x=None, y=None, w=100, h=25, text="add exercise", text_size=12, corner_radius=0, bg_color=PANEL_BG, callback=self.create_custom_exercise)
        button1.place(relx=0.65, rely=0.01)
        button2 = Objects.button(parent=parent, x=None, y=None, w=100, h=25, text="back", text_size=12, corner_radius=0, bg_color=PANEL_BG, callback=lambda: self.update_screen("mainmenu"))
        button2.place(relx=0.05, rely=0.01)
 
        workout_search = Objects.text_box(parent=parent, x=None, y=None, w=200, h=25, p_text="search workout")
        workout_search.place(relx=0.4, rely=0.1, anchor="center")
        results_frame = Objects.scrollable_frame(parent, w=350, h=400)
        results_frame.place(relx=0, rely=0.15)
 
        def on_type(event):
            self.destroy_widgets(results_frame)
            typed = workout_search.get().replace(" ", "_")
            results = self.exercisedatabase.take_all_info(typed)
            for key in results:
                name = key[0]
                edit = key[5]
                button1 = Objects.button(parent=results_frame, x=None, y=None, w=350, h=35, text=name, text_size=12, corner_radius=0, bg_color=PANEL_BG, callback=lambda e=name,s=edit: self.view_workout(e,1,s))
                button1.pack()
 
        workout_search.bind("<KeyRelease>", on_type)
        return
 
    def build_muscle_analysis(self,parent):
        #All the muscles and there muscle groups
        muscle_groups = {
            "Chest": ["pecs", "upper pecs", "lower pecs", "serratus anterior"],
            "Shoulders": ["front deltoids", "lateral deltoids", "rear deltoids", "supraspinatus", "rotator cuff"],
            "Triceps": ["triceps", "triceps long head", "tricep lateral", "tricep medial", "anconeus"],
            "Biceps": ["biceps", "biceps long head", "brachialis", "brachioradialis"],
            "Back": ["lats", "rhomboids", "traps", "upper trapezius", "lower trapezius", "middle trapezius", "erector spinae", "teres major", "levator scapulae"],
            "Quads": ["quads", "rectus femoris", "vastus lateralis", "vastus medialis", "vastus intermedius"],
            "Hamstrings": ["hamstrings"],
            "Glutes": ["glutes", "adductors"],
            "Calves": ["calves", "gastrocnemius", "soleus"],
            "Core": ["core", "obliques", "rectus abdominis", "lower rectus abdominis", "hip flexors"],
            "Forearms": ["forearms", "forearm flexors", "forearm extensors"]
        }
        #gathers the data from the function
        muscles_worked, intensity_worked = self.calculate_muscles_worked()
        
        muscle_intensity = {}
        #loops through all the data
        for muscle_list, intensity_list in zip(muscles_worked, intensity_worked):
            for muscle, intensity in zip(muscle_list, intensity_list):
                muscle = muscle.lower()
                if muscle not in muscle_intensity:
                    muscle_intensity[muscle] = 0
                muscle_intensity[muscle] = max(muscle_intensity[muscle], int(intensity))
 
        text1 = Objects.label(parent=parent, x=None, y=None, w=None, h=None, size=20, text_color=TEXT_COLOR, text="Muscle Analysis")
        text1.pack(pady=10)
        #Calculate all the data to display to the user
        for group, muscles in muscle_groups.items():
            total_intensity = sum(muscle_intensity.get(m, 0) for m in muscles)
            max_possible = len(muscles) * 3
            #calculate the percentage trained
            percentage = (total_intensity / max_possible) * 100
 
            #display messages based on how much its been trained
            if percentage == 0:
                status = "NOT TRAINED"
                color = NEGATIVE_COLOR
            elif percentage < 30:
                status = "UNDERTRAINED"
                color = NEGATIVE_COLOR
            elif percentage < 60:
                status = "MODERATE"
                color = TEXT_COLOR4
            else:
                status = "WELL TRAINED"
                color = POSITIVE_COLOR
            #Display all the information
            row = Objects.label(parent=parent, x=None, y=None, w=None, h=None, size=13, text_color=color, text=f"{group}: {status} ({int(percentage)}%)")
            row.pack(pady=3)
        #Button to return to mainmenu
        button2 = Objects.button(parent=parent, x=None, y=None, w=100, h=35, text="Back", text_size=12, corner_radius=0, bg_color=PANEL_BG, callback=lambda: self.update_screen("mainmenu"))
        button2.pack(pady=10)
 
    def build_workout(self, m_parent):
        #Initilise data
        button_clicked = False
        stats = {}
 
        panel1 = Objects.panel(parent=m_parent, x=None, y=None, w=500, h=50)
        panel1.pack(side="top", pady=0, padx=0)
 
        panel2 = Objects.panel(parent=m_parent, x=None, y=None, w=500, h=50)
        panel2.pack(side="bottom", pady=0, padx=0)
 
        text1 = Objects.label(parent=panel1, x=None, y=None, w=None, h=None, size=20, text_color=TEXT_COLOR, text=self.current_workout)
        text1.pack(pady=10, padx=20, side="left")
 
        if not self.WORKOUT_START:
            #'can only go back if workout hasnt been started
            button2 = Objects.button(parent=panel1, x=None, y=None, w=100, h=35, text="Back", text_size=12, corner_radius=0, bg_color=PANEL_BG, callback=lambda: self.update_screen("mainmenu"))
            button2.pack(side="right", pady=10, padx=20)
        #list all the exercises
        keys = list(self.datamanager.workouts[self.current_workout].keys())
 
        if self.WORKOUT_START:
            #if workout start is true than will display the stopwatch label. SELF. because stopwatch edits it like that
            self.stopwatch_label = Objects.label(parent=panel1, x=None, y=None, w=None, h=None, size=20, text_color=TEXT_COLOR, text="00:00")
            self.stopwatch_label.pack(pady=10, padx=20, side="right")
        #Frame to store all the sets
        workout_frame = Objects.scrollable_frame(m_parent, w=500, h=680)
        workout_frame.pack()
        parent = workout_frame
        #If keys are empty it means there are no exercises
        if not keys:
            text1 = Objects.label(parent=parent, x=None, y=None, w=None, h=None, size=20, text_color=TEXT_COLOR, text="NO WORKOUTS ADDED")
            text1.pack(pady=10)
        
        for workout_name in keys:
            #display  a row
            row = Objects.panel(parent=parent, x=None, y=None, w=450, h=200)
            row.pack(fill="x", pady=5)
            #display the exercise image
            image = Objects.graphic(parent=row, x=None, y=None, w=70, h=70, image=self.exercisedatabase.take_info("image", workout_name))
            image.pack(side="left", padx=10)
 
            #exercise title
            Exercise1_title = Objects.label(parent=row, x=None, y=None, w=None, h=None, size=12, text_color=TEXT_COLOR, text=self.exercisedatabase.take_info("exercise", workout_name))
            Exercise1_title.pack(side="left", padx=5)
            #button to view PRS
            view_prs = Objects.button(parent=row, x=None, y=None, w=30, h=20, text="PRS", text_size=8, corner_radius=0, bg_color=PANEL_BG, callback=lambda e=workout_name: self.view_workout(e,0,""))
            view_prs.pack(side="left", padx=1, pady=2)
            #info button
            info = Objects.button(
                parent=row,
                x=None, y=None,
                w=30, h=20,
                text="i",
                text_size=12,
                corner_radius=0,
                bg_color=PANEL_BG
            )
 
            info.configure(
                command=lambda wn=workout_name, btn=info:
                    self.show_info(panel2, wn, btn)
            )
 
            info.pack(side="left", padx=1, pady=2)
 
            if not self.WORKOUT_START:
                #if workout hasnt been started yet then:
 
                #You can set the rest time of an exercise
                Set_rest_time = Objects.button(parent=row, x=None, y=None, w=30, h=20, text="SET", text_size=8, corner_radius=0, bg_color=PANEL_BG, callback=lambda w=workout_name: self.add_rest_time(w))
                Set_rest_time.pack(side="left", padx=1, pady=2)
                #remove an exercise
                Remove_exercise = Objects.button(parent=row, x=None, y=None, w=60, h=30, text="REMOVE", text_size=10, corner_radius=2, bg_color=PANEL_BG, callback=lambda w=workout_name: self.change_workout("remove", workout_name=w))
                Remove_exercise.pack(side="right", padx=1)
                #Add and remove sets from the exercise
                add_set = Objects.button(parent=row, x=None, y=None, w=40, h=30, text="ADD SET", text_size=10, corner_radius=2, bg_color=PANEL_BG, callback=lambda w=workout_name: self.change_set(w, "increase"))
                add_set.pack(side="right", padx=1)
 
                remove_set = Objects.button(parent=row, x=None, y=None, w=40, h=30, text="REMOVE SET", text_size=10, corner_radius=2, bg_color=PANEL_BG, callback=lambda w=workout_name: self.change_set(w, "decrease"))
                remove_set.pack(side="right", padx=1)
            #Will hold all the sets
            weight_arr, reps_arr = Objects.workout_box(parent=parent, workout=self.exercisedatabase.take_info("exercise", workout_name), w=300, h=40, sets=self.datamanager.workouts[self.current_workout][workout_name]["sets"], relx=0, rely=0, workout_start=self.WORKOUT_START, timer_location=panel2, workout_name=workout_name)
            
            stats[workout_name] = {"weight": weight_arr, "reps": reps_arr}
 
        if not self.WORKOUT_START:
            #If workout hasnt been started then you can add another exercise and start the workout
            add_exercise = Objects.button(parent=panel2, x=None, y=None, w=100, h=35, text="ADD WORKOUT", text_size=12, corner_radius=1, bg_color=PANEL_BG, callback=lambda: self.change_workout("add"))
            add_exercise.pack(pady=10, padx=4, side="left")
            start_workout = Objects.button(parent=panel2, x=None, y=None, w=100, h=35, text="START WORKOUT", text_size=12, corner_radius=1, bg_color=PANEL_BG, callback=self.start_workout)
            start_workout.pack(pady=10, padx=4, side="right")
 
        if self.WORKOUT_START:
            #When workout has been started then you can end a workout
            end_workout = Objects.button(parent=panel2, x=None, y=None, w=100, h=35, text="END WORKOUT", text_size=12, corner_radius=1, bg_color=PANEL_BG, callback=lambda: self.end_workout(stats))
            end_workout.pack(pady=10, padx=4, side="right")
 
            
APP = Running()
APP.update_screen("entry")
app.mainloop()
