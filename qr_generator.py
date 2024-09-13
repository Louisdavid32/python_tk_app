import tkinter as tk
from tkinter import filedialog
import customtkinter as ctk
from PIL import Image, ImageTk
import qrcode

class App(ctk.CTk):
	def __init__(self):

		# window setup
		ctk.set_appearance_mode('light')
		super().__init__(fg_color = 'white')

		# customization
		self.title('qr code generator')
		#self.iconbitmap('empty.ico')
		self.geometry('400x500')

		# Entry field
		self.entry_string = ctk.StringVar()
		self.entry_string.trace('w', self.create_qr)
		# make the save method callable from the EntryField button
		EntryField(self, self.entry_string, self.save)

		# event 
		# also call it when the enter key is pressed
		self.bind('<Return>', self.save)

		# exercise

		# QR code
		self.raw_image = None
		self.tk_image = None
		self.qr_image = QrImage(self)

		# running the app
		self.mainloop()

	def create_qr(self, *args):
		current_text = self.entry_string.get()
		if current_text:
			self.raw_image = qrcode.make(current_text).resize((400,400))
			self.tk_image = ImageTk.PhotoImage(self.raw_image)
			self.qr_image.update_image(self.tk_image)
		else:
			self.qr_image.clear()
			self.raw_image = None
			self.tk_image = None

	def save(self, event = ''):
		if self.raw_image:
			file_path = filedialog.asksaveasfilename()

			if file_path:
				self.raw_image.save(file_path + '.jpg')

class EntryField(ctk.CTkFrame):
	def __init__(self, parent, entry_string, save_func):
		super().__init__(master = parent, corner_radius = 20, fg_color = '#3178C6')
		self.place(relx = 0.5, rely = 1, relwidth = 1, relheight = 0.4, anchor = 'center')

		# grid layout 
		self.rowconfigure((0,1), weight = 1, uniform = 'a')
		self.columnconfigure(0, weight = 1, uniform = 'a')

		# widgets 
		self.frame = ctk.CTkFrame(self, fg_color = 'transparent')
		self.frame.columnconfigure(0, weight = 1, uniform = 'b')
		self.frame.columnconfigure(1, weight = 4, uniform = 'b')
		self.frame.columnconfigure(2, weight = 2, uniform = 'b')
		self.frame.columnconfigure(3, weight = 1, uniform = 'b')
		self.frame.grid(row = 0, column = 0)

		entry = ctk.CTkEntry(
			self.frame, 
			textvariable = entry_string,
			fg_color = '#2E54E8', 
			border_width = 0, 
			text_color = 'white')
		entry.grid(row = 0, column = 1, sticky = 'nsew')

		button = ctk.CTkButton(
			self.frame, 
			command = save_func,
			text = 'Enregistré', 
			fg_color = '#2E54E8', 
			hover_color = '#4266f1')
		button.grid(row = 0, column = 2, sticky = 'nsew', padx = 10)

class QrImage(tk.Canvas):
	def __init__(self, parent):
		super().__init__(
			master = parent, 
			background = '#3178C6', 
			bd = 0, 
			highlightthickness = 0, 
			relief = 'ridge')
		self.place(relx = 0.5, rely = 0.4, width = 400, height = 400, anchor = 'center')

	def update_image(self, image_tk):
		self.clear()
		self.create_image(0,0, image = image_tk, anchor = 'nw')

	def clear(self):
		self.delete('all')

App()