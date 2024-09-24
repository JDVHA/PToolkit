# Configure some important things
import sys, os, logging
BASEDIR = os.path.dirname(os.path.abspath(__file__))
APPNAME = "example"

from PToolkit.LabControl import MainPToolkitApp, PTOOLKITLOGGER

# Configuring the logger 
PTOOLKITLOGGER.setLevel(logging.INFO)

# Loading the interfaces folder
sys.path.append(BASEDIR + "\\interfaces")

# Your application
# ------------------------------------------------------------------------------------------------
from blankinterface import blankinterface
        
root = MainPToolkitApp(APPNAME)

blankinterface(root, "BlankInterface").pack()

if __name__ == "__main__":
    root.mainloop()
