from LabControl import Interface
import tkinter as tk
from tkinter import ttk
import sys

sys.path.append("dependencies/")

from LabControl import MainPToolkitApp, Interface, ParameterField, SerialPortSelector, Terminal, Display, Plot, StatusLED, TkTable, VerticalAllign, KeyBoard, ArrowKeyPad
import tkinter as tk
import math, serial, random, queue
from LabControl import ConsumerThread, ProducerThread

class Arduino(Interface):

    def __init__(self, root, name):
        Interface.__init__(self, root, name)
        
        self.serial = serial.Serial()
                
        self.terminal = Terminal(self)

        self.vallign = VerticalAllign(self)

        self.serialselector = SerialPortSelector(self.vallign, self.serial, terminal=self.terminal)

        self.position = ParameterField(self.vallign, text="x", unit="m")

        self.speed = ParameterField(self.vallign, text="Speed", unit="m/s")

        self.actualspeed = Display(self.vallign, text="Actual speed:", unit="m/s")

        self.vallign.grid(row=0, column=0, sticky="n")

        self.button1 = tk.Button(self.frame, text="ABC", command=self.MyMethod)
        self.button1.grid(row=1, column=0, sticky="n")

        self.LED = StatusLED(self, text="Status:")
        self.LED.grid(row=2, column=0, sticky="n")

        self.terminal.grid(row=3, column=0, sticky="n")

        self.plot = Plot(self.frame)
        self.plot.set_xlabel("Test")
        self.plot.set_ylabel("Test")
        self.plot.grid(row=0, column=1, rowspan=4, sticky="n")
        
        self.RegisterKey("Key1", self.terminal.Terminal_msg)
        self.RegisterKey("Key2", lambda x: print(x, 1))
        self.terminal.Add_Commands(self.commands)
        
        #KeyBoard(self, 
        #            grid=[[1, 0, 1]], textgrid=[["a", "b", "c"]]
        #        ).pack()
        #
        #ArrowKeyPad(self,includehome=True, buttons=8).pack()
        Q = queue.Queue(10)
        C = ConsumerThread("Thread1", self.plot.Appendy, Q)        
        P = ProducerThread("Thread2", self.ReadArduino, Q)
        #C.Start()
       

        self.startacq = tk.Button(self.frame, text="on/off", command=P.Toggle)
        self.startacq.grid(row=4, column=0)

    @Interface.RegisterCommand("test", ["Key1", "Key2"])
    def MyMethod(self):
        self.actualspeed.set(random.randint(1, 10))
        self.plot.Appendy(random.randint(1, 10))
        self.LED.Toggle_State()
        return math.cos(self.speed)
    
    @Interface.RegisterCommand("test1", ["Key2"])
    def MyMethod1(self):

        data = self.serial.readline()
        self.plot.Appendy(int(data))
        return self.speed
    
    @Interface.RegisterCommand("test1", ["Key2"])
    def ReadArduino(self):
        data = self.serial.readline()
        return float(data)







