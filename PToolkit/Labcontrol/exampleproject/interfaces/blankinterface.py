from LabControl import *

import tkinter as tk
from tkinter import ttk
import sys


sys.path.append("dependencies/")

#from PToolkit.LabControl import *

class blankinterface(Interface):

    def __init__(self, root, name):
        Interface.__init__(self, root, name)

        self.terminal = Terminal(self)

        self.var = ParameterField(self, "Variable")

        self.loader = ScriptLoader(self, terminal=self.terminal)

        
    def __GUI__(self):
        self.terminal.pack()
        self.loader.pack()
        self.var.pack()
         
    def mymethod(self, val):
        self.terminal.terminal_msg(f"This is mymethod speaking var is: {val}")

