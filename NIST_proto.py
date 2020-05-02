from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image
from kivy.graphics import Rectangle
from kivy.graphics import Color
from kivy.graphics import Line
from math import cos, sin, pi
from kivy.clock import Clock
from kivy.properties import NumericProperty
from time import strftime
from datetime import *
import time
import mysql.connector
from mysql.connector import Error

# connecting to the mysql database for user authentication
mydb = mysql.connector.connect(
    host = '127.0.0.1',
    user = 'root',
    password = 'Qq879060003NIST',
    database = "mydatabase")

# Window to select between researcher and test subject
class SelectWindow(Screen):
    pass

# Window for researcher to login in order to access question making tools
class LogWindow(Screen):
    username = ObjectProperty(None)
    password = ObjectProperty(None)
    
    # this button pulls the database entries and checks with the text input
    # of the login page
    def loginBtn(self):
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM researchers")
        myresult = mycursor.fetchall()
        for x in myresult:
            if x[1] == self.username.text:
                if x[2] == self.password.text:
                    self.reset()
                    sm.current = "researcher"
                    return True
                else:
                    break
        invalidLogin()
                
    def reset(self):
        self.username.text = ""
        self.password.text = ""

def invalidLogin():
    pop = Popup(title = 'Invalid Login',
                content = Label(text = 'Invalid username or password. '),
                size_hint = (None, None), size = (400, 400))
    pop.open()
    

# researcher window - current has nothing in it    
class ReWindow(Screen):
    def create_Btn(self):
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM slide")
        myresult = mycursor.fetchall()
        slide_num = mycursor.rowcount
        mycursor.execute("SELECT * FROM mult_choice")
        myresult = mycursor.fetchall()
        mult_num = mycursor.rowcount
        mycursor.execute("SELECT * FROM textinput")
        myresult = mycursor.fetchall()
        text_num = mycursor.rowcount
        
        if slide_num + mult_num + text_num == 0:
            no_question_warn()
        else:
            pass
    def show_question_Btn(self):
        show_question_num()
        

class MultWindow(Screen):
    question = ObjectProperty(None)
    option1 = ObjectProperty(None)
    option2 = ObjectProperty(None)
    option3 = ObjectProperty(None)
    option4 = ObjectProperty(None)
    

    def submit_Btn(self):
        q = self.question.text
        op1 = self.option1.text
        op2 = self.option2.text
        op3 = self.option3.text
        op4 = self.option4.text
        if self.question.text == "":
            invalidInput()
        elif mult_duplicate(q):
            duplicate_warning()
        else:
            mycursor = mydb.cursor()
            sql = "INSERT INTO mult_choice (question,option1,option2,option3,option4) VALUES (%s, %s, %s, %s, %s)"
            val =(q, op1, op2, op3, op4)
            mycursor.execute(sql, val)
            mydb.commit()

def mult_duplicate(question):
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM mult_choice")
    myresult = mycursor.fetchall() 
    for x in myresult:
        if question == x[1]:
            return True
        else:
            pass
    return False

            
def duplicate_warning():
    pop = Popup(title = 'Error',
                content = Label(text = 'This question already exist'),
                size_hint = (None, None), size = (400, 400))
    pop.open()

def invalidInput():
    pop = Popup(title = 'Error',
                content = Label(text = 'One or more input is invalid'),
                size_hint = (None, None), size = (400, 400))
    pop.open()    
    
def no_question_warn():
    pop = Popup(title = 'Error',
                content = Label(text = 'There are no questions saved'),
                size_hint = (None, None), size = (400, 400))
    pop.open()

def show_question_num():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM mult_choice")
    myresult = mycursor.fetchall()     
    mult_counter = mycursor.rowcount
    mycursor.execute("SELECT * FROM slide")
    myresult = mycursor.fetchall()   
    slider_counter = mycursor.rowcount
    mycursor.execute("SELECT * FROM textinput")
    myresult = mycursor.fetchall() 
    text_counter = mycursor.rowcount
    pop = Popup(title = 'Current question types saved',
                content = Label(text = "Multiple Choice Question: " + str(mult_counter) +"\n" + "\n"
                                + "Slider Question: " + str(slider_counter) + "\n" + "\n"
                                + "Text Question: " + str(text_counter)),
                size_hint = (None, None), size = (400, 400))
    pop.open()

class SliderWindow(Screen):
    question = ObjectProperty(None)
    limit = ObjectProperty(None)

    def submit_Btn(self):
        q = self.question.text
        lim = self.limit.text
        if q == "" or lim == "":
            invalidInput()
        elif check_num(lim):
            invalidInput()
        elif mult_duplicate(q):
            duplicate_warning()
        else:
            print(int(lim))
            mycursor = mydb.cursor()
            sql = "INSERT INTO slide (question,slide_limit) VALUES (%s, %s)"
            val =(q, int(lim))
            mycursor.execute(sql, val)
            mydb.commit()            

def check_num(st):
    for x in st:
        if ord(x) < 48 or ord(x) > 57:
            return True
        else:
            pass
    return False

class InputWindow(Screen):
    pass


# the main user window where the user can proceed to answer question and read
# instructions
class MainWindow(Screen):
    
    #popup button for the instruction page
    def btn(self):
        POP.open_popup()
    
    def change(self):
        self.background_color = (1.0, 0.0, 0.0, 1.0)
    
    # canvas for the background picture
    def __init__ (self, **kwargs):
        super (MainWindow, self).__init__(**kwargs)
        with self.canvas:
            pass

        with self.canvas.before:
            pass
        with self.canvas.after:
            pass

#second question window
class SecondWindow(Screen):
    pass
# raido buttons
# slider answer

#third question window
class ThirdWindow(Screen):
    pass 

# this manages the window to allow for screen transitions
class WindowManager (ScreenManager):
    pass


#this displays the clock seen in each window
class ClockLabel(Label):
    def __init__(self, **kwargs):
        super(ClockLabel, self).__init__(**kwargs)
        Clock.schedule_interval(self.update, 1)

    def update(self, *args):
        self.text = time.strftime('%H:%M:%S')

#this class contains the function that opens up the instruction popup
class POP(FloatLayout):
    def open_popup():
        show = POP()
        popupWindow = Popup(title = "Instruction", content = show, size_hint = (None, None), size = (400, 400)) 
        popupWindow.open()


    
sm = WindowManager()

# this loads the cutomization kv file
kv = Builder.load_file("nist_proto.kv") 

# this allows screen to be called by one another via their names
screens = [SelectWindow(name = 'home'), LogWindow(name = 'login'), 
           ReWindow(name = 'researcher'), MainWindow(name ='main'),
           SecondWindow(name = 'second'), ThirdWindow(name ='third'),
           MultWindow(name = 're_mult'), SliderWindow(name = 're_slider'),
           InputWindow(name = 're_input')]

for screen in screens:
    sm.add_widget(screen)

# the starting screen when starting the program
sm.current = 'home'

class NISTApp (App):
    def build(self):
        return sm
    
if __name__ == "__main__":
    NISTApp(). run()