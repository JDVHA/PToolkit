import tkinter as tk
import logging, time, os, sys, threading
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import importlib
from tkinter import ttk
import datetime, math
import numpy as np
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

        self.interfaces = {}

        self.exitfunc = lambda: print("")
        self.protocol("WM_DELETE_WINDOW", self.stop_app)
        self.title(self.name)

        scriptpath = sys.path[0] + "\\scripts" + "\\"

        sys.path.append(scriptpath)

    def mainloop(self):
        self.start_app()
        self.tk.mainloop()
    
    def start_app(self):
        global INIT_FASE
        if not INIT_FASE:
            raise SystemError("""INIT_FASE was false. Possible causes: INIT_FASE was changed in the program by the user. Or a second App was created, a maximum of 1 App may exist per program.""")
        
        for interface in list(self.interfaces.values()):
            interface.__GUI__()
        
        INIT_FASE = False

        PTOOLKITLOGGER.info(f"Just started the main application.")

    def set_exit_func(self, func):
        self.exitfunc = func

    def stop_app(self):
        if tk.messagebox.askokcancel("Quit", f"Do you want to quit {self.name}?"):
            self.exitfunc()
            for interface in list(self.interfaces.values()):
                interface.stop()
                del interface
            PTOOLKITLOGGER.info(f"Stopping the main application.")
            self.destroy()
            sys.exit()


    def append_interface(self, interface):
        if interface.name in list(self.interfaces.keys()):
            raise NameError(f"Interface with name: {interface.name} already exists.")
        else:

            self.interfaces[interface.name] = interface

    def validate_project(self):
        project_path = ""

        if not os.path.isfile(project_path+"\\.state"):
            open(project_path+"\\.state")

        if not os.path.isdir(project_path+"\\scripts"):
            os.mkdir(project_path+"\\scripts")

        if not os.path.isdir(project_path+"\\profiles"):
            os.mkdir(project_path+"\\profiles")
        
        if not os.path.isdir(project_path+"\\log"):
            os.mkdir(project_path+"\\log")

        

       
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

        self.master.append_interface(self)

        PTOOLKITLOGGER.debug(f"Finished post init of an {self.classname} instance.")        
    
    def __GUI__(self):
        pass

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

    def stop(self):
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
        self.root = root
        self.frame = root.frame
        self.name = root.name

        self.widget_grid = []
    

    def Make_Grid(self):
        m, n = 0, 0
        for row in self.widget_grid:
            #print(row, "\n")
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

class PToolkitWidgetBase(tk.Frame):
    def __init__(self, root):
        self.x = False

        if isinstance(root, VerticalAllign):

            self.master = root

        else: 
            self.x = True
            try:
                tk.Frame.__init__(self, root.frame)
            except:
                tk.Frame.__init__(self, root)
            self.master = self
    
    def __SETWIDGETS__(self, content):
        self.widgets = content
        m, n = 0, 0

        if self.x == True:
            for row in self.widgets:

                for widget in row:

                    widget.grid(row=m, column=n)
                    n += 1
                n = 0
                m += 1
        
        else:
            for row in self.widgets:
                self.master.widget_grid.append(row)

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
    def __init__(self, root, commandgrid=None, size=(4, 4), includehome=False, design="*"):
        
        BASEDIR = os.path.dirname(os.path.abspath(__file__))

        ICONSIZE = size

        if includehome == True:
            home = 1

        else:
            home = 0

        if design == "+":
            grid = [
                [0, 1, 0],
                [1, home, 1],
                [0, 1, 0]
            ]
        elif design == "*":
            grid = [
                [1, 1, 1],
                [1, home, 1],
                [1, 1, 1]
            ]

        elif design == "<>":
            grid =[
                [0, 0, 0],
                [1, home, 1],
                [0, 0, 0]
            ]
        elif design == "v^":
            grid =[
                [0, 1, 0],
                [0, home, 0],
                [0, 1, 0]
            ]

        else:
            raise NameError(f"{design} is a unkown design type only: *, +, <> and v^ are available")


        upkey = tk.PhotoImage(file=BASEDIR + "\\assets\\toparrow.png").subsample(*ICONSIZE) 
        downkey = tk.PhotoImage(file=BASEDIR + "\\assets\\downarrow.png").subsample(*ICONSIZE) 
        rightkey = tk.PhotoImage(file=BASEDIR + "\\assets\\rightarrow.png").subsample(*ICONSIZE) 
        leftkey = tk.PhotoImage(file=BASEDIR + "\\assets\\leftarrow.png").subsample(*ICONSIZE) 

        toprightkey = tk.PhotoImage(file=BASEDIR + "\\assets\\toprightarrow.png").subsample(*ICONSIZE) 
        topleftkey = tk.PhotoImage(file=BASEDIR + "\\assets\\topleftarrow.png").subsample(*ICONSIZE) 
        downrightkey = tk.PhotoImage(file=BASEDIR + "\\assets\\downrightarrow.png").subsample(*ICONSIZE) 
        downleftkey = tk.PhotoImage(file=BASEDIR + "\\assets\\downleftarrow.png").subsample(*ICONSIZE) 
        homebutton = tk.PhotoImage(file=BASEDIR + "\\assets\\homebutton.png").subsample(*ICONSIZE)

        imagegrid = [
            [topleftkey, upkey, toprightkey],
            [leftkey, homebutton, rightkey],
            [downleftkey, downkey, downrightkey]
        ]

        KeyBoard.__init__(self, root, grid, imagegrid=imagegrid)
        
class Display(Parameter, PToolkitWidgetBase):
    def __init__(self, root, text="", unit="-", font=2):
        PToolkitWidgetBase.__init__(self, root)

        self.unit = unit
        self.text = text 

        self.textvariable = tk.StringVar()

        self.textlabel = tk.Label(self.master, text=self.text, font=font, anchor="w")
        self.displaylabel = tk.Label(self.master, textvariable=self.textvariable, font=font)
        self.unitlabel = tk.Label(self.master, text=self.unit, font=font)

        self.__SETWIDGETS__(
            [
                [self.textlabel, self.displaylabel, self.unitlabel]
            ]
        )

        self.textvariable.set("0")
        Parameter.__init__(self, self.get)

    def get(self):
        return self.textvariable.get()
    
    def update_display(self, value):
        if isinstance(value, ParameterField):
            value = value.get()
        self.textvariable.set(value)
        
class ParameterField(Parameter, PToolkitWidgetBase):
    def __init__(self, root, text="", unit="-", font=2, save=True, from_=-999, to=999, increment=0.1):
        PToolkitWidgetBase.__init__(self, root)
        
        self.variable = tk.StringVar()

        self.unit = unit
        self.text = text 
        
        self.textLabel = tk.Label(self.master, text=self.text, font=font, anchor="w")
        self.spinBox = tk.Spinbox(self.master, font=font, from_=from_, to=to, textvariable=self.variable, increment=0.1)
        self.unitlabel = tk.Label(self.master, text=self.unit, font=font)

        parametername = f"{root.name}:{text}[{unit}]"
        Parameter.__init__(self, self.get, name=parametername, save=True)

        parametervalue = self.Load()

        if parametervalue:
            self.variable.set(parametervalue)
        
        else:
            self.variable.set("0")


        self.__SETWIDGETS__(
            [
                [self.textLabel, self.spinBox, self.unitlabel]
            ]
        )
    

    def get(self):
        return self.spinBox.get()
    
class SerialPortSelector(PToolkitWidgetBase):
    
    def __init__(self, root, serial, text="Serial devices: ", terminal=None):
        PToolkitWidgetBase.__init__(self, root)
        
        self.serial = serial
        self.terminal = terminal
        self.lastselect = None

        self.label = tk.Label(self.master, text=text, anchor="w", font=2)
        self.combobox = ttk.Combobox(self.master)
        self.combobox.bind("<<ComboboxSelected>>", self.set_port)
        self.button = tk.Button(self.master, text="\u27F3", command=self.get_serial_devices)
        
        self.__SETWIDGETS__(
            [
                [self.label, self.combobox, self.button]
            ]
        )

        if self.terminal != None:
            self.terminal.add_command("reloadserial", self.get_serial_devices)
            
        self.get_serial_devices()

    def set_port(self, port=None):
        device = self.combobox.current()
        if type(port) != type(""):
            port = list(self.devices.values())[device]
        
        if self.lastselect == device:
            self.serial.close()
       
        self.serial.port = port
        self.serial.open()

              
        if self.terminal != None:

            device_name = list(self.devices.keys())[device]

            if self.serial.is_open and self.lastselect == device:
                self.terminal.terminal_msg(f"Serial connection with {device_name} is re established.")

            elif self.serial.is_open:
                self.terminal.terminal_msg(f"Serial connection with {device_name} is established.")

            else:
                self.terminal.terminal_msg(f"Serial connection with {device_name} has failed.", True)

            self.lastselect = device

    def get_serial_devices(self):
        """Scan for available devices"""
        available_ports = comports()
        self.devices = {}
        
        for port, device, _ in sorted(available_ports):
            self.devices[device] = port

        self.combobox['values'] = list(self.devices.keys())
  
class Terminal(tk.LabelFrame):
    def __init__(self, root, text=None, allowcommands=True, width=60, height=10):
        super().__init__(root.frame, text=text)
        self.commands = {
            "help": self.list_commands,
            "history": self.show_history,
            "clearhistory": self.clear_history,
            "clearterminal": self.clear_terminal,
            "clearall": self.clear_all,
        }

        self.commandhistory = [""]
        self.counter = 0

        self.progressbars = {}

        scrollbar = tk.Scrollbar(self)
        self.terminal = tk.Text(self, wrap="word", yscrollcommand=scrollbar.set, width=width, height=height)
        self.terminal.tag_config("ERROR", foreground="red")
        scrollbar.config(command=self.terminal.yview)
        
        self.terminal.grid(row=0, column=0)
        scrollbar.grid(row=0, column=1, sticky=tk.N+tk.S)
        self.terminal.config(state=tk.DISABLED)

        if allowcommands:
            self.entry = tk.Entry(self)
            self.entry.grid(row=1, column=0, sticky="NWSE")

            self.sendbutton = tk.Button(self, text="send", command=lambda: self.run_Command(self.entry.get()))
            self.sendbutton.grid(row=1, column=1)

            self.entry.bind('<Return>', self.entry_Run)
            self.entry.bind('<Up>', lambda x: self.prev_command(-1, x))
            self.entry.bind('<Down>', lambda x: self.prev_command(1, x))
    
    def prev_command(self, val, e):
        
        if -len(self.commandhistory) < self.counter+val <= 0:

            command = self.commandhistory[self.counter + val]
            self.entry.delete(0,tk.END)
            self.entry.insert(0,command)
            self.counter += val

    def show_history(self):
        """Prints the command history to the terminal"""

        self.terminal_msg("Command history: ")
        command_list = list(self.commands.keys())
        
        for command in self.commandhistory[1:]:

            if command in command_list:
                self.terminal_msg(f"\t\u2611{command}")   
            else:
                self.terminal_msg(f"\t\u2610{command}") 
    
    def clear_history(self):
        """Erase the command history"""

        self.terminal_msg("Erasing the command history...")
        self.counter = 0    
        self.commandhistory = [""]

    def clear_terminal(self):
        """Clears the terminal"""

        self.terminal.config(state=tk.NORMAL)
        self.terminal.delete("1.0", tk.END)
        self.terminal.config(state=tk.DISABLED)
        self.terminal.see("end")

    def clear_all(self):
        """Clear terminal and command history"""

        self.clear_history()
        self.clear_terminal()

    def terminal_msg(self, msg, error=False):
        if msg != None:
            self.terminal.config(state=tk.NORMAL)
            if error:
                self.terminal.insert(tk.END, f"ERROR: {msg}\n", "ERROR")
            else:
                self.terminal.insert(tk.END, f"{msg}\n")
            self.terminal.config(state=tk.DISABLED)
            self.terminal.see("end")
        
    def list_commands(self):
        """Lists all the commands available in terminal."""

        self.terminal_msg("Available commands:")
        for name, function in self.commands.items():  
            self.terminal_msg(f"\t-{name}: {function.__doc__}")

    def entry_Run(self, e):
        self.run_Command(self.entry.get())

    def run_Command(self, command):
        self.commandhistory.append(command)
        self.counter = 0

        self.terminal_msg(f"Input: {command}")

        # Decoder required
        try:
            self.commands[command]()
            
        except KeyError as e:
            self.terminal_msg("Unkown command", True)

        
        self.entry.delete(0, 'end')

    def add_command(self, name, function):
        self.commands[name] = function

    def add_progressbar(self, name, max):

        line = self.terminal.get("1.0", tk.END).count("\n")
        
        self.progressbars[name] = [line, 0, max, time.time()]

        self.update_progressbar(name, 0)

    def update_terminal_line(self, line, updatedtext):
        self.terminal.config(state=tk.NORMAL)

        self.terminal.delete(f"{line}.0", "1.999999999999")
        self.terminal.insert(f"{line}.0", updatedtext)

        self.terminal.config(state=tk.DISABLED)
        self.terminal.see("end")

    def delete_progressbar(self, name):
        del self.progressbars[name]


    def update_progressbar(self, name, amount=1):

        line, current, max, startime = self.progressbars[name]
        
        new_current = current + amount

        self.progressbars[name][1] = new_current

        iteration_time = np.round(time.time()-startime, 2)
        estimatedtime = np.round((max-new_current)*iteration_time,2)
        estimatedtime_str = str(datetime.timedelta(seconds=estimatedtime))
        self.progressbars[name][3] = time.time()

        percentage = new_current/max * 100

        hashtagcount = int(math.floor(percentage/10))
        dashcount = 10-hashtagcount


        new_line = f"{name}: [" + "#"*hashtagcount + "-"*dashcount + f"]{new_current}/{max} [{estimatedtime_str}, {iteration_time} s/it]"
        
        # Bug fix
        if amount == 0:
            new_line += "\n"
            

        if not new_current > max:

            self.update_terminal_line(line, new_line)

        else:
            self.terminal_msg("Process tries to update finished progressbar.", True)
    
class StatusLED(PToolkitWidgetBase):
    def __init__(self, root, text=None):
        PToolkitWidgetBase.__init__(self, root)

        self.text = text
        BASEDIR = os.path.dirname(os.path.abspath(__file__))
        
        self.red = tk.PhotoImage(file=BASEDIR + "\\assets\\greenled.PNG", master=self.master).subsample(7, 7) 
        self.green = tk.PhotoImage(file=BASEDIR + "\\assets\\redled.PNG", master=self.master).subsample(7, 7) 

        self.LEDlabel = tk.Label(self.master, image=self.red)
        self.state = False

        if self.text != None:
            self.textlabel = tk.Label(self.master, text=text)
            self.__SETWIDGETS__(
                [
                    [self.textlabel, self.LEDlabel]
                ]
            )
        else:
            self.__SETWIDGETS__(
                [
                    [self.LEDlabel]
                ]
            )
            

    def toggle_state(self):
        self.state = not self.state

        self.update_label()

    def set_state(self, state):

        if state == True or state == False:
            self.state = state

        else:
            raise TypeError("State must be True or False")
        
        self.update_label()
    
    def update_label(self):
        if self.state == True:
            self.LEDlabel.config(image=self.green)
        elif self.state == False:
            self.LEDlabel.config(image=self.red)

        else:
            raise TypeError("State must be a boolean")

    def get_state(self):
        return self.state

class Plot(tk.Frame):
    def __init__(self, root, interval=10, maxpoints=50, ylim=(0, 10), diplayfps=False):
        tk.Frame.__init__(self, root)
        blit=False
        self.x = []
        self.y = []
        self.maxpoints = maxpoints
        self.figure = plt.figure()
        self.ax = self.figure.add_subplot(111)
        self.FPS_DISPLAY = diplayfps
        
        self.line, = self.ax.plot([], lw=3)
        self.ax.set_ylim(*ylim)
        self.ax.set_xlim(0, self.maxpoints)
        self.text = self.ax.text(0, ylim[1]-0.5, "")
        self.figure.canvas.draw()
        self.t_start = time.time()
        self.axbackground = self.figure.canvas.copy_from_bbox(self.ax.bbox)
        
        self.canvas = FigureCanvasTkAgg(self.figure, master=root)
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
        # Improved animation speed achieved using following stackoverflow example:
        # https://stackoverflow.com/a/40139416
        self.update()
       
        self.line.set_data(self.x, self.y)
        
        if PTOOLKITLOGGER.level == logging.DEBUG or self.FPS_DISPLAY:
            fps = str(np.round((i+1) / (time.time() - self.t_start), 0)).replace(".0", "")
            tx = f' Figure frame rate: {fps} fps'
            self.text.set_text(tx)

        self.figure.canvas.restore_region(self.axbackground)

        self.ax.draw_artist(self.line)
        if PTOOLKITLOGGER.level == logging.DEBUG or self.FPS_DISPLAY:
            self.ax.draw_artist(self.text)

        self.figure.canvas.blit(self.ax.bbox)

        self.figure.canvas.flush_events()
        
        

    def update(self): 
        if len(self.x) >= self.maxpoints + 1:
            self.x = self.x[1:self.maxpoints + 1]

        if len(self.y) >= self.maxpoints + 1:
            self.y = self.y[1:self.maxpoints + 1]

    def update_plot(self, x=[], y=[]):
        self.x = x
        self.y = y
        
    def appendy(self, value):
        if len(self.y) >= self.maxpoints:
            self.y.pop(0)

        self.y.append(value)

        if len(self.x) > 0:
            if max(self.x) >= self.maxpoints:
                pass
            else:
                self.increment("x")
        else:
            self.increment("x")

        

    def increment(self, variable):
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

class BaseThread:
    """
    Base class for the producer-consumer threads. 
    """
    def __init__(self, name, queue, interval, terminal=None):
        # Init base class
        
        self.thread = None

        # Store queue and interval in object
        self.interval = interval
        self.queue = queue

        # Create active and alive parameters
        self.alive = False
        self.name = name

        self.terminal = terminal

        if self.terminal != None:
            self.terminal.add_command(f"onT {name}", self.start)
            self.terminal.add_command(f"offT {name}", self.stop)
            self.terminal.add_command(f"toggleT {name}", self.toggle)

    def run(self):
       
        # Start loop aslong as the thread is alive
        while self.alive:
            # Execute the inner thread
            self.thread_inside()
            # Sleep if needed
            if self.interval != None:
                time.sleep(self.interval)
            
            # Debug msg
            if PTOOLKITLOGGER.level == logging.DEBUG:
                time.sleep(0.5)
                PTOOLKITLOGGER.debug(f"Thread {self.name} is using a queue with current size: {self.queue.qsize()}.")

    def thread_inside(self):
       pass

    def start(self):
        f"""Start the thread"""
        self.thread = threading.Thread(target=self.run, daemon=True)

        PTOOLKITLOGGER.info(f"Starting thread: {self.name}")
        # Set the thread active
        self.alive = True
        if self.terminal != None and not INIT_FASE:
            self.terminal.terminal_msg(f"Starting thread: {self.name}")

        self.thread.start()


    def stop(self):
        """Stop the thread"""

        if self.terminal != None and not INIT_FASE:
            self.terminal.terminal_msg(f"Stopping thread: {self.name}")
        
        PTOOLKITLOGGER.info(f"Stopping thread: {self.name}")
        self.alive = False

    def toggle(self):
        """Toggle the thread"""
        if self.alive == True:
            self.Stop()

        elif self.alive == False:
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
        BaseThread.__init__(self, name, queue, interval, terminal)
        self.generationfunction = generationfunction
        

    def thread_inside(self):
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
                self.terminal.terminal_msg(msg, True) 
   
            
            PTOOLKITLOGGER.warning(msg)
                
class ConsumerThread(BaseThread):
    """
    A class that allows for data processing from a queue
    """
    def __init__(self, name, consumerfunction, queue, interval=1, terminal=None):
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
        BaseThread.__init__(self, name, queue, interval, terminal)
        self.consumerfunction = consumerfunction
        

    def thread_inside(self):
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

        else:
            time.sleep(self.interval)

class Digit:
    def __init__(self, canvas, offsetx, offsety, length=30, style="rectangle"):
        self.canvas = canvas
        self.segments = []
        offsets = (
            (0, 0, 1, 0),  # top
            (1, 0, 1, 1),  # upper right
            (1, 1, 1, 2),  # lower right
            (0, 2, 1, 2),  # bottom
            (0, 1, 0, 2),  # lower left
            (0, 0, 0, 1),  # upper left
            (0, 1, 1, 1),  # middle
        )

        total = 2*length

        a = length/20
        b = length-4*a
        c = 7

        disp = [
            ("h", 0, 0, c, 0),
            ("v", 1, 0, 1.1*c, c),
            ("v", 1, 1, 1.1*c, 2.1*c+a),
            ("h", 0, 2, c, 2.2*c+2*a),
            ("v", 0, 1, 0, 2*c+a),
            ("v", 0, 0, 0, c),
            ("h", 0, 1, c, 2*c),
        ]

        self.digits = {
            "0": (1, 1, 1, 1, 1, 1, 0),  # 0
            "1": (0, 1, 1, 0, 0, 0, 0),  # 1
            "2": (1, 1, 0, 1, 1, 0, 1),  # 2
            "3": (1, 1, 1, 1, 0, 0, 1),  # 3
            "4": (0, 1, 1, 0, 0, 1, 1),  # 4
            "5": (1, 0, 1, 1, 0, 1, 1),  # 5
            "6": (1, 0, 1, 1, 1, 1, 1),  # 6
            "7": (1, 1, 1, 0, 0, 0, 0),  # 7
            "8": (1, 1, 1, 1, 1, 1, 1),  # 8
            "9": (1, 1, 1, 1, 0, 1, 1),  # 9
            "-": (0, 0, 0, 0, 0, 0, 1),  # -
            " ": (0, 0, 0, 0, 0, 0, 0),  # Blanck
        }

        width = 3
        x = offsetx
        y = offsety

        baseoffset = 0
        
        if style == "rectangle":
            for x0, y0, x1, y1 in offsets:
                seg = self.canvas.create_line(
                        x + x0*length,
                        y + y0*length,
                        x + x1*length,
                        y + y1*length,
                    width=width, fill="gray")
            
                self.segments.append(seg)
            
            xc0 = x + length
            yc0 = y + 2*length-2*width
            xc1 = xc0 + int(length/5)
            yc1 = yc0 + int(length/5)

        elif style == "hexagon":
            for i in disp:

                mode = i[0]
                offsetx = baseoffset + i[1]*b+2*a + i[3] + x
                offsety = baseoffset + i[2]*b+2*a + i[4] + y

                points = self.get_points(a, b, offsetx, offsety, mode=mode)
                seg = self.canvas.create_polygon(points, fill="gray")
                self.segments.append(seg)

            xc0 = x + length + c
            yc0 = y + 2*length
            xc1 = xc0 + int(length/5)
            yc1 = yc0 + int(length/5)
        

        self.dot = self.canvas.create_oval(xc0, yc0, xc1, yc1, fill="black", width=0)
    
    def get_points(self, a, b, offsetx, offsety, mode):
        points_v = [
                offsetx+a, 0 + offsety,
                offsetx+2*a, a + offsety,
                offsetx+2*a, a+b + offsety,
                offsetx+a, 2*a+b + offsety,
                offsetx+0, a+b + offsety,
                offsetx+0, a + offsety,
            ]
        points_h = [
                offsetx, a+offsety,
                offsetx+a, 0+offsety,
                offsetx+b, 0+offsety,
                offsetx+b+a, a+offsety,
                offsetx+b, 2*a+offsety,
                offsetx+a, 2*a+offsety,
            ]
        if mode == "h":
            return points_h
        
        elif mode == "v":
            return points_v
        
    def update(self, char):

        binarysegments = self.digits[char]

        for iid, on in zip(self.segments, binarysegments):

            if on == True:
                color = "red"

            else:
                color = "gray"

            self.canvas.itemconfigure(iid, fill=color)
    
    def setdot(self, state):
        if state == True:
            color = "red"

        else:
            color = "black"
        self.canvas.itemconfigure(self.dot, fill=color)

class SevenSegmentDisplay(tk.Frame):
    def __init__(self, root, digits, negative_numbers=True, style="hexagon"):
        tk.Frame.__init__(self, root.frame)
        font=5
        self.length = 10*font
        self.width = font

        self.lastdot = 0
        
        self.digits = []
        self.negative_numbers = negative_numbers
        
        if negative_numbers == True:
            digits += 1

        spacing = 20
        f = 20

        # Bug
        if style == "hexagon":
            f += 10
        
        # After digits mod, prevents bug
        self.canvas = tk.Canvas(self, width=10+(self.length+spacing)*digits, height=2*self.length+f, bg="black")
        self.canvas.pack()

        for i in range(digits):
            self.digits.append(Digit(self.canvas, 10+(self.length+spacing)*i, 10, self.length, style=style))
        
        for i in self.digits:
            i.update(" ")

        

    def update_display(self, num):
        string = str(num)

        if num > 0 and self.negative_numbers == True:
            string = " " + string

        self.digits[self.lastdot].setdot(False)

        if "." in string:   
            
            pos = string.index(".")

            self.lastdot = pos-1

            string = string.replace(".", "")
            self.digits[self.lastdot].setdot(True)

        for i in range(len(self.digits)):

            if i < len(string):
                self.digits[i].update(string[i])
            
            else:
                self.digits[i].update(" ")
        
class ScriptLoader(PToolkitWidgetBase):

    def __init__(self, root, text="Script:", terminal=None, default="blank.py"):
        PToolkitWidgetBase.__init__(self, root)

        self.default = default
        self.root = root

        self.scripts = []
        self.terminal = terminal

        runscript_wrapper = lambda: self.run_script(self.scripts[self.combobox.current()].replace(".py", ""))
        runscript_wrapper.__doc__ =  """Run the currently selected script."""
        
        if self.terminal != None:
            self.terminal.add_command("reloadscripts", self.list_scripts)
            self.terminal.add_command("runscript", runscript_wrapper)
            self.terminal.add_command("reset", self.reset)

        self.label = tk.Label(self.master, text=text, font=2, anchor="w")
        self.combobox = ttk.Combobox(self.master)
        self.button = tk.Button(self.master, text="Run script", command=runscript_wrapper)
        self.__SETWIDGETS__(
                [
                    [self.label, self.combobox, self.button]
                ]
            )

        self.list_scripts()

        if default in self.scripts:
            self.combobox.set(default)

    def reset(self):
        """Reseting to default script"""

        if not INIT_FASE and self.terminal != None:
            self.terminal.terminal_msg(f"Reseting script to {self.default}")

        if self.default in self.scripts:
            self.combobox.set(self.default)

        elif not INIT_FASE and self.terminal != None:
            self.terminal.terminal_msg(f"No default script selected.")

    def list_scripts(self):
        """Reload script folder"""

        path = sys.path[0] + "\\scripts"


        if not INIT_FASE and self.terminal != None:
            n = 0
            for file in os.listdir(path):
                if file.endswith(".py"):
                    n+=1
            self.terminal.terminal_msg(f"Reloading scripts, found: {n}")

        self.scripts = []

        for file in os.listdir(path):
            if file.endswith(".py"):
                if not INIT_FASE and self.terminal != None:
                    script = importlib.import_module(file.replace(".py", ""))
                    mainfunc = getattr(script, "main")
                    description = mainfunc.__doc__

                    self.terminal.terminal_msg(f"\t- {file}: {description}")

                self.scripts.append(file)


        self.combobox['values'] = self.scripts

    def run_script(self, scriptname):
        """Run the currently selected script."""
        
        #scriptname = self.scripts[self.combobox.current()].replace(".py", "")

        try:
            script = importlib.import_module(scriptname)

            mainfunc = getattr(script, "main")
            
            try:
                interfaces = self.root.master.interfaces
            except: 

                try:
                    interfaces = self.root.root.master.interfaces
                except: 
                    PTOOLKITLOGGER.error(f"Cannot locate main app. Running script without interfaces")
                    if self.terminal != None:
                        self.terminal.terminal_msg(f"Cannot locate main app. Running script without interfaces.")
                    interfaces = {}

            PTOOLKITLOGGER.info(f"Running script: {scriptname}")

            if self.terminal != None:
                self.terminal.terminal_msg(f"Running script: {scriptname} ....")
                self.terminal.terminal_msg(f"##############################\n")
            self.button.config(state="disabled")
            mainfunc(interfaces)
            self.button.config(state="active")

            if self.terminal != None:
                self.terminal.terminal_msg(f"\n##############################")
                self.terminal.terminal_msg(f"Script: {scriptname} finished")

        except ModuleNotFoundError as e:
            if self.terminal != None:
                self.terminal.terminal_msg(f"No script called {scriptname} found in script folder.", True)
            
            PTOOLKITLOGGER.error(f"No script called {scriptname} found in script folder. " + str(e))
        
        except SyntaxError as e:
            if self.terminal != None:
                self.terminal.terminal_msg(f"Syntax error in script {scriptname}: {e}.", True)
            PTOOLKITLOGGER.error(f"Syntax error in script {scriptname}: {e}")

        except Exception as e:
            if self.terminal != None:
                self.terminal.terminal_msg(f"Error in script {scriptname}.", True)
            PTOOLKITLOGGER.error(f"Error in script {scriptname}." + str(e))

        self.button.config(state="active")

class Button(PToolkitWidgetBase):
    def __init__(self, root, text="", command=None):
        PToolkitWidgetBase.__init__(self, root)

        self.button = tk.Button(self.master, text=text, command=command)

        self.__SETWIDGETS__(
            [
                [self.button]
            ]
        )