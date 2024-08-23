# Configure some important things
import logging.handlers
import sys, os, logging, datetime
BASEDIR = os.path.dirname(os.path.abspath(__file__))
APPNAME = "example"

# Remove---------------
sys.path.append(os.path.dirname(BASEDIR))

from LabControl import MainPToolkitApp, PTOOLKITLOGGER

# Configuring the logger
logging.getLogger('matplotlib.font_manager').disabled = True
LOGFILENAME = BASEDIR + f"\\log\\{APPNAME}{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.log"
PTOOLKITLOGGER.setLevel(logging.INFO)
PTOOLKITLOGGER.addHandler(logging.FileHandler(LOGFILENAME))

# Loading the interfaces
sys.path.append(BASEDIR + "\\interfaces")

# Your application
# ------------------------------------------------------------------------------------------------
from Arduino import Arduino
from TTi_1604 import TTi_1604
        
root = MainPToolkitApp(APPNAME)

#A = Arduino(root, "Arduino1")
#A.grid(row=0, column=0)

B = TTi_1604(root, "TTi_1604")
B.grid(row=0, column=0)

if __name__ == "__main__":
    root.mainloop()
