import customtkinter as ctk
from PIL import Image
from database import DataManager
from database import ExerciseDatabase
import os
import json
import time

#setting the settings for customtkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

#name and geometry of the app
APP_SIZE = "800x800"
APP_WIDTH, APP_HEIGHT = 800, 800



app = ctk.CTk()
app.title("APP>SYS")
app.geometry(APP_SIZE)



#REST TIMES BETWEEN SETS







#global variables

#In your write-up mention "Used Claude AI to learn CustomTkinter syntax and JSON file handling"


#colors that will be used
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
    @staticmethod
    def label(parent, text, x, y, w, h, size, text_color=TEXT_COLOR, bold=True, panel_color=APP_BG):
        font_styles = "bold" if bold else "normal"
        font = ("Arial", size, font_styles)

        label = ctk.CTkLabel(
            parent,
            text=text,
            font=font,
            text_color=text_color,
            bg_color=panel_color
        )
        if w is not None:
            label.configure(width=w)
        if h is not None:
            label.configure(height=h)
            
        # Position using place if x,y provided
        if x is not None and y is not None:
            label.place(x=x, y=y)
        
        return label

    @staticmethod
    def panel(parent, x, y, w, h, bg_color=PANEL_BG):
        panel = ctk.CTkFrame(
            parent,
            width=w,
            height=h,
            fg_color=bg_color,
            corner_radius=10,
            border_width=2.5
        )
        if x is not None and y is not None:
            panel.place(x=x, y=y)
        
        return panel

    @staticmethod
    def button(parent, x, y, w, h, text, text_size, corner_radius, bg_color, text_color="#FFFFFF", bg_normal=BUTTON_BG_NORMAL, bg_hover=BUTTON_BG_HOVER, bg_clicked=BUTTON_BG_CLICKED, bold=True, callback=None):
        font_style = "bold" if bold else "normal"
        font = ("arial", text_size, font_style)

        button = ctk.CTkButton(parent, text=text, width=w, height=h, fg_color=bg_normal, hover_color=bg_hover, bg_color=bg_color, text_color=text_color, font=font, corner_radius=corner_radius, command=callback)

        def on_press(event):
            button.configure(fg_color=bg_clicked)
        def on_release(event):
            button.configure(fg_color=bg_normal)

        button.bind("<ButtonPress-1>", on_press)
        button.bind("<ButtonRelease-1>", on_release)

        if x is not None and y is not None:
            button.place(x=x, y=y)
        return button
    @staticmethod
    def graphical_button(parent,w,h,x,y,image,image_hover,image_clicked,callback=None):

        image = ctk.CTkImage(Image.open(image), size=(w,h))
        image_hover = ctk.CTkImage(Image.open(image_hover), size=(w,h)) if image_hover else image
        image_clicked = ctk.CTkImage(Image.open(image_clicked), size=(w,h)) if image_clicked else image

        
        if image_hover and image_clicked == None:
            button = ctk.CTkButton(parent,image=image,text="",width=w,height=h,fg_color="white",hover_color="black",command=callback)
        else:
            button = ctk.CTkButton(parent,image=image,text="",width=w,height=h,fg_color=PANEL_BG,hover_color=PANEL_BG,command=callback)

        def on_press(event):
            button.configure(image=image_clicked)
            
        def revert(event):
            button.configure(image=image)

        def on_hover(event):
            button.configure(image=image_hover)

        button.bind("<Enter>",on_hover)
        button.bind("<Leave>",revert)

        button.bind("<ButtonPress-1>",on_press)
        button.bind("<ButtonRelease-1>",revert)

        
        if x is not None and y is not None:
            button.place(x=x,y=y)

        return button

    @staticmethod
    def graphic(parent, x, y, w, h,image):
        graphic = ctk.CTkImage(dark_image=Image.open(image), size=(w, h))

        graphic_label = ctk.CTkLabel(parent, image=graphic, text="")
        if x is not None and y is not None:
            graphic_label.place(x=x, y=y)
        return graphic_label

    @staticmethod
    def text_box(parent,x,y,w,h,p_text):

        text_box = ctk.CTkEntry(parent,placeholder_text=p_text,width=w,height=h)



        
        if x is not None and y is not None:
            text_box.place(x=x,y=y)

        return text_box

    @staticmethod
    def workout_box(parent, workout, w, h, sets, relx, rely,workout_start):
        weight_arr = []
        reps_arr = []
        for i in range(sets):
            bg = ctk.CTkFrame(parent, width=w, height=h, fg_color=PANEL_BG, corner_radius=5)
            bg.clicked = False
            bg.pack(fill="x", pady=3, padx=5)

            frame_count_circle = ctk.CTkFrame(bg, width=30, height=30, fg_color=APP_BG, corner_radius=5)
            frame_count_circle.pack(side="left", padx=5, pady=5)
            frame_count_text = Objects.label(parent=frame_count_circle, text=i+1, x=None, y=None, w=30, h=30, size=12)
            frame_count_text.place(relx=0.5, rely=0.5, anchor="center")

            weight_input_box = Objects.text_box(bg, x=None, y=None, w=80, h=30, p_text="weight")
            weight_input_box.pack(side="left", padx=5, pady=5)
            #weight_arr.append(weight_input_box)

            rep_input_box = Objects.text_box(bg, x=None, y=None, w=80, h=30, p_text="reps")
            rep_input_box.pack(side="left", padx=5, pady=5)
            #reps_arr.append(rep_input_box)

            def workout_completed(object1,weight_input,reps_input,turn):
                if object1.clicked:
                    return
                object1.clicked = True
                    
                object1.configure(fg_color = "#90EE90")
                
                weight = weight_input.get()
                if weight == "":
                    weight = 0
                weight_arr.append(weight)
    
                reps = reps_input.get()
                if reps == "":
                    reps = 0
                reps_arr.append(reps)

                
    

            if workout_start:
                tick_button  = Objects.graphical_button(bg,w=40,h=40,x=None,y=None,image="Graphics/tick.png",image_hover="Graphics/tick_hover.png",image_clicked="Graphics/tick_pressed.png",callback=lambda bg_ = bg,w=weight_input_box,r=rep_input_box,turn=i: workout_completed(bg_,w,r,turn) )
                tick_button.pack(side="right",padx=5,pady=5)

        return weight_arr,reps_arr

        
    @staticmethod
    def scrollable_frame(parent,w,h):
        scrollable_frame = ctk.CTkScrollableFrame(parent,width=w,height=h)
        return scrollable_frame




        
        #have a label that displays the time
        #the time variable updates every secound after button is pressed
        
        
        
        

        
        
                                              
            

#button needs to add a new set
    #firstly make a function to increase sets
    #store insied the dictionary
    #undraw current screen
    #redraw new screen with new sets amount





class Running:
    def __init__(self):
        self.current_screen = None
        self.current_workout = None
        
        self.datamanager = DataManager()
        self.exercisedatabase = ExerciseDatabase()


        self.WORKOUT_START = False



        #all the canvases
        
        self.mainmenu_screen = ctk.CTkFrame(app, width=APP_WIDTH, height=APP_HEIGHT, fg_color=APP_BG)
        self.entry_screen = ctk.CTkFrame(app, width=500, height=700, fg_color=APP_BG)
        self.signup_screen = ctk.CTkFrame(app, width=400, height=500, fg_color=APP_BG)
        self.login_screen = ctk.CTkFrame(app,width=400,height=500,fg_color=APP_BG)
        self.workout_screen = ctk.CTkFrame(app,width=520,height=800,fg_color=APP_BG)

        #build screen on startup here
        self.build_entry(self.entry_screen)
        self.build_signup(self.signup_screen)
        self.build_login(self.login_screen)

        


        #add new screen data here
        self.screen_dictionary = {
            "mainmenu": [self.mainmenu_screen,800,800,"dashboard",app],
            "entry": [self.entry_screen,500,700,"entry",app],
            "signup": [self.signup_screen,400,500,"signup",app],
            "login": [self.login_screen,400,500,"login",app],
            "workout":[self.workout_screen,520,800,"workout",app]
        }





    #updates the screen and unplaces the old one
    def update_screen(self,screen):
        if self.current_screen:
            self.current_screen.place_forget()

        for name,screen_list in self.screen_dictionary.items():
            if name == screen:
                self.window_configure(screen_list[4],screen_list[1],screen_list[2],screen_list[3])
                screen_list[0].place(x=0,y=0)
                self.current_screen = screen_list[0]

    #configures window name and size   
    def window_configure(self,screen,w,h,name):
        screen.geometry(str(w)+"x"+str(h))
        screen.title(name)

    #a secoundary popup window
    def secoundary_window(self,title,w,h):
        try:
            self.popup.destroy()
        except:
            pass
        popup = ctk.CTkToplevel(app)
        popup.attributes('-topmost', True)
        self.window_configure(popup,w,h,title)
        popup.geometry(f"{w}x{h}+960+540")
        return popup

        
    #handle signup after inputs are given and confirm is clicked
    def handle_signup(self):

        #set the username and password to local variables
        username = self.signup_username_input.get()
        password = self.signup_password_input.get()

        #call the save method
        error = self.datamanager.new_save(username,password)

        #if error = account created can now move on
        if error == "account created":
            self.build_mainmenu(self.mainmenu_screen)
            self.update_screen("mainmenu")
            return
        #if error not equal to account created will then display the error and not move on

        self.popup = self.secoundary_window("ERROR",300,200)
        text1 = Objects.label(parent=self.popup,x=None,y=None,w=None,h=None,size=14,text_color=TEXT_COLOR,text=error)
        text1.place(relx=0.5,rely=0.5,anchor="center")
        
        
    def handle_login(self):
        #get inputs as local variables
        username = self.login_username_input.get()
        password = self.login_password_input.get()

        #call the method
        error = self.datamanager.load_data(username,password)

        #if username and password found continue to mainmenu
        if error == "logged in successfully":
            self.build_mainmenu(self.mainmenu_screen)
            self.update_screen("mainmenu")
            return
        self.popup = self.secoundary_window("ERROR",200,200)
        text1 = Objects.label(parent=self.popup,x=None,y=None,w=None,h=None,size=14,text_color=TEXT_COLOR,text=error)
        text1.place(relx=0.5,rely=0.5,anchor="center")
        

    def destroy_widgets(self,screen):
        for widget in screen.winfo_children():
            widget.destroy()

    def open_workout(self,day):
        #destroy all the widgets in the screen before placing the new workout
        self.destroy_widgets(self.workout_screen)
        #set the day
        self.current_workout =  day
        #draw the screen
        self.build_workout(self.workout_screen)
        #change the screen to the workout screen
        self.update_screen("workout")

        
    def change_set(self,workout_name,s):


        sets = self.datamanager.workouts[self.current_workout][workout_name]["sets"]
        if sets < 1 and s== "decrease":
            return
        if sets >= 6 and s== "increase":
            return


            
        if s == "increase":
            self.datamanager.workouts[self.current_workout][workout_name]["sets"]+=1
        else:
            self.datamanager.workouts[self.current_workout][workout_name]["sets"]-=1
            
        self.datamanager.save_data(self.datamanager.username,"workouts",self.datamanager.workouts)
            

        self.destroy_widgets(self.workout_screen)

        self.build_workout(self.workout_screen)
    def change_workout(self,command,workout_name=None):
        
        if command == "remove":
            self.datamanager.workouts[self.current_workout].pop(workout_name, None)
            self.datamanager.save_data(self.datamanager.username,"workouts",self.datamanager.workouts)

        if command == "add":
            parent = self.secoundary_window("SEARCH WORKOUT",300,400)
            workout_search = Objects.text_box(parent=parent,x=None,y=None,w=200,h=25,p_text="type here")
            workout_search.place(relx=0.5,rely=0.2,anchor="center")
            results_frame = Objects.scrollable_frame(parent,w=200,h=100)
            results_frame.place(relx=0.5,rely=0.65,anchor = "center")
            pass

            def add_workout(exercise):
                self.datamanager.workouts[self.current_workout][exercise] = {"sets": 0, "reps": 0, "weight": 0}
                self.datamanager.save_data(self.datamanager.username, "workouts", self.datamanager.workouts)
                print(self.datamanager.workouts)
                self.destroy_widgets(self.workout_screen)
                self.build_workout(self.workout_screen)
                parent.destroy()


            def on_type(event):
                self.destroy_widgets(results_frame)
                typed = workout_search.get().replace(" ","_")
                results = self.exercisedatabase.take_all_info(typed)
                for key in results:
                    name = key[0]
                    button1 = Objects.button(parent=results_frame, x=None, y=None, w=200, h=35, text=name, text_size=12, corner_radius=0, bg_color=PANEL_BG,callback=lambda n=name:add_workout(n))
                    button1.pack()
            workout_search.bind("<KeyRelease>", on_type)
            
            return
            



        self.destroy_widgets(self.workout_screen)
        self.build_workout(self.workout_screen)
        
    def start_workout(self):
        self.WORKOUT_START = True
        self.destroy_widgets(self.workout_screen)
        self.build_workout(self.workout_screen)
        self.start_stopwatch()

        
    def update_stopwatch(self):
        elapsed_time = int(time.time() - self.start_time)
        mins, secs = divmod(elapsed_time, 60)
        self.timer_label.configure(text = f"{mins:02}:{secs:02}")
        self.timer_i = self.timer_label.after(1000,self.update_stopwatch)
        self.workout_time = f"{mins:02}:{secs:02}"

    def start_stopwatch(self):
        self.start_time = time.time()
        self.update_stopwatch()

    def end_workout(self,stats):
        self.WORKOUT_START  = False
        self.timer_label.after_cancel(self.timer_i)
        self.update_screen("mainmenu")

        parent = self.secoundary_window("WORKOUT RESULTS",400,700)
        scrollable_frame = Objects.scrollable_frame(parent,w=400,h=700)
        scrollable_frame.pack()

        text1 = Objects.label(parent=scrollable_frame, x=None, y=None, w=None, h=None, size=16, text_color=TEXT_COLOR, text="WORKOUT RESULTS")
        text1.pack(pady=5)

        text1 = Objects.label(parent=scrollable_frame, x=None, y=None, w=None, h=None, size=16, text_color=TEXT_COLOR, text=f"DURATION:{self.workout_time}")
        text1.pack(pady=15)


        #have to edit self.datamanger.workouts to take into account the multiple sets with the multiples reps
        keys = list(self.datamanager.workouts[self.current_workout].keys())

        for workout_name in keys:
            
            sets=self.datamanager.workouts[self.current_workout][workout_name]["sets"]
            text2 = Objects.label(parent=scrollable_frame, x=None, y=None, w=None, h=None, size=16, text_color=TEXT_COLOR, text=workout_name)
            text2.pack(pady=10)
            
            for i in range(sets):
                
                w = stats[workout_name]["weight"][i] if i < len(stats[workout_name]["weight"]) else "—"
                r = stats[workout_name]["reps"][i] if i < len(stats[workout_name]["reps"]) else "—"
                
                text3 = Objects.label(parent=scrollable_frame, x=None, y=None, w=None, h=None, size=12, text_color=TEXT_COLOR, text=f"Set {i+1}  weight:{w}  reps:{r}")
                text3.pack(pady=1)

        
        


        


        
    def build_mainmenu(self, parent):      

        rely=0.5
        for day in self.datamanager.workouts:#***********************************************************************************************************************************************************************************************
            button2 = Objects.button(parent=parent, x=None, y=None, w=200, h=35, text=day, text_size=12, corner_radius=10, bg_color=PANEL_BG,callback=lambda d=day:self.open_workout(d))
            button2.place(relx=0.5, rely=rely, anchor="center")
            rely+= 0.05
            
    def build_entry(self, parent):   
        logo = Objects.graphic(parent=parent, x=None, y=None, w=400, h=400,image="Graphics/RepRegistry.png")
        logo.place(relx=0.5, rely=0.25, anchor=("center"))

        panel1 = Objects.panel(parent=parent, x=None, y=None, w=300, h=150)
        panel1.place(relx=0.5, rely=0.66, anchor="center")
        text1 = Objects.label(parent=parent, x=None, y=None, w=None, h=None, size=16, text_color=TEXT_COLOR, text="©RepRegistry")
        text1.place(relx=0.99, rely=0.99, anchor="se")
        
        #entry buttons
        button1 = Objects.button(parent=parent, x=None, y=None, w=200, h=35, text="LOG IN", text_size=12, corner_radius=10, bg_color=PANEL_BG,callback=lambda:self.update_screen("login"))
        button1.place(relx=0.5, rely=0.6, anchor="center")
        button2 = Objects.button(parent=parent, x=None, y=None, w=200, h=35, text="SIGN UP", text_size=12, corner_radius=10, bg_color=PANEL_BG,callback=lambda: self.update_screen("signup"))
        button2.place(relx=0.5, rely=0.66, anchor="center")
        button3 = Objects.button(parent=parent, x=None, y=None, w=200, h=35, text="EXIT", text_size=12, corner_radius=10, bg_color=PANEL_BG,callback=lambda:exit())
        button3.place(relx=0.5, rely=0.72, anchor="center")

    def build_signup(self, parent):
        text1 = Objects.label(parent=parent,x=None,y=None,w=None,h=None,size=20,text_color=TEXT_COLOR,text="SignUp")
        text1.place(relx=0.1,rely=0.05,anchor="center")

        text2 = Objects.label(parent=parent,x=None,y=None,w=None,h=None,size=16,text_color=TEXT_COLOR2,text="Create Username")
        text2.place(relx = 0.2,rely =0.15,anchor = "center")

        self.signup_username_input = Objects.text_box(parent=parent,x=None,y=None,w=200,h=25,p_text="type here")
        self.signup_username_input.place(relx=0.27,rely=0.2,anchor="center")

        text3 = Objects.label(parent=parent,x=None,y=None,w=None,h=None,size=16,text_color=TEXT_COLOR2,text="Create Password")
        text3.place(relx = 0.2,rely =0.3,anchor = "center")

        self.signup_password_input = Objects.text_box(parent=parent,x=None,y=None,w=200,h=25,p_text="type here")
        self.signup_password_input.place(relx=0.27,rely=0.35,anchor="center")
        


        button1 = Objects.button(parent=parent, x=None, y=None, w=100, h=35, text="Confirm", text_size=12, corner_radius=10, bg_color=PANEL_BG,callback=lambda:self.handle_signup())
        button1.place(relx=0.15, rely=0.45, anchor="center")

        button2 = Objects.button(parent=parent, x=None, y=None, w=100, h=35, text="Back", text_size=12, corner_radius=10, bg_color=PANEL_BG,callback=lambda:self.update_screen("entry"))
        button2.place(relx=0.15, rely=0.95, anchor="center")

    def build_login(self,parent):
        text1 = Objects.label(parent=parent,x=None,y=None,w=None,h=None,size=20,text_color=TEXT_COLOR,text="Login")
        text1.place(relx=0.1,rely=0.05,anchor="center")

        text2 = Objects.label(parent=parent,x=None,y=None,w=None,h=None,size=16,text_color=TEXT_COLOR2,text="Type Username")
        text2.place(relx = 0.2,rely =0.15,anchor = "center")

        self.login_username_input = Objects.text_box(parent=parent,x=None,y=None,w=200,h=25,p_text="type here")
        self.login_username_input.place(relx=0.27,rely=0.2,anchor="center")

        text3 = Objects.label(parent=parent,x=None,y=None,w=None,h=None,size=16,text_color=TEXT_COLOR2,text="Type Password")
        text3.place(relx = 0.2,rely =0.3,anchor = "center")

        self.login_password_input = Objects.text_box(parent=parent,x=None,y=None,w=200,h=25,p_text="type here")
        self.login_password_input.place(relx=0.27,rely=0.35,anchor="center")
        


        button1 = Objects.button(parent=parent, x=None, y=None, w=100, h=35, text="Confirm", text_size=12, corner_radius=10, bg_color=PANEL_BG,callback=lambda:self.handle_login())
        button1.place(relx=0.15, rely=0.45, anchor="center")

        button2 = Objects.button(parent=parent, x=None, y=None, w=100, h=35, text="Back", text_size=12, corner_radius=10, bg_color=PANEL_BG,callback=lambda:self.update_screen("entry"))
        button2.place(relx=0.15, rely=0.95, anchor="center")
        
    def build_workout(self, parent):
        workout_frame = Objects.scrollable_frame(parent, w=500, h=800)
        workout_frame.pack()
        parent = workout_frame



        stats = {}
        

        panel1 = Objects.panel(parent=parent, x=None, y=None, w=450, h=200)
        panel1.pack(fill="x")

        text1 = Objects.label(parent=panel1, x=None, y=None, w=None, h=None, size=20, text_color=TEXT_COLOR, text=self.current_workout)
        text1.pack(pady=10,padx=4,side="left")

        if not self.WORKOUT_START:

            button2 = Objects.button(parent=panel1, x=None, y=None, w=100, h=35, text="Back", text_size=12, corner_radius=0, bg_color=PANEL_BG, callback=lambda: self.update_screen("mainmenu"))
            button2.pack(side="right",pady=10,padx=4)

        keys = list(self.datamanager.workouts[self.current_workout].keys())


        self.timer_label = Objects.label(parent=panel1, x=None, y=None, w=None, h=None, size=20, text_color=TEXT_COLOR, text="00:00")

        self.timer_label.pack(pady=10,padx=10,side="right")
            

        if not keys:
            text1 = Objects.label(parent=parent, x=None, y=None, w=None, h=None, size=20, text_color=TEXT_COLOR, text="NO WORKOUTS ADDED")
            text1.pack(pady=10)

        for workout_name in keys:
            row = Objects.panel(parent=parent, x=None, y=None, w=450, h=200)
            row.pack(fill = "x",pady = 5)

            image = Objects.graphic(parent=row, x=None, y=None, w=70, h=70, image=self.exercisedatabase.take_info("image", workout_name))
            image.pack(side="left", padx=10)

            Exercise1_title = Objects.label(parent=row, x=None, y=None, w=None, h=None, size=12, text_color=TEXT_COLOR, text=self.exercisedatabase.take_info("exercise", workout_name))
            Exercise1_title.pack(side="left", padx=5)

            if not self.WORKOUT_START:

                Remove_exercise = Objects.button(parent=row, x=None, y=None, w=100, h=30, text="REMOVE", text_size=12, corner_radius=2, bg_color=PANEL_BG, callback=lambda w=workout_name: self.change_workout("remove", workout_name=w))
                Remove_exercise.pack(side="right", padx=5)

                add_set = Objects.graphical_button(parent=row, w=35, h=35, x=None, y=None, image="Graphics/+.png", image_hover=None, image_clicked=None, callback=lambda w=workout_name: self.change_set(w, "increase"))
                add_set.pack(side="right", padx=2)

                remove_set = Objects.graphical_button(parent=row, w=35, h=35, x=None, y=None, image="Graphics/-.png", image_hover=None, image_clicked=None, callback=lambda w=workout_name: self.change_set(w, "decrease"))
                remove_set.pack(side="right", padx=2)

            weight_arr,reps_arr = Objects.workout_box(parent=parent, workout=self.exercisedatabase.take_info("exercise", workout_name), w=300, h=40, sets=self.datamanager.workouts[self.current_workout][workout_name]["sets"], relx=0, rely=0,workout_start=self.WORKOUT_START)
            stats[workout_name] = {"weight": weight_arr, "reps": reps_arr}

        if  not self.WORKOUT_START:
            panel2 = Objects.panel(parent=parent, x=None, y=None, w=450, h=200)
            panel2.pack(fill="x")



            add_exercise = Objects.button(parent=panel2, x=None, y=None, w=100, h=30, text="ADD WORKOUT", text_size=12, corner_radius=1, bg_color=PANEL_BG, callback=lambda: self.change_workout("add"))
            add_exercise.pack(pady=10,padx=4,side="left")
            start_workout = Objects.button(parent=panel2, x=None, y=None, w=100, h=30, text="START WORKOUT", text_size=12, corner_radius=1, bg_color=PANEL_BG, callback=self.start_workout)
            start_workout.pack(pady=10,padx=4,side="right")
            
        if self.WORKOUT_START:
            end_workout = Objects.button(parent=parent, x=None, y=None, w=100, h=30, text="END WORKOUT", text_size=12, corner_radius=1, bg_color=PANEL_BG, callback=lambda:self.end_workout(stats))
            end_workout.pack(pady=10,padx=4,side="bottom")








APP = Running()
APP.update_screen("entry")



app.mainloop()
