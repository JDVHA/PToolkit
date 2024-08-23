from LabControl import Interface
import tkinter as tk
from tkinter import ttk
import sys, serial, queue
import numpy as np

from LabControl import SerialPortSelector, KeyBoard, SevenSegmentDisplay, ConsumerThread, ProducerThread
sys.path.append("dependencies/")

class TTi_1604(Interface):

    def __init__(self, root, name):
        Interface.__init__(self, root, name)
        
        self.serial = serial.Serial()
        self.selector = SerialPortSelector(self, self.serial)

        self.keyboard = KeyBoard(self, np.ones((3, 4)),
                                [
                                    ["mV", "V", "\u2126", "\u2191"],
                                    ["mA", "A", "Hz", "\u2193"],
                                    ["DC", "AC", "SHIFT", "Auto"]
                                 ]
                                )
        
        self.dis = SevenSegmentDisplay(self, 5) #, style="rectangle"
        self.q = queue.Queue(10)

        ConsumerThread("ScreenUpdate", self.dis.UpdateDisplay, self.q).Start()
        ProducerThread("ReadData", self.Read_Data, self.q).Start()


        self.__GUI__()
        
    def __GUI__(self):
        self.dis.grid(row=1, column=0, sticky="nesw")
        self.selector.grid(row=0, column=0, sticky="nesw")
        self.keyboard.grid(row=1, column=1, sticky="nesw")
    
    def Read_Data(self):
        return np.random.uniform(-200, 200)

    def Key_Up(self):
        self.serial.write(b"a")

    def Key_Down(self):
        self.serial.write(b"b")

    def Key_Auto(self):
        self.serial.write(b"c")

    def Key_A(self):
        self.serial.write(b"d")

    def Key_mA(self):
        self.serial.write(b"e")

    def Key_V(self):
        self.serial.write(b"f")

    def Key_Operate(self):
        self.serial.write(b"g")

    def Key_Omega(self):
        self.serial.write(b"i")

    def Key_Hz(self):
        self.serial.write(b"j")

    def Key_Shift(self):
        self.serial.write(b"k")

    def Key_AC(self):
        self.serial.write(b"l")

    def Key_DC(self):
        self.serial.write(b"m")

    def Key_mV(self):
        self.serial.write(b"n")

    def Key_Ser_remote_mode(self):
        self.serial.write(b"u")

    def Set_local_mode(self):
        self.serial.write(b"v")
