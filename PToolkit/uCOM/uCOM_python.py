class uCOM:
    """
    Class to setup a pi pico or esp as a usb device
    """
    def __init__(self, messages=True):
        """
        Init the class
        """
        self.commands = {}
        self.msg = messages
    
    def Start(self):
        """
        Method to start the USB device
        """
        
        # Check if the starting msg needs to be displayed
        if self.msg:
            print("Starting....")
        
        # Start the mainloop
        while True:
            
            # Wait for a command
            command_raw = input("Command: ")
            
            # Determine the dash and space count
            dash_count = command_raw.count("|")
            space_count = command_raw.count(" ")
            
            # Check if the command contains the neseccery amount of |
            if  dash_count == 3:

                # Check if the command contains any spaces
                if  space_count == 0:

                    # Split the command based on |
                    s = command_raw.split("|")

                    # Remove the last index
                    s.pop(-1)

                    # Split the command in the actual command the data en datatypes
                    command = s[0]
                    data = s[1].split(",")
                    datatype = s[2].split(",")

                    print(command, data, datatype)

                    # Check if the length of the datatype and data is the same
                    if len(data) == len(datatype):

                        # Convert the data to the corresponding data type
                        for i in range(0, len(data)):
                            
                            if datatype[i] == "str":
                                pass

                            elif datatype[i] == "int":
                                data[i] = int(data[i])

                            elif datatype[i] == "float":
                                data[i] == float(data[i])

                            else:
                                raise NameError(f"'{datatype[i]}' is not a supported datatype")
                    else:
                        raise IndexError(f"Data list length {len(data)} is not the same as datatype length {len(datatype)}")
                else:
                    raise NameError(f"You can not use spaces in commands")
            
            # Check if dashcount is 0
            elif dash_count == 0:
                command = command_raw
            
            else:
                raise SyntaxError(f"Unclosed '|' in command")
            
            # Check if the command is in the command list
            try:
                c = self.commands[command]
                
            except KeyError:
                # if key error print that command is not found 
                if self.msg:
                   print(f"{command} is a unkown command")
            
            # Check if c is not none and parameters are given
            if c and dash_count !=0:
                # Excute the command function
                c(*data)
                
            # If c is not none and no parameters are given
            elif c and dash_count == 0:
                c()
                
                
    
    def Add_command(self, command, **options):
        """
        Method to add a command to the usb device (method is a decorator)
        Example:
        
        D = USB_Device()
        
        D.Add_command("t")
        def test():
            print("test")
            
        if command takes arguments use the following syntax: command|value1,value2,value3|int,str,float| example:
        
        D = USB_Device()
        
        D.Add_command("t")
        def test(a, b):
            print(a, b)
        
        When entering: t|123,123|str,int| it will print: 123, 123
        """
        def wrapper(func):
            # Add the command to a dict as a key and the function as its value
            self.commands[command] = func
            
            return func
        
        return wrapper

# Example
"""
D = uCOM()

@D.Add_command("t")
def test(a, b):
    print(a, b)

D.Start()
"""

# Input: t|123,123|str,int| prints 123, 123








