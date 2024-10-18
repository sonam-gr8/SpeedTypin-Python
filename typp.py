import tkinter as tk
import time 
import threading 
import random 
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

class TypeSpeedGUI:

    def __init__(self):
        self.root=tk.Tk()
        self.root.title("Typing Speed Application")
        self.root.geometry("800x600")

        self.frame = tk.Frame(self.root)

        self.sample_label=tk.Label(self.root,text=self.generate(),wraplength=300,justify='center')
        self.sample_label.pack(fill='x',padx=5,pady=10)
        #self.sample_label.grid(row=0,column=0,rowspan=3,columnspan=2,padx=5,pady=5)

        self.input_entry = tk.Entry(self.root,width=40,font=("Helvetica",24))
        self.input_entry.pack()
        #self.input_entry.grid(row=1,column=0,columnspan=2,padx=5,pady=10)
        self.input_entry.bind("<KeyRelease>",self.start)

        self.speed_label= tk.Label(self.root,text="Speed :\n0.00 CPS\n0.00 CPM\n0.00 WPS\n0.00 WPM",font=("Helvetica",18))
        #self.speed_label.grid(row=2,column=0,columnspan=2,padx=5,pady=10)]
        self.speed_label.pack()

        self.reset_button = tk.Button(self.root,text="Reset", command=self.reset)
        #self.reset_button.grid(row=3,column=0,padx=5,pady=10)
        self.reset_button.pack()
        #self.frame.pack(expand=True)

        self.counter=0
        self.running=False

        self.root.mainloop()

    def start(self,event):
        if not self.running:
            if not   event.keycode in [16,17,18]:
                self.running=True 
                t= threading.Thread(target=self.time_thread)
                t.start()
        if not self.sample_label.cget('text').startswith(self.input_entry.get()):
            self.input_entry.config(fg="red")

        else:
            self.input_entry.config(fg="black")
        if self.input_entry.get()==self.sample_label.cget('text'):
            self.running=False
            self.input_entry.config(fg="green")

    def time_thread(self):
        while self.running:
            time.sleep(0.1)
            self.counter +=0.1

            cps=len(self.input_entry.get())/self.counter
            cpm=cps*60
            wps=len(self.input_entry.get().split(" "))/self.counter
            wpm=wps*60
            self.speed_label.config(text=f"Speed:  \n{cps:.2f} CPS\n{cpm:.2f} CPM\n {wps:.2f} WPS\n {wpm:.2f} WPM")

    def reset(self):
        self.running=False
        self.counter=0
        self.speed_label.config(text="Speed :\n0.00 CPS\n0.00 CPM\n0.00 WPS\n0.00 WPM")
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
 
TypeSpeedGUI()