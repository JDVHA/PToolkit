# Configure some important things
import sys, os, logging
BASEDIR = os.path.dirname(os.path.abspath(__file__))

# Remove---------------
sys.path.append(os.path.dirname(BASEDIR))

from LabControl import MainPToolkitApp, PTOOLKITLOGGER

# Configuring the logger
PTOOLKITLOGGER.setLevel(logging.INFO)

# Loading the interfaces
sys.path.append(BASEDIR + "\\interfaces")

# Your application
# ------------------------------------------------------------------------------------------------
from Arduino import Arduino

APPNAME = "example"
        
root = MainPToolkitApp(APPNAME)

A = Arduino(root, "Arduino1")
A.pack()

if __name__ == "__main__":
    root.mainloop()
