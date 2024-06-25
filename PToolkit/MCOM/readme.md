# Introduction
MCOM is a micropython library that makes serial communication between the PC and microcontroller extremly easy. The library adds a class which handles the serial communication. The user only needs to create an commication object and add there desired command. 


# Command syntax
MCOM uses a command syntax make it possible to give parameters yout functions from the computer. A command without paramters is the command specefied on the microcontroller. For example given the following code on the microcontroller: 

```
from MCOM import MCOM

D = MCOM()

@D.Add_command("test")
def test():
    print("Hello world")

D.Start()
```

The command is "test" thus sending this over de serial bus will trigger the function. Lets say the function used requires for example a message that needs to be printed or a number that specefies how far a motor must travel than the command can be extended. This extension follows the following syntax:

<br>

command|value1,value2, ...|dtype1,dtype2, ...|

<br>

The command is the one specefied on the microcontroller just like when using no parameters. The value1 and value2 are the values you want to pass (not limited by 2). And dtype1 and dtype2 are the datatypes of there coresponding values. The datatypes supported in MCOM are:

1. String (str)
2. Interger (int)
3. Float (float)

For example given the following piece of code on the microcontroller:
```
from MCOM import MCOM

D = MCOM()

@D.Add_command("test")
def test(a,b):
    print(a,b)

D.Start()
```
When the following command is sent: "test|123,123|str,int|" the microcontroller wil print out: 123, 123 