import customtkinter as ctk
from buttons import Button, ImageButton, NumButton, MathButton, MathImageButton
import darkdetect
from PIL import Image
from settings import *
import speech_recognition as sr
try:
	from ctypes import windll, byref, sizeof, c_int
except:
	pass

class Calculator(ctk.CTk):
	def __init__(self, is_dark):
		
		# setup 
		super().__init__(fg_color = (WHITE, BLACK))
		ctk.set_appearance_mode("dark")#f'{"dark" if is_dark else "light"}'
		self.geometry(f'{APP_SIZE[0]}x{APP_SIZE[1]}')
		self.resizable(False, False)
		self.title('cloning iphone caculator')
		self.iconbitmap('empty.ico')
		self.title_bar_color(is_dark)

		# grid layout
		self.rowconfigure(list(range(MAIN_ROWS)), weight = 1, uniform = 'a')
		self.columnconfigure(list(range(MAIN_COLUMNS)), weight = 1, uniform = 'a')

		# data 
		self.result_string = ctk.StringVar(value = '0')
		self.formula_string = ctk.StringVar(value = '')
		self.display_nums = []
		self.full_operation = []
		# Liste pour stocker l'historique
		self.history = []  

		# widgets 
		self.create_widgets()

		self.mainloop()

	def create_widgets(self):
		# fonts 
		main_font = ctk.CTkFont(family = FONT, size = NORMAL_FONT_SIZE)
		result_font = ctk.CTkFont(family = FONT, size = OUTPUT_FONT_SIZE)

		# output labels 
		OutputLabel(self, 0,'SE', main_font, self.formula_string) # formula
		OutputLabel(self, 1,'E', result_font, self.result_string) # result

		# clear (AC) button
		Button(
			parent = self, 
			func = self.clear,
			text = OPERATORS['clear']['text'], 
			col = OPERATORS['clear']['col'], 
			row = OPERATORS['clear']['row'],
			font = main_font)

		# percentage button
		Button(
			parent = self, 
			func = self.percent,
			text = OPERATORS['percent']['text'], 
			col = OPERATORS['percent']['col'], 
			row = OPERATORS['percent']['row'],
			font = main_font)

		# invert button
		invert_image = ctk.CTkImage(
			light_image = Image.open(OPERATORS['invert']['image path']['dark']),
			dark_image = Image.open(OPERATORS['invert']['image path']['light']))
		ImageButton(
			parent = self, 
			func = self.invert, 
			col = OPERATORS['invert']['col'], 
			row = OPERATORS['invert']['row'], 
			image = invert_image)

		# Historique Button 
		Button(parent=self, func=self.show_history,text="Historique", col=0, row=7, font=ctk.CTkFont(family=FONT, size=14))

		# Permet d'ajouter 'i' pour les nombres imaginaires
		Button(
    parent = self,
    func = lambda: self.num_press('i'),  
    text = "i",
    col = 1,  # Placez le bouton à un endroit libre dans la grille
    row =7 ,  # Par exemple, à côté des autres opérations mathématiques
    font = main_font
)


        # Ajouter le bouton micro
		Button(
			parent=self,
			func=self.voice_input,
			col=2,
			row=7,
			text='voice',
			font=main_font)


		# number buttons
		for num, data in NUM_POSITIONS.items():
			NumButton(
				parent = self, 
				text = num, 
				func = self.num_press, 
				col = data['col'], 
				row = data['row'], 
				font = main_font,
				span = data['span'])

		# math buttons
		for operator, data in MATH_POSITIONS.items():
			if data['image path']:
				divide_image = ctk.CTkImage(
					light_image = Image.open(data['image path']['dark']),
					dark_image = Image.open(data['image path']['light']),
					)

				MathImageButton(
					parent = self,
					operator = operator, 
					func = self.math_press, 
					col = data['col'], 
					row = data['row'], 
					image = divide_image)
			else:
				MathButton(
					parent = self, 
					text = data['character'], 
					operator = operator, 
					func = self.math_press, 
					col = data['col'], 
					row = data['row'], 
					font = main_font)

	def num_press(self, value):
		self.display_nums.append(str(value))
		full_number = ''.join(self.display_nums)
		self.result_string.set(full_number)

	def math_press(self, value):
		current_number = ''.join(self.display_nums)

		if current_number:
			self.full_operation.append(current_number)

			if value != '=':
		        # Ajout de l'opérateur aux opérations
				self.full_operation.append(value)
				self.display_nums.clear()
		        # Mise à jour de l'affichag
				self.result_string.set('')
				self.formula_string.set(' '.join(self.full_operation))

			else:
				formula = ' '.join(self.full_operation)
				try:
					result = eval(formula.replace('i', 'j'))  # Conversion 'i' en 'j' pour nombres complexes

					if isinstance(result, float):
						if result.is_integer():
							result = int(result)
						else:
							result = round(result, 3)

					self.full_operation.clear()
					self.display_nums = [str(result)]

	                # Mise à jour de l'affichage
					self.result_string.set(result)
					self.formula_string.set(formula)
				except Exception as e:
					self.result_string.set("Erreur")


	def clear(self):
		# clear the output
		self.result_string.set(0)
		self.formula_string.set('')

		# clear the data
		self.display_nums.clear()
		self.full_operation.clear()

	def percent(self):
		if self.display_nums:
			
			# get the percentage number
			current_number = float(''.join(self.display_nums))
			percent_number = current_number / 100

			# update the data and output
			self.display_nums = list(str(percent_number))
			self.result_string.set(''.join(self.display_nums))

	def invert(self):
		current_number = ''.join(self.display_nums)
		if current_number:
			# positive / negative
			if float(current_number) > 0:
				self.display_nums.insert(0, '-')
			else:
				del self.display_nums[0]

			self.result_string.set(''.join(self.display_nums))

	def title_bar_color(self, is_dark):
		try:
			HWND = windll.user32.GetParent(self.winfo_id())
			DWMWA_ATTRIBUTE = 35
			COLOR = TITLE_BAR_HEX_COLORS['dark'] if is_dark else TITLE_BAR_HEX_COLORS['light']
			windll.dwmapi.DwmSetWindowAttribute(HWND, DWMWA_ATTRIBUTE, byref(c_int(COLOR)), sizeof(c_int))
		except:
			pass


	def show_history(self):
	    history_window = ctk.CTkToplevel(self)  # Fenêtre secondaire
	    history_window.geometry("300x400")
	    history_window.title("Historique des calculs")
	    
	    history_listbox = ctk.CTkTextbox(history_window, width=300, height=400)
	    history_listbox.grid(row=0, column=0)

	    # Remplir la zone avec l'historique
	    for item in self.history:
	        history_listbox.insert('end', item + "\n")


	def show_history(self):
	    history_window = ctk.CTkToplevel(self)
	    history_window.geometry("300x400")
	    history_window.title("Historique des calculs")
	    
	    history_listbox = ctk.CTkTextbox(history_window, width=300, height=400)
	    history_listbox.grid(row=0, column=0)

	    # Remplir la zone avec l'historique
	    for item in self.history:
	        history_listbox.insert('end', item + "\n")
	    
	    # Permettre la sélection d'un calcul
	    history_listbox.bind("<Double-1>", lambda event: self.reuse_calculation(event, history_listbox))
    
	def reuse_calculation(self, event, listbox):
	    # Obtenir le calcul sélectionné
	    selection = listbox.get('current linestart', 'current lineend')
	    
	    # Extraire le résultat du calcul
	    result = selection.split('=')[-1].strip()
	    
	    # Réutiliser le résultat dans le champ de saisie
	    self.result_string.set(result)
	    self.display_nums = [result]

	def abs_press(self):
	    current_number = ''.join(self.display_nums)
	    if current_number:
	        try:
	            complex_num = complex(current_number.replace('i', 'j'))
	            result = abs(complex_num)
	            self.result_string.set(result)
	        except ValueError:
	            self.result_string.set("Erreur")

	
	def voice_input(self):
		recognizer = sr.Recognizer()
		with sr.Microphone() as source:
			print("Parlez maintenant...")
			audio = recognizer.listen(source)
			try:
                # Utilise Google Web Speech API pour convertir l'audio en texte
				input_string = recognizer.recognize_google(audio, language="fr-FR")
				print(f"Vous avez dit : {input_string}")

                # Convertir le texte pour l'utiliser dans le calcul
				input_string = input_string.replace("deux", "2").replace("plus", "+").replace("moins", "-").replace("fois", "*").replace("divisé par", "/").replace("égal", "=")
				self.full_operation.append(input_string)
				self.math_press('=')
			except sr.UnknownValueError:
				print("Je n'ai pas pu comprendre l'audio.")
				self.result_string.set("Erreur de reconnaissance")
			except sr.RequestError as e:
				print(f"Erreur de service de reconnaissance vocale : {e}")
				self.result_string.set("Erreur de service")
            



class OutputLabel(ctk.CTkLabel):
	def __init__(self, parent, row, anchor, font, string_var):
		super().__init__(master = parent, font = font, textvariable = string_var)
		self.grid(column = 0, columnspan = 4, row = row, sticky = anchor, padx = 10)

if __name__ == '__main__':
	Calculator(False)