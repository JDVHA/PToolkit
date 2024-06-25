from LabControl import MainPToolkitApp, Interface, ParameterField, SerialPortSelector, Terminal, Display
import tkinter as tk
import math, serial

class Arduino(Interface):

    def __init__(self, root, name):
        Interface.__init__(self, root, name)
        
        self.serial = serial.Serial()
                
        self.terminal = Terminal(self.frame)

        self.serialselector = SerialPortSelector(self.frame, self.serial, terminal=self.terminal)
        self.serialselector.pack()

        self.position = ParameterField(self.frame, text="x", unit="m")
        self.position.pack()

        self.speed = ParameterField(self.frame, text="Speed", unit="m/s")
        self.speed.pack()

        self.actualspeed = Display(self.frame, text="Actual speed", unit="m/s")
        self.actualspeed.pack()

        self.terminal.pack()

        self.RegisterKey("Key1", self.terminal.Terminal_msg)
        self.RegisterKey("Key2", print)


    @Interface.RegisterCommand("test", tk.Button, ["Key1"])
    def MyMethod(self):
        self.actualspeed.set(self.speed)
        return math.cos(self.speed)
    
    @Interface.RegisterCommand("test1", tk.Button, ["Key2"])
    def MyMethod1(self):
        return 1



root = MainPToolkitApp()

A = Arduino(root, "Arduino1")
A.pack()

root.mainloop()

