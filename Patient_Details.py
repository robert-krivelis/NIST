import kivy
import os
from kivy.lang.builder import Builder
#import xlsxwriter

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.base import runTouchApp

from kivy.properties import ObjectProperty

from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout

from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.dropdown import DropDown
from kivy.uix.spinner import Spinner

kivy.require("1.11.1")

#Builder.load_file("Patient_Details.kv")





class PatientDetails(FloatLayout):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		
		PATIENT_ATTRIBUTES = ["Name", "Subject Number", "Date of Birth", "Age", "Sex", "Height", "Weight", "Trial Start Date", "Trial End Date", "Number of Questions"]
		
		MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
		
		DAY_RANGE = list(range(1,32))
		DAYS = list(map(str, DAY_RANGE))
		
		YEAR_RANGE = list(range(1950,2031))
		YEARS = list(map(str, YEAR_RANGE))
		
		BOOM = [MONTHS, DAYS, YEARS]
		
		AGE = ["Month", "Day", "Year"]
		
		SEX = ["Male", "Female"]
		
		NUM_QUESTIONS = 0 # Initializing variable to store user input
		
		
		
		### Widgets for Patient Attributes
		# for i in range(0,10):
			# self.patientLabels = Label(text = PATIENT_ATTRIBUTES[i], size_hint = (0.2,0.05), pos_hint = {'x':0.1, 'y':0.8-0.05*i})
			
			# self.InputBox = TextInput(text = "", multiline = False, size_hint = (0.2, 0.05), pos_hint = {'x':0.3, 'y':0.8-0.05*i}, cursor_blink = True)
			
			# self.add_widget(self.patientLabels)
			# self.add_widget(self.InputBox)
			
			
			
		#### Trying to use for-loop in .kv file
		# patient = ObjectProperty(None)
		
		# for i in range(0,10):
			
			# self.patient.text = PATIENT_ATTRIBUTES[i]
			# self.patient.pos_hint = {'x':0.1, 'y':0.8-0.05*i}
		
		
		
		
		
		
		
		
		
		
		### Widget for Instructions
		self.Instructions = Label(text = "Please input all patient details below.These will be transferred to the patient's Excel file.", size_hint = (1.0,0.1), pos_hint = {'top': 1.0})
		self.add_widget(self.Instructions)
		
		### Widget for D.O.B Selections (Dropdown/Spinner)
		for i in range(0,3):
			self.ageDate = Spinner(
				text = AGE[i],
				values = BOOM[i],
				size_hint = (0.1, 0.05),
				#size = (100,44),
				pos_hint = {'center_x':0.6+i/10, 'center_y':0.725},
				sync_height = True)
			self.add_widget(self.ageDate)


		
		# ### Widget for Sex Selection (Radio Button)
		for i in range(0,2):
			self.Sex = Label(
				text = SEX[i],
				pos_hint = {'center_x':0.6+i/5, 'center_y':0.625})
			self.sexSelect = CheckBox(
				active = False,
				group = 'sex',
				pos_hint = {'center_x':0.6+(2*i+1)/10, 'center_y':0.625},
				size_hint = (0.03, 0.03))
			self.add_widget(self.Sex)	
			self.add_widget(self.sexSelect)		

		
		### Widget for Height Inputs
		self.Feet = TextInput(text = "ft", multiline = False, size_hint = (0.05, 0.05), pos_hint = {'x':0.55, 'y':0.55 }, input_filter = "float")
		self.add_widget(self.Feet)
		
		self.feetLabel = Label(text = "feet", size_hint = (0.05,0.05), pos_hint = {'x':0.6, 'y':0.55 })
		self.add_widget(self.feetLabel)
		
		self.Inch = TextInput(text = "in", multiline = False, size_hint = (0.05, 0.05), pos_hint = {'x':0.65, 'y':0.55 }, input_filter = "float")
		self.add_widget(self.Inch)
		
		self.inchLabel = Label(text = "in", size_hint = (0.03,0.05), pos_hint = {'x':0.7, 'y':0.55 })
		self.add_widget(self.inchLabel)
				
		### Widget for Height Conversion
		self.heightConv = Label(text = "(equiv: ", size_hint = (0.05,0.05), pos_hint = {'x':0.75, 'y':0.55 })
		self.add_widget(self.heightConv)
		
		self.centi = TextInput(text = "cm", multiline = False, size_hint = (0.07, 0.05), pos_hint = {'x':0.8, 'y':0.55 })
		self.add_widget(self.centi)
		
		self.centiLabel = Label(text = " cm)", size_hint = (0.03,0.05), pos_hint = {'x':0.87, 'y':0.55 })
		self.add_widget(self.centiLabel)
		
		def feet_to_cm(instance, value):
			feet = self.Feet.text
			inch = self.Inch.text
							
			if feet == "" or feet == "ft":
				cm = 0
				inch = 0

				###### 1 in = 2.54 cm
				boom = (float(feet)*12+float(inch))*2.54
				cm = round(boom, 2)				
				
			else:
				if inch == "" or inch == "in":
					cm = 0
					inch = 0
					
					###### 1 in = 2.54 cm
					boom = (float(feet)*12+float(inch))*2.54
					cm = round(boom, 2)	
				
				else:
					###### 1 in = 2.54 cm
					boom = (float(feet)*12+float(inch))*2.54
					cm = round(boom, 2)
				
			self.centi = TextInput(text = str(cm), multiline = False, size_hint = (0.07, 0.05), pos_hint = {'x':0.8, 'y':0.55 })
			self.add_widget(self.centi)
			
		
		self.Feet.bind(text = feet_to_cm)
		self.Inch.bind(text = feet_to_cm)
		
		
		def cm_to_feetinch(instance, value):
			cm = self.centi.text
							
			if cm == "":
				feet = 0
				inch = 0
				
			else:
				###### 1 cm = 0.393701 in
				boom = float(cm)*0.393701
				boom2 = round(boom, 2)					
				
				feet = int(boom2 // 12)
				inch = int(boom2 % 12)
				
			self.Feet = TextInput(text = str(feet), multiline = False, size_hint = (0.05, 0.05), pos_hint = {'x':0.55, 'y':0.55 }, input_filter = "float")
			self.add_widget(self.Feet)
		
			self.Inch = TextInput(text = str(inch), multiline = False, size_hint = (0.05, 0.05), pos_hint = {'x':0.65, 'y':0.55 }, input_filter = "float")
			self.add_widget(self.Inch)	

		
		self.centi.bind(text = cm_to_feetinch)
		
		### Widget for Weight Inputs
		self.kilo = TextInput(text = "kg", multiline = False, size_hint = (0.07, 0.05), pos_hint = {'x':0.55, 'y':0.5 }, input_filter = "float")
		self.add_widget(self.kilo)
		
		self.kiloLabel = Label(text = "kg", size_hint = (0.05,0.05), pos_hint = {'x':0.62, 'y':0.5 })
		self.add_widget(self.kiloLabel)
		
		
		### Widget for Weight Conversion
		self.weightConv = Label(text = "(equiv: ", size_hint = (0.05,0.05), pos_hint = {'x':0.73, 'y':0.5 })
		self.add_widget(self.weightConv)
		
		self.lbs = TextInput(text = "lbs", multiline = False, size_hint = (0.07, 0.05), pos_hint = {'x':0.78, 'y':0.5 })
		self.add_widget(self.lbs)		
		
		self.lbsLabel = Label(text = " lbs)", size_hint = (0.03,0.05), pos_hint = {'x':0.85, 'y':0.5 })
		self.add_widget(self.lbsLabel)	
		
		def kilo_to_lbs(instance, value):
			kilo = self.kilo.text
								
			if kilo == "":
				lbs = 0
			else:
				###### 1 kg = 2.20462 lbs
				boom = float(kilo)*2.20462
				lbs = round(boom, 2)
				
			self.lbs = TextInput(text = str(lbs), multiline = False, size_hint = (0.07, 0.05), pos_hint = {'x':0.78, 'y':0.5 })
			
			self.add_widget(self.lbs)
		
		self.kilo.bind(text = kilo_to_lbs)
				
		def lbs_to_kilo(instance, value):
			lbs = self.lbs.text
								
			if lbs == "":
				kilo = 0
			else:
				###### 1 lb = 0.45359 kg
				boom = float(lbs)*0.45359
				kilo = round(boom, 2)		
		
			self.kilo = TextInput(text = str(kilo), multiline = False, size_hint = (0.07, 0.05), pos_hint = {'x':0.55, 'y':0.5 })
			
			self.add_widget(self.kilo)

		self.lbs.bind(text = lbs_to_kilo)
		
		
		### Widget for Trial Start/End Date Selection (Spinner)
		for j in range(0,2): # Sets vertical
			for i in range(0,3): # Sets horizontal
				self.trialStart = Spinner(
					text = AGE[i],
					values = BOOM[i],
					size_hint = (0.1, 0.05),
					#size = (100,44),
					pos_hint = {'center_x':0.6+i/10, 'center_y':0.475-j/20},
					sync_height = True)
				self.add_widget(self.trialStart)
		
		
		### Widget for Confirm/Skip Buttons
		self.Confirm = Button(text = "Confirm", size_hint = (0.2,0.05), pos_hint = {'left':0, 'bottom':0})
		self.add_widget(self.Confirm)
		
		self.Skip = Button(text = "Skip", size_hint = (0.2,0.05), pos_hint = {'right':1, 'bottom':0})
		self.add_widget(self.Skip)
		
		
		### Widget for Back Button (to Intro Page)
		self.BackToIntro = Button(text = "Back to Intro Page", size_hint = (0.3,0.05), pos_hint = {'center_x':0.5, 'bottom':0})
		self.add_widget(self.BackToIntro)
		
		def PageChange(self):
			Patient_Deets.screen_manager.current = "Introduction Page"
			
		self.BackToIntro.bind(on_release = PageChange)
		



class IntroPage(FloatLayout):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
	
		NIST = ["N", "I", "S", "T"]
		NIST_2 = ["on", "nvasive", "ampling", "echnology"]
	
		### Widget for Introductory Title
		self.Title = Button(text = "[size=35] Welcome to... [/size]", size_hint = (0.3,0.1), pos_hint = {'top': 1, 'center_x':0.5}, markup = True)
		self.add_widget(self.Title)	
		
		### Widget for Researcher Interface (Patient Details)
		self.researcherInterface = Button(text = "Researcher Interface", size_hint = (0.3, 0.05), pos_hint = {'center_x': 0.8, 'center_y':0.8})
		self.add_widget(self.researcherInterface)
		
		### Widget for Patient Interface (get from David)
		self.patientInterface = Button(text = "Patient Interface", size_hint = (0.3, 0.05), pos_hint = {'center_x': 0.8, 'center_y':0.5})
		self.add_widget(self.patientInterface)
		
		### Widget for NIST Title
		for i in range(0,4):
			self.Letter = Label(text = f"[size=95] {NIST[i]} [/size]" , pos_hint = {'center_x': 0.1, 'center_y': 0.8-i/5}, size_hint = (0.3,0.3), markup=True)
			
			self.Name = Label(text = f"[size=25] {NIST_2[i]} [/size]" , pos_hint = {'center_x': 0.2, 'y': 0.625-i/5}, size_hint = (0.3,0.3), markup=True)			
			self.add_widget(self.Letter)
			self.add_widget(self.Name)
		
		def GoToResearcher(self):
			Patient_Deets.screen_manager.current = "Patient Details Screen"
		
		self.researcherInterface.bind(on_release = GoToResearcher)
		


class PatientDetailsBuild(App):
	def build(self):
		self.screen_manager = ScreenManager()
		
		screen = Screen(name = "Introduction Page")
		self.intro_page = IntroPage()
		screen.add_widget(self.intro_page)
		self.screen_manager.add_widget(screen)		
		
		screen = Screen(name = "Patient Details Screen")
		self.patient_details = PatientDetails()
		screen.add_widget(self.patient_details)
		self.screen_manager.add_widget(screen)
		
		
		return self.screen_manager

if __name__ == "__main__":
	Patient_Deets = PatientDetailsBuild()
	Patient_Deets.run()

















##################################################
########### OLD/UNUSED CODE ######################
##################################################

# class CustomSpinBox(DropDown):
	# def __init__(self, **kwargs):
		# super(CustomSpinBox, self).__init__(**kwargs)
		# self.drop_list = None
		# self.drop_list = DropDown()
		
		# types = ["item1", "item2", "item3"]
		
		# for item in types:
			# btn = Button(text = item, size_hint_y = None, height = 50, pos_hint = {'top':0.8, 'right':1.0})
			# btn.bind(on_release = lambda btn: self.drop_list.select(btn.text))
			# self.drop_list.add_widget(btn)
		
		# self.bind(on_release = self.drop_list.open)
		# self.drop_list.bind(on_select = lambda instance, x: setattr(self, 'text', x))
#spinbox = DropDown()
	
# class CustomSpinBox(DropDown):
	# def __init__(self, **kwargs):
		# self.spinbox = DropDown()
		
		# for months in range(1,13):
			# Month = Button(text = "months %d" % months, size_hint_y = None, height = 44)
			# Month.bind(on_release = lambda Month: self.spinbox.select(Month.text))
			
			# #self.add_widget(self.Month)
			
			# self.spinbox.add_widget(Month)
		
		# self.bind(on_release = self.spinbox.open)
		# self.spinbox.bind(on_select = lambda instance, x: setattr(self, 'text', x))






		# ### Widget for Patient Name
		# self.add_widget(Button(text = "Patient Name: ", size_hint = (0.2, 0.1), pos_hint = { 'x':0.1, 'y':0.8 }))
		# self.Name = TextInput(text = "insert_name", multiline = False, size_hint = (0.2, 0.1), pos_hint = {'x':0.3, 'y':0.8 })
		# self.add_widget(self.Name)
		
		# ### Widget for Subject Number
		# self.add_widget(Button(text = "Subject Number: ", size_hint = (0.2, 0.1), pos_hint = { 'x':0.1, 'y':0.7 }))
		# self.Name = TextInput(text = "insert_num", multiline = False, size_hint = (0.2, 0.1), pos_hint = {'x':0.3, 'y':0.7 })
		# self.add_widget(self.Name)
		
		# ### Widget for D.O.B
		# self.add_widget(Button(text = "Date of Birth: ", size_hint = (0.2, 0.1), pos_hint = { 'x':0.1, 'y':0.6 }))
		# self.Name = TextInput(text = "insert_num", multiline = False, size_hint = (0.2, 0.1), pos_hint = {'x':0.3, 'y':0.6 })
		# self.add_widget(self.Name)

		# ### Widget for Age
		# self.add_widget(Button(text = "Age: ", size_hint = (0.2, 0.1), pos_hint = { 'x':0.1, 'y':0.5 }))
		# self.Name = TextInput(text = "insert_num", multiline = False, size_hint = (0.2, 0.1), pos_hint = {'x':0.3, 'y':0.5 })
		# self.add_widget(self.Name)			
		
		# ### Widget for Sex
		# self.add_widget(Button(text = "Sex: ", size_hint = (0.2, 0.1), pos_hint = { 'x':0.1, 'y':0.4 }))
		# self.Name = TextInput(text = "insert_num", multiline = False, size_hint = (0.2, 0.1), pos_hint = {'x':0.3, 'y':0.4 })
		# self.add_widget(self.Name)			
		
		# ### Widget for Height
		# self.add_widget(Button(text = "Height: ", size_hint = (0.2, 0.1), pos_hint = { 'x':0.1, 'y':0.3 }))
		# self.Name = TextInput(text = "insert_num", multiline = False, size_hint = (0.2, 0.1), pos_hint = {'x':0.3, 'y':0.3 })
		# self.add_widget(self.Name)			
		
		# ### Widget for Weight
		# self.add_widget(Button(text = "Weight: ", size_hint = (0.2, 0.1), pos_hint = { 'x':0.1, 'y':0.2 }))
		# self.Name = TextInput(text = "insert_num", multiline = False, size_hint = (0.2, 0.1), pos_hint = {'x':0.3, 'y':0.2 })
		# self.add_widget(self.Name)			
				
		# ### Widget for Trial Start Date
		# self.add_widget(Button(text = "Trial Start Date ", size_hint = (0.2, 0.1), pos_hint = { 'x':0.1, 'y':0.1 }))
		# self.Name = TextInput(text = "insert_num", multiline = False, size_hint = (0.2, 0.1), pos_hint = {'x':0.3, 'y':0.1 })
		# self.add_widget(self.Name)			
		
		### Widget for Trial End Date
		
		
		### Widget for Number of Questions




####################################################3		
		#self.spinbox = DropDown()
		
		#self.CustomSpinBox(DropDown)
		
		
		# for month in range(1,12,1):
			# self.Month = Button(text = "month %d" % month, size_hint_y = None, height = 44)
			
			# #self.add_widget(self.Month)
			
			# self.spinbox.add_widget(self.Month)
		#runTouchApp()
		#self.spinbox.open(self)	
#######################################################3

		#self.cols = 2
		#self.rows = 4


		#DAYS = ['0','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31']

		#YEARS = ['2000','2001','2002']

		# self.ageMonth = Spinner(
			# text = "Month",
			# values = MONTHS,
			# size_hint = (0.1, 0.05),
			# pos_hint = {'center_x':0.6, 'center_y':0.725},
			# sync_height = True)
		# self.add_widget(self.ageMonth)
		
		# self.ageDay = Spinner(
			# text = "Day",
			# values = DAYS,
			# size_hint = (0.1, 0.05),
			# pos_hint = {'center_x':0.7, 'center_y':0.725},
			# sync_height = True)
		# self.add_widget(self.ageDay)		

		# self.ageYear = Spinner(
			# text = "Year",
			# values = YEARS,
			# size_hint = (0.1, 0.05),
			# pos_hint = {'center_x':0.8, 'center_y':0.725},
			# sync_height = True)
		# self.add_widget(self.ageYear)	




		# self.ageMonth = Spinner(
			# text = "Month",
			# values = MONTHS,
			# size_hint = (0.1, 0.05),
			# pos_hint = {'center_x':0.6, 'center_y':0.425},
			# sync_height = True)
		# self.add_widget(self.ageMonth)
		
		# self.ageDay = Spinner(
			# text = "Day",
			# values = DAYS,
			# size_hint = (0.1, 0.05),
			# pos_hint = {'center_x':0.7, 'center_y':0.425},
			# sync_height = True)
		# self.add_widget(self.ageDay)		

		# self.ageYear = Spinner(
			# text = "Year",
			# values = YEARS,
			# size_hint = (0.1, 0.05),
			# pos_hint = {'center_x':0.8, 'center_y':0.425},
			# sync_height = True)
		# self.add_widget(self.ageYear)	



		# self.spinner = CustomSpinBox()
		# screen.add_widget(self.spinner)



		#######################
		# THIS WIDGET BELOW  (sex radio buttons) INTERFERES WITH THE
		# INPUT BOXES FOR SOME REASON
		### Fixed it! Their size_hint wasn't set, so
		### their area-of-affect was probably huge
		######################




# import xlsxwriter

# workbook = xlsxwriter.Workbook("NIST_TEST.xlsx")
# sheet1 = workbook.add_worksheet()

# expenses = [
	# ["Rent", 2000],
	# ["Gas", 200],
	# ["Food", 300],
	# ["Gym", 70]
# ]


# PATIENT_ATTRIBUTES = ["Name", "Subject Number", "Date of Birth", "Age", "Sex", "Height", "Weight", "Trial Start Date", "Trial End Date", "Number of Questions"]

# rowStart = 3 #Row 4
# rowStart2 = 0
# colStart = 4 #Column E

# for item, cost in expenses:
	# sheet1.write(rowStart, colStart, item)
	# sheet1.write(rowStart, colStart+1, cost)
	# rowStart += 1
	
# for attribute in PATIENT_ATTRIBUTES:
	# sheet1.write(rowStart2, colStart-4, attribute)
	# rowStart2 += 1
	
# sheet1.write_formula("F8", "=sum(F4:F7)")

# workbook.close()
