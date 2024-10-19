import tkinter as tk 
import time 
import threading
from tkinter import PhotoImage
from PIL import ImageTk,Image 
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

acc=100 
val=0

class Speed_Type:

	def __init__(self):
		global val
		self.window=tk.Tk()
		self.window.title("Speed Typing")
		self.window.geometry("800x600")

		img=Image.open('bluerect.jpg')
		img=ImageTk.PhotoImage(img)
		self.back=tk.Label(self.window,image=img)
		self.back.pack(padx=100,pady=100)

		self.speed_label=tk.Label(self.back,text="Speed :\tWPM :\tAccuracy\n0.00\t0.00\t100%",bg="LightBlue")
		self.speed_label.pack()

		self.sample_label=tk.Label(self.back,text="Nigga PLease",wraplength=300,justify='center',bg="LightBlue")
		self.sample_label.pack(fill='x',padx=5,pady=10)

		self.input_entry=tk.Text(self.back,height=5,width=40,padx=20,pady=20)
		self.input_entry.place()
		self.input_entry.pack(padx=20,pady=20)
		self.input_entry.bind("<KeyRelease>",self.start)

		self.reset_button = tk.Button(self.back,text="Reset", command=self.reset)
		self.reset_button.pack(pady=10)

		self.counter=0
		self.running=False

		self.window.mainloop()

	def start(self,event):
		global val
		if not self.running:
			if not   event.keycode in [16,17,18]:
				self.running=True 
				t= threading.Thread(target=self.time_thread)
				t.start()
		if event.keycode ==8: 
			val-=1
			print(val)
			self.sample_label.config(underline=val)

		if not self.sample_label.cget('text').startswith(self.input_entry.get("1.0","end-1c")):
			self.input_entry.config(fg="red")
			self.decacc()

		else:
			if val==0:
				self.sample_label.config(underline=val)
				val+=1
			else:
				self.sample_label.config(underline=val)
				val+=1

			self.input_entry.config(fg="black")
		if self.input_entry.get("1.0","end-1c")==self.sample_label.cget('text'):
			self.running=False
			self.input_entry.config(fg="green")

	def time_thread(self):
		while self.running:
			global acc
			time.sleep(0.1)
			self.counter +=0.1

			cps=len(self.input_entry.get("1.0","end-1c"))/self.counter
			cpm=cps*60
			wps=len(self.input_entry.get("1.0","end-1c").split(" "))/self.counter
			wpm=wps*60
			self.speed_label.config(text=f"Speed :\tWPM :\tAccuracy\n{cps:.2f}\t{wpm:.2f}\t{acc:.2f}%")
	def decacc(self):
		global acc
		acc = acc - 0.2
		return acc
	def reset(self):
		global acc,val 
		acc=100
		val=0
		self.running=False
		self.counter=0
		self.speed_label.config(text="Speed :\tWPM :\tAccuracy\n0.00\t0.00\t100%")
		self.sample_label.config(text=self.generate())
		self.input_entry.delete(0,tk.END)

	def generate(self):
		chrome_options = Options()
		chrome_options.add_experimental_option("detach", True)
		chrome_options.add_argument("headless")

		driver = webdriver.Chrome(options=chrome_options)
		driver.get("https://randomword.com/paragraph")
		text=driver.find_element(By.ID,"random_word_definition").text
		return text

Speed_Type()

