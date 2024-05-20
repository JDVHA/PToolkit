import tkinter as tk
import logging
import threading

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
        self.interfaces = []

    def mainloop(self):
        self.StartApp()
        self.tk.mainloop()
    
    def StartApp(self):
        
        for interface in self.interfaces:
            interface.Post_init()
        
        global INIT_FASE
        if not INIT_FASE:
            raise SystemError("""INIT_FASE was false. Possible causes: INIT_FASE was changed in the program by the user. A second controll bus was created a maximum of 1 controlbus may exist per program. Another library uses the same variablename (can currently not be solved).""")
        INIT_FASE = False
        PTOOLKITLOGGER.info(f"Just started the main application.")

    def AppendInterface(self, interface):
        PTOOLKITLOGGER.debug(f"Just added an instance of {interface.__class__.__name__} to main.")
        self.interfaces.append(interface)
        
class Command:
    def __init__(self, profile, root):
        self.name = profile["name"]
        self.excutefunction = profile["command"]
        self.GUI_element = profile["gui_element"]
        self.GUI_link = profile["links"]
        self.root = root
        self.Pre_constructer()
        

    def Pre_constructer(self):
        if self.GUI_element == None:
            pass
        elif self.GUI_element == tk.Button:
            self.GUI_element = tk.Button(master=self.root, text=self.name, command=self.Excute_wrapper)

    def Excute_wrapper(self):
        results = [self.excutefunction()]
        for i in range(len(results)):
            try: 
                self.GUI_link[i](results[i])
            except Exception as ex:
                PTOOLKITLOGGER.warning(f"There is no link")
        return results


class Interface:
    def __init__(self, master, text=None):
        self.classname = self.__class__.__name__
        self.commands = {}
        self.keys = {}
        self.utilfuncs = ["RegisterCommand", "RegisterKey", "grid", "pack", "Post_init"]
        self.frame = tk.LabelFrame(master, text=text)
        PTOOLKITLOGGER.debug(f"Just created an instance of {self.classname}.")

    def Post_init(self):

        PTOOLKITLOGGER.debug(f"Starting post init of an {self.classname} instance.")

        for i in dir(self):
            if not (i.startswith("_") or i.endswith("_") or i in self.utilfuncs):
                if callable(getattr(self, i)):
                    profile = getattr(self, i)()
                    profile["command"] = getattr(self, i)
                    links = []
                    
                    for key in profile["links"]:
                        links.append(self.keys[key])
                    profile["links"] = links
                    self.commands[i] = Command(profile, self.frame)

        PTOOLKITLOGGER.debug(f"Finished post init of an {self.classname} instance.")
        
        self._Construct_GUI()


    def RegisterCommand(name, GUI_element=None, links=[]):
        
        def _Appenddict(function):
            
            def wrapper(*args):
                self = args[0]
                
                if INIT_FASE:
                    PTOOLKITLOGGER.debug(f"Registered {name} as a command for interface {self.classname}")
                    return  {
                    "name": name,
                    "command": function,
                    "gui_element": GUI_element,
                    "links": links
                    }

                else:
                    return function(*args)
            
            return wrapper
        return _Appenddict

    def RegisterKey(self, keyname, function):
        print(f"Registering key '{keyname}' in {self.classname}")
        PTOOLKITLOGGER.debug(f"Registered {keyname} as a key for interface {self.classname}")
        self.keys[keyname] = function


    def _Construct_GUI(self):
        PTOOLKITLOGGER.debug(f"Starting automatic GUI constructer for an instance of {self.classname}")
        
        for _, command in self.commands.items():
            if command.GUI_element == None:
                pass
            else:
                command.GUI_element.pack()

        PTOOLKITLOGGER.debug(f"Finished automatic GUI constructer for an instance of {self.classname}")

    def grid(self, *args, **kwargs):
        self.frame.grid(*args, **kwargs)

    def pack(self, *args, **kwargs):
        self.frame.pack(*args, **kwargs)
