# Configure some important things
import sys, os, logging, datetime
BASEDIR = os.path.dirname(os.path.abspath(__file__))
APPNAME = "example"

from PToolkit.LabControl import MainPToolkitApp, PTOOLKITLOGGER

# Configuring the logger 
LOGFILENAME = BASEDIR + f"\\log\\{APPNAME}{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.log"
PTOOLKITLOGGER.setLevel(logging.INFO)
PTOOLKITLOGGER.addHandler(logging.FileHandler(LOGFILENAME))

# Loading the interfaces folder
sys.path.append(BASEDIR + "\\interfaces")

# Your application
# ------------------------------------------------------------------------------------------------
from blankinterface import blankinterface
        
root = MainPToolkitApp(APPNAME)

blankinterface(root, "BlankInterface").pack()

if __name__ == "__main__":
    root.mainloop()
