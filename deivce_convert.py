import tkinter as tk 
import ttkbootstrap as ttk

"""
	The code snippet creates a simple GUI application using tkinter in Python to convert Xaf to
	Euro.
"""
	


def convert():
	mile_input = entry_double.get()
	km_output = mile_input/656.08
	output_string.set(km_output)

# window 
window = ttk.Window(themename = 'darkly')
window.title('DEMO APP')
window.geometry('300x150')

# title 
title_label = ttk.Label(master = window, text = 'XAF EN EURO', font = 'Calibri 24 bold')
title_label.pack()

# input field 
input_frame = ttk.Frame(master = window)
entry_double = tk.DoubleVar()
entry = ttk.Entry(master = input_frame, textvariable = entry_double)
button = ttk.Button(master = input_frame, text = 'Convertir', command = convert)
entry.pack(side = 'left', padx = 10)
button.pack(side = 'left')
input_frame.pack(pady = 10)

# output
output_string = tk.StringVar()
output_label = ttk.Label(
	master = window, 
	text = 'resulta', 
	font = 'Calibri 24', 
	textvariable = output_string)
output_label.pack(pady = 5)

# run 
window.mainloop()