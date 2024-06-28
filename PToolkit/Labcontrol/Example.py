from LabControl import MainPToolkitApp, Interface, ParameterField, SerialPortSelector, Terminal, Display, TkLivePlot, StatusLED, TkTable
import tkinter as tk
import math, serial, random

class Arduino(Interface):

    def __init__(self, root, name):
        Interface.__init__(self, root, name)
        
        self.serial = serial.Serial()
                
        self.terminal = Terminal(self)

        self.serialselector = SerialPortSelector(self, self.serial, terminal=self.terminal)
        self.serialselector.pack()

        self.position = ParameterField(self, text="x", unit="m")
        self.position.pack()

        self.speed = ParameterField(self, text="Speed", unit="m/s")
        self.speed.pack()

        self.actualspeed = Display(self, text="Actual speed:", unit="m/s")
        self.actualspeed.pack()

        self.button1 = tk.Button(self.frame, text="A", command=self.MyMethod)
        self.button1.pack()

        self.LED = StatusLED(self, text="Status:")
        self.LED.pack()

        self.terminal.pack()

        self.plot = TkLivePlot(self.frame)
        self.plot.pack()
        
        self.RegisterKey("Key1", self.terminal.Terminal_msg)
        self.RegisterKey("Key2", lambda x: print(x, 1))
        self.terminal.Add_Commands(self.commands)
        

    @Interface.RegisterCommand("test", ["Key1", "Key2"])
    def MyMethod(self):
        self.actualspeed.set(random.randint(1, 10))
        self.plot.Appendy(random.randint(1, 10))
        self.LED.Toggle_State()
        return math.cos(self.speed)
    
    @Interface.RegisterCommand("test1", ["Key2"])
    def MyMethod1(self):
        return 1



root = MainPToolkitApp()

A = Arduino(root, "Arduino1")
A.pack()

root.mainloop()


