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
           SecondWindow(name = 'second'), ThirdWindow(name ='third'),]

for screen in screens:
    sm.add_widget(screen)

# the starting screen when starting the program
sm.current = 'home'

class NISTApp (App):
    def build(self):
        return sm
    
if __name__ == "__main__":
    NISTApp(). run()