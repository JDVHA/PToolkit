import sys, os
import shutil


class PToolkit():
    def __init__(self, terminalpath, args):
        self.terminalcommands = {}
        self.terminalpath = terminalpath
        self.arguments = args[1:]
        self.scriptpath = args[0].replace("\\terminal.py", "")

    def Add_command(self, command, **options):
            def wrapper(func):
                
                self.terminalcommands[command] = func
                
                return func
            
            return wrapper
    
    def Excute_command(self):
        command = self.arguments[0]
        
        try:
            self.terminalcommands[command](self.scriptpath, self.terminalpath, self.arguments[1:])
        
        except KeyError as e:
            print("ERROR: Unkown command")

console_path = os.getcwd()
arguments = sys.argv
P = PToolkit(console_path, arguments)

@P.Add_command("newproject")
def Create_new_project(scriptpath, terminalpath, arguments):
    try:
        shutil.copytree(scriptpath+"\\Labcontrol\\newproject", terminalpath+f"\\{arguments[0]}")
        print(f"SUCCES: Created project {arguments[0]}")

    except IndexError as e:
        print("ERROR: No project name was given")

    except Exception as e:
        print("ERROR: Folder already exists")

@P.Add_command("newinterface")
def Create_new_interface(scriptpath, terminalpath, arguments):
    name = arguments[0]
    try:
        shutil.copyfile(scriptpath+"\\Labcontrol\\newproject\\interfaces\\blankinterface.py", terminalpath+f"\\{name}.py")
        print(f"SUCCES: Created interface {arguments[0]}")

    except IndexError as e:
        print("ERROR: No interrface name was given")

    except Exception as e:
        print("ERROR: Interface already exists")



if __name__ == "__main__":
    P.Excute_command()


"""
command list:

newproject <project name>
newinterface <interface name>

"""