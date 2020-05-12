##### CHANGES MADE BY AJ ON MON, MAY 11 #####

#                VERY IMPORTANT                    #
### Need to use the 'nist_proto_AJ_Edit.kv' file!!!!

### Needed to change "textinput" table name to "text_input"
### Added more fields to my tables (not used in this python file)
### Fixed issue with MC question creation (input boxes are now empty
####### after question submission + goes back to select screen)
### Got the slider questions to appear in patient windows
### Got the MC answers to show up in patient windows
### Included option for researcher to input slider start and increment
### Got physical slider to work in patient window
### Got it to show the slider value

##### END OF CHANGES FROM AJ #####

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder

from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.uix.slider import Slider

from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout

from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivy.properties import NumericProperty

from kivy.uix.image import Image
from kivy.graphics import Rectangle
from kivy.graphics import Color
from kivy.graphics import Line

from math import cos, sin, pi

from kivy.clock import Clock
from time import strftime
from datetime import *
import time

import mysql.connector
from mysql.connector import Error

# connecting to the mysql database for user authentication
### You will need to change user,password,database to your own
mydb = mysql.connector.connect(
    host = 'localhost',
    user = 'ajnist',
    password = 'nist', 
    database = "NIST_v1") 
    
    
# this loads the cutomization kv file
kv = Builder.load_file("nist_proto_AJ_Edit.kv") 
    
    

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
        mycursor.execute("SELECT * FROM text_input")
        myresult = mycursor.fetchall()
        text_num = mycursor.rowcount
        
        if slide_num + mult_num + text_num == 0:
            no_question_warn()
        else:
            pass
    def show_question_Btn(self):
        show_question_num()
        
### Window for researcher
### This code creates a MC question and
### puts it into the SQL database
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
        self.question.text = ""
        self.option1.text = ""
        self.option2.text = ""
        self.option3.text = ""
        self.option4.text = ""

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
    mycursor.execute("SELECT * FROM text_input")
    myresult = mycursor.fetchall() 
    text_counter = mycursor.rowcount
    pop = Popup(title = 'Current question types saved',
                content = Label(text = "Multiple Choice Question: " + str(mult_counter) +"\n" + "\n"
                                + "Slider Question: " + str(slider_counter) + "\n" + "\n"
                                + "Text Question: " + str(text_counter)),
                size_hint = (None, None), size = (400, 400))
    pop.open()

### This code creates a slider question and puts it into SQL database
class SliderWindow(Screen):
    question = ObjectProperty(None)
    start = ObjectProperty(None)
    limit = ObjectProperty(None)
    increment = ObjectProperty(None)

    def submit_Btn(self):
        q = self.question.text
        strt = self.start.text
        lim = self.limit.text
        inc = self.increment.text
        
        if q == "" or lim == "":
            invalidInput()
        elif check_num(lim):
            invalidInput()
        elif mult_duplicate(q):
            duplicate_warning()
        else:
            mycursor = mydb.cursor()
            sql = "INSERT INTO slide (question, slide_limit, slide_start, slide_increment) VALUES (%s, %s, %s, %s)"
            val = (q, int(lim), int(strt), int(inc))
            mycursor.execute(sql, val)
            mydb.commit() 
                
        self.question.text = ""
        self.start.text = ""
        self.limit.text = ""
        self.increment.text = ""

def check_num(st):
    for x in st:
        ### To check if each entry is an integer between 0 and 9
        if ord(x) < 48 or ord(x) > 57:
            return True
        else:
            pass
    return False

class InputWindow(Screen):
    pass


# the main user (PATIENT) window where the user (PATIENT) can 
# proceed to answer question and read instructions
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
    def next_Btn(self):
        first_q = quest_str_lst[0]
        sm.current = first_q
        sm.transition.direction = "left"
        
# this manages the window to allow for screen transitions
class WindowManager (ScreenManager):
    pass


### This code creates a window on the PATIENT interface
### for each MC question that is in the database
class MultTemplate (Screen):
    mult_question = StringProperty()
    MC_1 = StringProperty()
    MC_2 = StringProperty()
    MC_3 = StringProperty()
    MC_4 = StringProperty()
    
    #### mylist = [mult_question, MC_1, MC_2, MC_3, MC_4]

    
    # this allows the kv label text to be changed via python
    def __init__(self, **kwargs):
        super(MultTemplate, self).__init__(**kwargs)
        self.question = ObjectProperty(None)
        self.answer1 = ObjectProperty(None)
        self.answer2 = ObjectProperty(None)
        self.answer3 = ObjectProperty(None)
        self.answer4 = ObjectProperty(None)

        mycursor = mydb.cursor()
        
        # MC_FIELDS = ["question", 'option1', 'option2', 'option3', 'option4']
        
        # for i in range(0,5):
            # sql = "SELECT %s FROM mult_choice WHERE mc_id = %d" % (MC_FIELDS[i], mult_num)
            # mycursor.execute(sql)
            # myresult = mycursor.fetchall()
            # self.mylist[i]= (myresult[0])[0]
        
        sql_question = "SELECT question FROM mult_choice WHERE mc_id = %d" % mult_num
        mycursor.execute(sql_question)
        myresult = mycursor.fetchall()        
        self.mult_question = (myresult[0])[0]        
        
        sql_option1 = "SELECT option1 FROM mult_choice WHERE mc_id = %d" % mult_num
        mycursor.execute(sql_option1)
        myresult = mycursor.fetchall() 
        self.MC_1 = (myresult[0])[0] # myresult produces the question as [(question)]
    
        sql_option2 = "SELECT option2 FROM mult_choice WHERE mc_id = %d" % mult_num
        mycursor.execute(sql_option2)
        myresult = mycursor.fetchall() 
        self.MC_2 = (myresult[0])[0]   
   
        sql_option3 = "SELECT option3 FROM mult_choice WHERE mc_id = %d" % mult_num
        mycursor.execute(sql_option3)
        myresult = mycursor.fetchall() 
        self.MC_3 = (myresult[0])[0]  

        sql_option4 = "SELECT option4 FROM mult_choice WHERE mc_id = %d" % mult_num
        mycursor.execute(sql_option4)
        myresult = mycursor.fetchall() 
        self.MC_4 = (myresult[0])[0]


    def next_Btn(self):
        if len (quest_str_lst) == 1:
            pass
        else:
            quest_str_lst.pop(0)
            next_q = quest_str_lst[0]
            sm.current = next_q
            sm.transition.diretion = "left"
       
       
### This code creates a window on the PATIENT interface
### for each SLIDER question that is in the database
class SlideTemplate(Screen):
    
    slider_question = StringProperty() 
    start = NumericProperty()
    limit = NumericProperty()
    increment = NumericProperty()
    
    # this allows the kv label text to be changed via python
    def __init__(self, **kwargs):
        super(SlideTemplate, self).__init__(**kwargs)
        self.question = ObjectProperty(None)
        #self.answer1 = ObjectProperty(None)

        mycursor = mydb.cursor()
                
        sql = "SELECT question FROM slide WHERE slide_id = %d" % slide_num  
        mycursor.execute(sql)
        myresult = mycursor.fetchall() 
        self.slider_question = (myresult[0])[0]
        
        sql = "SELECT slide_start FROM slide WHERE slide_id = %d" % slide_num  
        mycursor.execute(sql)
        myresult = mycursor.fetchall() 
        self.start = (myresult[0])[0]
        
        sql = "SELECT slide_increment FROM slide WHERE slide_id = %d" % slide_num  
        mycursor.execute(sql)
        myresult = mycursor.fetchall() 
        self.increment = (myresult[0])[0]
                
        sql = "SELECT slide_limit FROM slide WHERE slide_id = %d" % slide_num  
        mycursor.execute(sql)
        myresult = mycursor.fetchall() 
        self.limit = (myresult[0])[0]
  
    
    
    def next_Btn(self):
        if len (quest_str_lst) == 1:
            pass
        else:
            quest_str_lst.pop(0)
            next_q = quest_str_lst[0]
            sm.current = next_q
            sm.transition.direction = "left"


class TextTemplate(Screen):
    def next_Btn(self):
        if len (quest_str_lst) == 1:
            pass
        else:
            quest_str_lst.pop(0)
            next_q = quest_str_lst[0]
            sm.current = next_q
            sm.transition.direction = "left"    
    

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



# this allows screen to be called by one another via their names
screens = [SelectWindow(name = 'home'), LogWindow(name = 'login'), 
           ReWindow(name = 'researcher'), MainWindow(name ='main'),
           SecondWindow(name = 'second'), ThirdWindow(name ='third'),
           MultWindow(name = 're_mult'), SliderWindow(name = 're_slider'),
           InputWindow(name = 're_input')]



### Code to allow for any number of questions of any type
mycursor = mydb.cursor()

mycursor.execute("SELECT * FROM mult_choice")
myresult = mycursor.fetchall()
NUM_OF_MC = mycursor.rowcount

mycursor.execute("SELECT * FROM slide")
myresult = mycursor.fetchall()
NUM_OF_SLIDER = mycursor.rowcount

mycursor.execute("SELECT * FROM text_input")
myresult = mycursor.fetchall()
NUM_OF_TEXT = mycursor.rowcount


print("The total number of MC questions is: %d" % NUM_OF_MC)
print("The total number of Slider questions is: %d" % NUM_OF_SLIDER)
print("The total number of Text questions is: %d" % NUM_OF_TEXT)
### End of that piece of code


mult_num = 1
mult_list = []
slide_num = 1
slide_list =[]
text_num = 1
text_list = []

quest_str_lst = []

while mult_num < NUM_OF_MC+1: 
    screen = MultTemplate(name = 'mult %d' % mult_num)
    quest_str_lst.append("mult %d" % mult_num)
    mult_list.append(screen)
    mult_num += 1
#print(mult_list)

while slide_num < NUM_OF_SLIDER+1:
    screen = SlideTemplate(name = 'slide %d' % slide_num)
    quest_str_lst.append("slide %d" % slide_num)
    slide_list.append(screen)
    slide_num += 1

while text_num < NUM_OF_TEXT+1:
    screen = TextTemplate(name = 'text %d' % text_num)
    quest_str_lst.append("text %d" % text_num)
    text_list.append(screen)
    text_num += 1
    
screens.extend(mult_list)
screens.extend(slide_list)
screens.extend(text_list)


for i in screens:
    sm.add_widget(i)




###print("\n")
###print("The screens are listed below: ")
###print(screens)

###print("\n")
###print("The question list is listed below: ")
###print(quest_str_lst)

###print("\n")

# the starting screen when starting the program
sm.current = 'home'

class NISTApp (App):
    def build(self):
        return sm
    
if __name__ == "__main__":
    NISTApp(). run()
