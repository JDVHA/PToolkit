from Terminal import TkTerminal
from LabControl import Interface
from LabControl import MainPToolkitApp
import tkinter as tk


class Arduino(Interface):

    def __init__(self, root, name):
        Interface.__init__(self, root, name)
        self.terminal = TkTerminal(self.frame, "test")
        self.terminal.pack()

        self.RegisterKey("Key1", self.terminal.Terminal_msg)
        self.RegisterKey("Key2", print)

    @Interface.RegisterCommand("test", tk.Button, ["Key1"])
    def MyMethod(self):
        return 0
    
    @Interface.RegisterCommand("test1", tk.Button, ["Key2"])
    def MyMethod1(self):
        return 1



root = MainPToolkitApp()

A = Arduino(root, "MyArduino")
A.pack()

root.AppendInterface(A)
root.mainloop()