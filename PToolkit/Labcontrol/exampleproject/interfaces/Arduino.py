from LabControl import *
import tkinter as tk
from tkinter import ttk
import sys

sys.path.append("dependencies/")

#from PToolkit.LabControl import *
import tkinter as tk
import serial, queue


class Arduino(Interface):

    def __init__(self, root, name):
        Interface.__init__(self, root, name)

        self.valign = VerticalAllign(self)

        self.terminal = Terminal(self)
        
        self.serial = serial.Serial(baudrate=9600)
        
        self.portselector = SerialPortSelector(self.valign, self.serial, terminal=self.terminal)

        self.var = ParameterField(self.valign, "Value to send")

        self.button = Button(self.valign, text="Send", command=self.SendVar)       

        self.arduino_queue = queue.Queue(10)

        self.prod = ProducerThread(
            name="ArduinoRead",
            generationfunction=self.ReadArduino, 
            queue=self.arduino_queue,
            interval=0.1,
            terminal=self.terminal
        ) 

        self.cons = ConsumerThread(
            name="TerminalPrinter",
            consumerfunction=self.terminal.terminal_msg,
            queue=self.arduino_queue,
            interval=0.1,
            terminal=self.terminal
            )

        self.prod.start()
        self.cons.start()

    def __GUI__(self):
        self.valign.grid(row=0, column=0, sticky="N")
        self.terminal.grid(row=0, column=1)
    
    def ReadArduino(self):
        try:
            return self.serial.readline().decode("utf-8").rstrip()
        except:
            pass
    
    def SendVar(self):
        msg = (str(self.var) + "\n").encode("utf-8")
        self.serial.write(msg)
    







