from PToolkit.LabControl import Interface
import tkinter as tk
from tkinter import ttk
import sys

sys.path.append("dependencies/")

class blankinterface(Interface):
    
    def __init__(self, root, name):
        Interface.__init__(self, root, name)

        self.label = tk.Label(self.frame, text="Welcome to PToolkit")

    def __GUI__(self):
        self.label.pack()


