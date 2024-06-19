from LabControl import MainPToolkitApp, Interface, ParameterField, SerialPortSelector, Terminal
import tkinter as tk
import math, serial

class Arduino(Interface):

    def __init__(self, root, name):
        Interface.__init__(self, root, name)
        
        self.serial = serial.Serial()
                
        self.terminal = Terminal(self.frame)
        

        self.serialselector = SerialPortSelector(self.frame, self.serial, terminal=self.terminal)
        self.serialselector.pack()

        self.position= ParameterField(self.frame, text="x", unit="m")
        self.position.pack()

        self.speed = ParameterField(self.frame, text="Speed", unit="m/s")
        self.speed.pack()

        self.terminal.pack()

        self.RegisterKey("Key1", self.terminal.Terminal_msg)
        self.RegisterKey("Key2", print)


    @Interface.RegisterCommand("test", tk.Button, ["Key1"])
    def MyMethod(self):
        return math.cos(self.speed)
    
    @Interface.RegisterCommand("test1", tk.Button, ["Key2"])
    def MyMethod1(self):
        self.serial.read(10)
        return 1



root = MainPToolkitApp()

A = Arduino(root, "MyArduino")
A.pack()

root.AppendInterface(A)
root.mainloop()

