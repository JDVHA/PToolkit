import tkinter as tk
import logging, time, os, sys, threading
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from tkinter import ttk
from serial.tools.list_ports import comports

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)
PTOOLKITLOGGER = logging.getLogger()
PTOOLKITLOGGER.setLevel(logging.DEBUG)


INIT_FASE = True


class MainPToolkitApp(tk.Tk):
    def __init__(self, appname, *kwargs, **args):
        tk.Tk.__init__(self, *kwargs, **args)
        self.name = appname
        self.interfaces = []
        self.interfacenames = []

        self.protocol("WM_DELETE_WINDOW", self.StopApp)

    def mainloop(self):
        self.StartApp()
        self.tk.mainloop()
    
    def StartApp(self):
        global INIT_FASE
        if not INIT_FASE:
            raise SystemError("""INIT_FASE was false. Possible causes: INIT_FASE was changed in the program by the user. Or a second App was created, a maximum of 1 App may exist per program.""")
        INIT_FASE = False

        PTOOLKITLOGGER.info(f"Just started the main application.")

    def StopApp(self):
        if tk.messagebox.askokcancel("Quit", f"Do you want to quit {self.name}?"):
            for interface in self.interfaces:
                interface.Stop()
                del interface
            self.destroy()

    def AppendInterface(self, interface):
        if interface.name in self.interfacenames:
            raise NameError(f"Interface with name: {interface.name} already exists.")
        else:
            self.interfacenames.append(interface.name)
            self.interfaces.append(interface)
       

class Interface:
    def __init__(self, master, name):
        self.classname = self.__class__.__name__
        self.name = name
        self.master = master
        self.commands = {}
        self.keys = {}
        self.utilfuncs = ["RegisterCommand", "RegisterKey", "grid", "pack", "Post_init"]
        self.frame = tk.LabelFrame(self.master, text=name)
        PTOOLKITLOGGER.debug(f"Just created an instance of {self.classname}.")
        PTOOLKITLOGGER.debug(f"Starting post init of an {self.classname} instance.")

        self.master.AppendInterface(self)

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

    def Stop(self):
        for child in self.frame.winfo_children():
            if issubclass(type(child), Parameter) == True:
                child.Save()




class Parameter:
    def __init__(self, source, name=None, save=False):
        self.source = source
        self.save= save
        self.name = name

    def Load(self):
        if self.save == True and self.name !=None:
            path = sys.path[0]

            try:
                with open(path+"\\.state", "r") as f:
                    data = f.readlines()

            except FileNotFoundError as e:
                raise FileNotFoundError("Cannot find .state file")

            if len(data) > 0:
                for line in data:
                    if "=" in line:
                        linename, value = line.rstrip().split("=")
                        if  linename == self.name:
                            return value
                    else:
                        raise IOError("Corrupt state file. Remove state file")
                        
            else:
                return None

            

    def Save(self):
        if self.save == True and self.name != None:   
            path = sys.path[0]

            try:
                with open(path+"\\.state", "r") as f:
                    data = f.readlines()
            except FileNotFoundError as e:
                raise FileNotFoundError("Cannot find .state file")

            n = 0
            if len(data) > 0:
                
                for line in data:
                    
                    if line.split("=")[0] == self.name:
                        
                        data[n] = f"{self.name}={self.source()}\n"
                        
                        with open(path+"\\.state", "w") as f:
                            f.writelines(data)

                        # Fixes bug
                        break

                    else:
                        with open(path+"\\.state", "a") as f:
                            f.write(f"{self.name}={self.source()}\n")

                    n += 1            
            else:
                with open(path+"\\.state", "a") as f:
                    f.write(f"{self.name}={self.source()}\n")
                    
            

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
    

class VerticalAllign(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root.frame)
        self.frame = root.frame
        self.name = root.name

        self.widget_grid = []
    

    def Make_Grid(self):
        m, n = 0, 0
        for row in self.widget_grid:

            for widget in row:
                widget.grid(row=m, column=n, sticky='nesw')
                n += 1

            n = 0
            m += 1


    def pack(self, *args, **kwargs):
        self.Make_Grid()
        super(tk.Frame, self).pack(*args, **kwargs)

    def grid(self, *args, **kwargs):
        self.Make_Grid()
        super(tk.Frame, self).grid(*args, **kwargs)

class PToolkitWidgetBase:
    def __init__(self, master, content):
        
        if isinstance(master, VerticalAllign):
            widgets = content
        
        else:
            pass


    def __new___(cls, *args, **kwargs):
        pass
        

class KeyBoard(tk.Frame):
    def __init__(self, root, grid, textgrid=None, commandgrid=None, imagegrid=None):    
        tk.Frame.__init__(self, root.frame)

        if isinstance(root, VerticalAllign):
            master = root
        
        else:
            master = self

        if isinstance(root, VerticalAllign):
            widgets = [
            ]
            master.widget_grid.append(widgets)

        else:
            pass

        self.widgets = []
        m = len(grid)
        n = len(grid[0])

        
        unique_id = []
        for j in range(m):
            for i in range(n):
                row = []
                id = grid[j][i]
                
                if id == 0:
                    row.append(None)        

                elif id > 0:
                    if not id in unique_id:
                        unique_id.append(id)
                    
                    try:
                        text = textgrid[j][i]
                    except:
                        text = None

                    try:
                        command = commandgrid[j][i]
                    except:
                        command = None

                    try:
                        image = imagegrid[j][i]
                    except:
                        image = None
                    
                    button = tk.Button(
                            self,
                            text=text,
                            command=command,
                            image=image
                        )
                    
                    # Fixes a bug
                    button.image = image

                    row.append(button)
                    button.grid(row=j, column=i, sticky="nesw")

class ArrowKeyPad(KeyBoard):
    def __init__(self, root, commandgrid=None, size=(4, 4), includehome=False, buttons=4):
        
        BASEDIR = os.path.dirname(os.path.abspath(__file__))

        ICONSIZE = size

        if includehome == True:
            home = 1

        else:
            home = 0

        textgrid = [
                [None, None, None],
                [None, "Home", None],
                [None, None, None]
            ]

        if buttons == 4:
            grid = [
                [0, 1, 0],
                [1, home, 1],
                [0, 1, 0]
            ]
        elif buttons == 8:
            grid = [
                [1, 1, 1],
                [1, home, 1],
                [1, 1, 1]
            ]

        upkey = tk.PhotoImage(file=BASEDIR + "\\assets\\toparrow.png").subsample(*ICONSIZE) 
        downkey = tk.PhotoImage(file=BASEDIR + "\\assets\\downarrow.png").subsample(*ICONSIZE) 
        rightkey = tk.PhotoImage(file=BASEDIR + "\\assets\\rightarrow.png").subsample(*ICONSIZE) 
        leftkey = tk.PhotoImage(file=BASEDIR + "\\assets\\leftarrow.png").subsample(*ICONSIZE) 

        toprightkey = tk.PhotoImage(file=BASEDIR + "\\assets\\toprightarrow.png").subsample(*ICONSIZE) 
        topleftkey = tk.PhotoImage(file=BASEDIR + "\\assets\\topleftarrow.png").subsample(*ICONSIZE) 
        downrightkey = tk.PhotoImage(file=BASEDIR + "\\assets\\downrightarrow.png").subsample(*ICONSIZE) 
        downleftkey = tk.PhotoImage(file=BASEDIR + "\\assets\\downleftarrow.png").subsample(*ICONSIZE) 


        imagegrid = [
            [topleftkey, upkey, toprightkey],
            [leftkey, None, rightkey],
            [downleftkey, downkey, downrightkey]
        ]

        print(upkey)
        KeyBoard.__init__(self, root, grid, imagegrid=imagegrid, textgrid=textgrid)


        
        

    


class Button(tk.Button):
    def __init__(self, root, *args, **kwargs):
               

        if isinstance(root, VerticalAllign):
            master = root
            self.Button = tk.Button(master, *args, **kwargs)
            widgets = [
                self.Button
            ]
            master.widget_grid.append(widgets)

        else:
            tk.Button.__init__(self, root, *args, **kwargs) 
        
        



class Display(tk.Frame, Parameter):
    def __init__(self, root, text="", unit="-", font=2):
        tk.Frame.__init__(self, root.frame)

        if isinstance(root, VerticalAllign):
            master = root
        
        else:
            master = self


        self.unit = unit
        self.text = text 

        self.textvariable = tk.StringVar()

        self.textlabel = tk.Label(master, text=self.text, font=font, anchor="w")
        self.displaylabel = tk.Label(master, textvariable=self.textvariable, font=font)
        self.unitlabel = tk.Label(master, text=self.unit, font=font)
        if isinstance(root, VerticalAllign):
            widgets = [
                self.textlabel,
                self.displaylabel,
                self.unitlabel
            ]
            master.widget_grid.append(widgets)

        else:
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
    def __init__(self, root, text="", unit="-", font=2, save=True, from_=-999, to=999, increment=0.1):
        tk.Frame.__init__(self, root.frame)
        if isinstance(root, VerticalAllign):
            master = root
        
        else:
            master = self
        
        self.variable = tk.StringVar()

        self.unit = unit
        self.text = text 
        
        self.textLabel = tk.Label(master, text=self.text, font=font, anchor="w")
        self.spinBox = tk.Spinbox(master, font=font, from_=from_, to=to, textvariable=self.variable, increment=0.1)
        self.unitlabel = tk.Label(master, text=self.unit, font=font)

        parametername = f"{root.name}:{text}[{unit}]"
        Parameter.__init__(self, self.get, name=parametername, save=True)

        parametervalue = self.Load()

        if parametervalue:
            self.variable.set(parametervalue)
        
        else:
            self.variable.set("0")


        if isinstance(root, VerticalAllign):
            widgets = [
                self.textLabel,
                self.spinBox,
                self.unitlabel
            ]
            master.widget_grid.append(widgets)

        else:
            self.textLabel.grid(row=0, column=0, sticky='nesw')
            self.spinBox.grid(row=0, column=1, sticky='nesw')
            self.unitlabel.grid(row=0, column=2, sticky='nesw')
    

    def get(self):
        return self.spinBox.get()
    
class SerialPortSelector(tk.Frame):
    
    def __init__(self, root, serial, text="Serial devices: ", terminal=None):
        tk.Frame.__init__(self, root.frame)
        if isinstance(root, VerticalAllign):
            master = root
        
        else:
            master = self
        
        self.serial = serial
        self.terminal = terminal
        self.lastselect = None

        self.label = tk.Label(master, text=text, anchor="w")
        self.combobox = ttk.Combobox(master)
        self.combobox.bind("<<ComboboxSelected>>", self.Set_port)
        self.button = tk.Button(master, text="\u27F3", command=self.Get_serial_devices)
        
        if isinstance(root, VerticalAllign):
            widgets = [
                self.label,
                self.combobox,
                self.button
            ]
            master.widget_grid.append(widgets)
        else:
            self.label.grid(row=0, column=0)
            self.combobox.grid(row=0, column=1)
            self.button.grid(row=0, column=2)

        if self.terminal != None:
            self.terminal.Add_Commands({"reloadserial": self.Get_serial_devices})
        self.Get_serial_devices()

    def Set_port(self, e):
        device = self.combobox.current()
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

        self.combobox['values'] = list(self.devices.keys())

    
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
        self.terminal.see("end")
    
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
        
        self.red = tk.PhotoImage(file=BASEDIR + "\\assets\\greenled.PNG", master=self).subsample(7, 7) 
        self.green = tk.PhotoImage(file=BASEDIR + "\\assets\\redled.PNG", master=self).subsample(7, 7) 

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

class Plot(tk.Frame):
    def __init__(self, root, interval=100, blit=False, maxpoints=50):
        tk.Frame.__init__(self, root)
        self.x = []
        self.y = []
        self.z = []
        self.maxpoints = maxpoints
        self.figure = Figure(dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master=root)
        self.plot = self.ax.plot(self.x, self.y)[0]
        self.ani = FuncAnimation(self.figure, self.Animation, interval=interval, blit=blit)
        

    def set_xlabel(self, *args, **kwargs):
        self.ax.set_xlabel(*args, **kwargs)

    def set_ylabel(self, *args, **kwargs):
        self.ax.set_ylabel(*args, **kwargs)
       
    def grid(self,**kwargs):
        self.canvas.get_tk_widget().grid(kwargs)
    
    def pack(self,**kwargs):
        self.canvas.get_tk_widget().pack(kwargs)

    def Animation(self, i):
        for artist in plt.gca().lines + plt.gca().collections:
            artist.remove()
        self.ax.plot(self.x, self.y, c="b")

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

class BaseThread(threading.Thread):
    """
    Base class for the producer-consumer threads. 
    """
    def __init__(self, name, queue, interval=1):
        """
        Initialization of the BaseThread class

        Parameters
        ----------
        queue: queue.Queue
        The queue to get and store data 

        interval: int
        Interval between operations in seconds

        Returns
        -------
        None
        """
        
        # Init base class
        threading.Thread.__init__(self)

        # Store queue and interval in object
        self.interval = interval
        self.queue = queue

        # Create active and alive parameters
        self.active = False
        self.alive = True
        self.name = name

    def run(self):
        """
        Mainloop of the thread

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        # Start loop aslong as the thread is alive
        while self.alive:

            # Check if the thread is actively used
            if self.active == True:

                # Execute the inner thread
                self.Thread_inside()

                # Sleep if needed
                if self.interval != None:
                    time.sleep(self.interval)
                
                # Debug msg
                if PTOOLKITLOGGER.level == logging.DEBUG:
                    time.sleep(0.1)
                    PTOOLKITLOGGER.debug(f"Thread {self.name} is reading from a queue with current size: {self.queue.qsize()}.")
        
        # Debug msg   
        PTOOLKITLOGGER.debug(f"Killing thread: {self.name}")

        return

    def Thread_inside(self):
        """
        Inside of the thread method in BaseThread no use

        Parameters
        ----------
        None

        Returns
        -------
        None
        """


    def Start(self):
        """
        Method to start or restart the thread

        Parameters
        ----------
        None

        Returns
        -------
        None
        """

        PTOOLKITLOGGER.debug(f"Starting thread: {self.name}")
        # Set the thread active
        self.active = True

        # Try to start the thread from the orginal if already active skip
        try:
            super(BaseThread, self).start()
        except:
            pass

    def Stop(self):
        """
        Method to stop the thread

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        PTOOLKITLOGGER.debug(f"Stopping thread: {self.name}")
        self.active = False

    def Kill(self):
        """
        Method to kill the thread

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        self.alive = False

    def Toggle(self):
        """
        Method to toggle the thread

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        if self.active == True:
            self.Stop()

        elif self.active == False:
            self.Start()


    

class ProducerThread(BaseThread):
    """
    A class that allows for data generation or data acquisition
    """
    def __init__(self, name, generationfunction, queue, interval=1, terminal=None):
        """
        Initialization of the ProducerThread class

        Parameters
        ----------
        generationfunction: function
        A function that returns a peace of data to put into the queue

        queue: queue.Queue
        The queue to get and store data 

        interval: int
        Interval between operations in seconds

        terminal: PToolkit terminal object
        Termianl to print messages to

        Returns
        -------
        None
        """
        BaseThread.__init__(self, name, queue, interval)
        self.generationfunction = generationfunction
        self.terminal = terminal
        

    def Thread_inside(self):
        """
        Inside of the thread method. Executes the generationfunction and puts the
        result in the queue.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """

        # Check if queue is full
        if not self.queue.full():

            # Execute the generationfunction and add the data to the queue
            data = self.generationfunction()
            self.queue.put(data)    

        else:
            msg = f"Data overflow in queue, thread {self.name} cannot add more data. Data is currently being lost!!! Increase queue size or increase processing speed."
            if self.terminal != None:
                self.terminal.Terminal_msg(msg, True)    
            
            PTOOLKITLOGGER.warning(msg)
                
class ConsumerThread(BaseThread):
    """
    A class that allows for data processing from a queue
    """
    def __init__(self, name, consumerfunction, queue, interval=None, terminal=None):
        """
        Initialization of the ConsumerThread class

        Parameters
        ----------
        consumerfunction: function
        A function that returns consumes a piece of data from the queue
        and processes it.

        queue: queue.Queue
        The queue to get and store data 

        interval: int
        Interval between operations in seconds

        terminal: PToolkit terminal object
        Termianl to print messages to

        Returns
        -------
        None
        """
        BaseThread.__init__(self, name, queue, interval)
        self.consumerfunction = consumerfunction
        self.terminal = terminal
        

    def Thread_inside(self):
        """
        Inside of the thread method. Executes the generationfunction and puts the
        result in the queue

        Parameters
        ----------
        None

        Returns
        -------
        None
        """

        # Check if queue is empty
        if not self.queue.empty():

            # Get data from the queue and process it
            data = self.queue.get()
            self.consumerfunction(data)
