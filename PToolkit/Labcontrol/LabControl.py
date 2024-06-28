import tkinter as tk
import logging, time, os
import threading
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from tkinter import ttk
from serial.tools.list_ports import comports

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        #logging.FileHandler("debug.log"),
        logging.StreamHandler()
    ]
)
PTOOLKITLOGGER = logging.getLogger()
PTOOLKITLOGGER.setLevel(logging.DEBUG)


INIT_FASE = True


class MainPToolkitApp(tk.Tk):
    def __init__(self, *kwargs, **args):
        tk.Tk.__init__(self, *kwargs, **args)

    def mainloop(self):
        self.StartApp()
        self.tk.mainloop()
    
    def StartApp(self):
        global INIT_FASE
        if not INIT_FASE:
            raise SystemError("""INIT_FASE was false. Possible causes: INIT_FASE was changed in the program by the user. Or a second App was created, a maximum of 1 App may exist per program.""")
        INIT_FASE = False
        PTOOLKITLOGGER.info(f"Just started the main application.")

class Interface:
    def __init__(self, master, name):
        self.classname = self.__class__.__name__
        self.name = name
        self.commands = {}
        self.keys = {}
        self.utilfuncs = ["RegisterCommand", "RegisterKey", "grid", "pack", "Post_init"]
        self.frame = tk.LabelFrame(master, text=name)
        PTOOLKITLOGGER.debug(f"Just created an instance of {self.classname}.")
        PTOOLKITLOGGER.debug(f"Starting post init of an {self.classname} instance.")

        for i in dir(self):
            if not (i.startswith("_") or i.endswith("_") or i in self.utilfuncs):
                if callable(getattr(self, i)):
                    name = getattr(self, i)()

                    self.commands[name] = getattr(self, i)

        PTOOLKITLOGGER.debug(f"Finished post init of an {self.classname} instance.")        

    def RegisterCommand(name, links=[]):
        
        def _Appenddict(function):
            
            def wrapper(*args):
                self = args[0]
                
                if INIT_FASE:
                    PTOOLKITLOGGER.debug(f"Registered {name} as a command for interface {self.classname}")
                    return name

                else:
                    for key in links:
                        f = self.keys[key]
                        f(function(*args))
                    return function(*args)
            
            return wrapper
        return _Appenddict

    def RegisterKey(self, keyname, function):
        PTOOLKITLOGGER.debug(f"Registered {keyname} as a key for interface {self.classname}")
        self.keys[keyname] = function

    def grid(self, *args, **kwargs):
        self.frame.grid(*args, **kwargs)

    def pack(self, *args, **kwargs):
        self.frame.pack(*args, **kwargs)


class Parameter:
    def __init__(self, source):
        self.source = source

    def __Check__(self, otherparam):
        val1 = self.source()
        
        if issubclass(type(otherparam), Parameter):
            val2 = otherparam.get()
            
            try:
                val1 = float(val1)
                val2 = float(val2)
            except:
                TypeError("Two parameters cannot be added")
            
            return val1, val2

        else:
            val2 = otherparam

            try:
                val1 = float(val1)
                val2 = float(val2)
            except:
                TypeError("Two parameters cannot be added")

            return val1, val2

    def __add__(self, otherparam):
        val1, val2 = self.__Check__(otherparam)
        return val1 + val2
    
    def __sub__(self, otherparam):
        val1, val2 = self.__Check__(otherparam)
        return val1 - val2
    
    def __mul__(self, otherparam):
        val1, val2 = self.__Check__(otherparam)
        return val1 * val2
    
    def __truediv__(self, otherparam):
        val1, val2 = self.__Check__(otherparam)
        return val1 / val2
    
    def __floordiv__(self, otherparam):
        val1, val2 = self.__Check__(otherparam)
        return val1 // val2
    
    def __mod__(self, otherparam):
        val1, val2 = self.__Check__(otherparam)
        return val1 % val2
    
    def __pow__(self, otherparam):
        val1, val2 = self.__Check__(otherparam)
        return val1 ** val2
    
    def __neg__(self):
        val = self.source()
        try:
            return -float(val)
        except:
            TypeError("Parameter is not numerical")
        
    def __lt__(self, otherparam):
        val1, val2 = self.__Check__(otherparam)
        return val1 < val2
    
    def __le__(self, otherparam):
        val1, val2 = self.__Check__(otherparam)
        return val1 <= val2
    
    def __eq__(self, otherparam):
        val1, val2 = self.__Check__(otherparam)
        return val1 == val2
    
    def __ne__(self, otherparam):
        val1, val2 = self.__Check__(otherparam)
        return val1 != val2
    
    def __ge__(self, otherparam):
        val1, val2 = self.__Check__(otherparam)
        return val1 >= val2
    
    def __gt__(self, otherparam):
        val1, val2 = self.__Check__(otherparam)
        return val1 > val2
    
    def __float__(self):
        val = self.source()
        
        try:
            return float(val)
        except:
            TypeError("Parameter is not numerical")

    def __str__(self):
        val = self.source()
        return str(val)

class Display(tk.Frame, Parameter):
    def __init__(self, root, text="", unit="-", font=2):
        tk.Frame.__init__(self, root.frame)
        self.unit = unit
        self.text = text 

        self.textvariable = tk.StringVar()

        self.textlabel = tk.Label(self, text=self.text, font=font, anchor="w")
        self.displaylabel = tk.Label(self, textvariable=self.textvariable, font=font)
        self.unitlabel = tk.Label(self, text=self.unit, font=font)

        self.textlabel.grid(row=0, column=0)
        self.displaylabel.grid(row=0, column=1)
        self.unitlabel.grid(row=0, column=2)

        self.textvariable.set("0")
        Parameter.__init__(self, self.get)

    def get(self):
        return self.textvariable.get()
    
    def set(self, value):
        if isinstance(value, ParameterField):
            value = value.get()
        self.textvariable.set(value)
        

class ParameterField(tk.Frame, Parameter):
    def __init__(self, root, text="", unit="-", font=2, save=True):
        tk.Frame.__init__(self, root.frame)
        
        self.unit = unit
        self.text = text 
        
        self.textLabel = tk.Label(self, text=self.text, font=font, anchor="w")
        self.spinBox = tk.Spinbox(self, font=font)
        self.unitlabel = tk.Label(self, text=self.unit, font=font)

        self.spinBox.insert(0, "0.0")

        Parameter.__init__(self, self.get)

        self.textLabel.grid(row=0, column=0, sticky='nesw')
        self.spinBox.grid(row=0, column=1, sticky='nesw')
        self.unitlabel.grid(row=0, column=2, sticky='nesw')
    

    def get(self):
        return self.spinBox.get()
    
class SerialPortSelector(tk.Frame):
    
    def __init__(self, root, serial, text="Serial devices: ", terminal=None):
        tk.Frame.__init__(self, root.frame)
        
        self.serial = serial
        self.terminal = terminal
        self.lastselect = None

        self.Label = tk.Label(self, text=text)
        self.ComboBox = ttk.Combobox(self)
        self.ComboBox.bind("<<ComboboxSelected>>", self.Set_port)
        self.Button = tk.Button(self, text="\u27F3", command=self.Get_serial_devices)
        

        self.Label.grid(row=0, column=0)
        self.ComboBox.grid(row=0, column=1)
        self.Button.grid(row=0, column=2)
        if self.terminal != None:
            self.terminal.Add_Commands({"reloadserial": self.Get_serial_devices})
        self.Get_serial_devices()

    def Set_port(self, e):
        device = self.ComboBox.current()
        if self.lastselect == device:
            self.serial.close()
       
        self.serial.port = list(self.devices.values())[device]
        self.serial.open()

              
        if self.terminal != None:

            device_name = list(self.devices.keys())[device]

            if self.serial.is_open and self.lastselect == device:
                self.terminal.Terminal_msg(f"Serial connection with {device_name} is re established.")

            elif self.serial.is_open:
                self.terminal.Terminal_msg(f"Serial connection with {device_name} is established.")

            else:
                self.terminal.Terminal_msg(f"Serial connection with {device_name} has failed.", True)

            self.lastselect = device

    def Get_serial_devices(self):
        """Get serial ports for available devices"""
        available_ports = comports()
        self.devices = {}
        
        for port, device, _ in sorted(available_ports):
            self.devices[device] = port

        self.ComboBox['values'] = list(self.devices.keys())

    
class Terminal(tk.LabelFrame):
    def __init__(self, root, text=None, allowcommands=True):
        super().__init__(root.frame, text=text)
        self.commands = {
            "list": self.List_commands
        }

        scrollbar = tk.Scrollbar(self)
        self.terminal = tk.Text(self, wrap="word", yscrollcommand=scrollbar.set, width=30, height=10)
        self.terminal.tag_config("ERROR", foreground="red")
        scrollbar.config(command=self.terminal.yview)
        
        self.terminal.grid(row=0, column=0)
        scrollbar.grid(row=0, column=1, sticky=tk.N+tk.S)
        self.terminal.config(state=tk.DISABLED)

        if allowcommands:
            self.entry = tk.Entry(self)
            self.entry.grid(row=1, column=0, sticky="NWSE")

            self.sendbutton = tk.Button(self, text="send", command=lambda: self.Run_Command(self.entry.get()))
            self.sendbutton.grid(row=1, column=1)

            self.entry.bind('<Return>', self.Entry_Run)
        
    def Terminal_msg(self, msg, error=False):
        self.terminal.config(state=tk.NORMAL)
        if error:
            self.terminal.insert(tk.END, f"ERROR: {msg}\n", "ERROR")
        else:
            self.terminal.insert(tk.END, f"{msg}\n")
        self.terminal.config(state=tk.DISABLED)
    
    def List_commands(self):
        """Lists all the commands available in terminal."""

        self.Terminal_msg("Available commands:")
        for name, function in self.commands.items():  
            self.Terminal_msg(f"\t{name}: {function.__doc__}")

    def Entry_Run(self, e):
        self.Run_Command(self.entry.get())

    def Run_Command(self, command):

        self.Terminal_msg(f"Input: {command}")

        # Decoder required
        try:
            self.commands[command]()
        except KeyError as e:
            self.Terminal_msg("Unkown command", True)

        self.entry.delete(0, 'end')

    def Add_Commands(self, commanddict):
        self.commands.update(commanddict)

class StatusLED(tk.Frame):
    def __init__(self, root, text=None):
        tk.Frame.__init__(self, root.frame)
        self.text = text
        BASEDIR = os.path.dirname(os.path.abspath(__file__))
        self.red = tk.PhotoImage(file=BASEDIR + "/assets/greenled.PNG").subsample(7, 7) 
        self.green = tk.PhotoImage(file=BASEDIR + "/assets/redled.PNG").subsample(7, 7) 

        self.LEDlabel = tk.Label(self, image=self.red)
        

        self.state = False

        if self.text != None:
            self.textlabel = tk.Label(self, text=text)
            self.textlabel.grid(row=0, column=0)
            self.LEDlabel.grid(row=0, column=1)
        else:
            self.LEDlabel.pack()
            

    def Toggle_State(self):
        self.state = not self.state

        self.Update_label()

    def Set_State(self, state):

        if state == True or state == False:
            self.state = state

        else:
            raise TypeError("State must be True or False")
        
        self.Update_label()
    
    def Update_label(self):
        if self.state == True:
            self.LEDlabel.config(image=self.green)
        elif self.state == False:
            self.LEDlabel.config(image=self.red)

        else:
            raise TypeError("State must be a boolean")

    def Get_State(self):
        return self.state

class TkLivePlot(tk.Frame):
    def __init__(self, root, interval=1000, blit=False, maxpoints=50):
        tk.Frame.__init__(self, root)
        self.x = []
        self.y = []
        self.z = []
        self.maxpoints = maxpoints
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(plt.gcf(), master=root)
        self.ani = FuncAnimation(plt.gcf(), self.Animation, interval=interval, blit=blit)

    def grid(self,**kwargs):
        self.canvas.get_tk_widget().grid(kwargs)
    
    def pack(self,**kwargs):
        self.canvas.get_tk_widget().pack(kwargs)

    def Animation(self, i):
        self.ax.cla()
        self.ax.plot(self.x, self.y)

    def Update(self): 
        if len(self.x) >= self.maxpoints + 1:
            self.x = self.x[1:self.maxpoints + 1]

        if len(self.y) >= self.maxpoints + 1:
            self.y = self.y[1:self.maxpoints + 1]


    def UpdatePlot(self, x=[], y=[], z=[]):
        self.x = x
        self.y = y
        self.z = z
        self.Update()

    def Appendy(self, value):
        self.y.append(value)
        self.Increment("x")

        self.Update()

    def Increment(self, variable):
        if variable == "x":
            if len(self.x) > 0:
                self.x.append(self.x[-1]+1)
            else:
                self.x.append(1)
        
        if variable == "y":
            if len(self.y) > 0:
                self.y.append(self.y[-1]+1)
            else:
                self.y.append(1)
        

        if variable == "z":
            pass


class TkTable(tk.LabelFrame):
    def __init__(self, master, dataframe, text=None):
        super().__init__(master, text=text)
        self.name = text
        self.dataframe = dataframe
        self.columns = ["Index", *list(dataframe.columns)]

        self.treeview = ttk.Treeview(self, selectmode ='browse',columns=self.columns, show='headings')
        self.treeview.grid(row=0,column=0)
        
        self.horizontalscrollbar = tk.Scrollbar(self)
        self.verticalscrollbar = tk.Scrollbar(self)
        
        self.horizontalscrollbar.config(orient=tk.HORIZONTAL, command=self.treeview.xview)
        self.verticalscrollbar.config(orient=tk.VERTICAL, command=self.treeview.yview)

        self.horizontalscrollbar.grid(row=1, column=0, sticky=tk.N+tk.E+tk.S+tk.W)
        self.verticalscrollbar.grid(row=0, column=1, sticky=tk.N+tk.E+tk.S+tk.W)
        
        self.bind('<Enter>', self._Boundscrollwheel)
        self.bind('<Leave>', self._UnBoundscrollwheel)
        self.treeview.bind('<Double Button-1>', self.EditCell)
        self.treeview.config(xscrollcommand=self.horizontalscrollbar.set)
        self.treeview.config(yscrollcommand=self.verticalscrollbar.set)
        self.Update()

        

    def Load_data(self, dataframe):
        self.dataframe = dataframe

    def Update(self):
        self.treeview.delete(*self.treeview.get_children())
        self.column_num = len(self.columns)
        self.rows_num = len(self.dataframe)

        for i in range(self.column_num):
            if i == 0:
                self.treeview.column(self.columns[i], anchor ='c', width=50)
            else:
                self.treeview.column(self.columns[i], anchor ='c', width=150)
            self.treeview.heading(self.columns[i], text =self.columns[i], command=self.test)

        for index, row in self.dataframe.iterrows():
            self.treeview.insert('', tk.END, values=[index, *list(row.values)])
    def test(self):
        print("test")
    def _Boundscrollwheel(self, event):
        self.treeview.bind_all("<MouseWheel>", self._Onscrollwheel)

    def _UnBoundscrollwheel(self, event):
        self.treeview.unbind_all("<MouseWheel>")

    def _Onscrollwheel(self, event):
        self.treeview.yview_scroll(int(-1*(event.delta/120)), "units")

    def EditCell(self, event):
        col = self.columns[int(self.treeview.identify_column(event.x).replace("#", ""))-1]
        row = self.treeview.index(self.treeview.focus())

        entry_cord = self.treeview.bbox(self.treeview.focus(), column=self.treeview.identify_column(event.x))

        var = tk.StringVar()
        E = tk.Entry(self, textvariable=var)
        E.focus_set()
        
        E.select_range(0, 'end')
        var.set(self.dataframe[col][row])
        E.select_range(0, 'end')
        E.icursor('end')
        if entry_cord == None or len(entry_cord) < 4: # Domme bug met .focus method
            pass
        else:
            E.place(x=entry_cord[0], y=entry_cord[1], width=entry_cord[2], height=entry_cord[3])
            E.bind('<FocusOut>', lambda x: self.DestroyCell(E, col, row, var))
            E.bind("<Return>", lambda x: self.DestroyCell(E, col, row, var))
            E.wait_window()
        
    
    def DestroyCell(self, E, col , row, var):
        E.destroy()
        self.dataframe[col][row] = var.get()
        self.Update()