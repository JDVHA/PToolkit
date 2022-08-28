# PToolkit
 
# Description
A set of tools than is usefull in lots of diffrent fields. This toolkit contains functions to make professional looking matplotlib plot without spending time on the looks of the plot. Not only that this toolkit also provides functions for rounding and determining errors.


# Documentation
### The main class for in PToolkit is the Plotter class. The Plotter class contains all the methods to config the mpl plot. Currently the methods available in the plotter are:

<br>

- Decimal_format_axis(ax, decimalx=1, decimaly=1, decimalz=None, imaginary_axis="")

    Config the axis based on a decimal number 

    Paramters:

    - ax: mpl axis object
    - decimalx (int): The amount of decimal places each x tick should display
    - decimaly (int): The amount of decimal places each y tick should display
    - deciamlz (int): The amount of decimal places each z tick should display
    - imaginary_axis (str): The axis that should be imaginary_axis

<br>

- Set_xlabel(ax, physical_quantity, unit, tenpower=0)

    Set the physical quantity, unit and the the scientific notation for the x-label

    Paramters:
    - ax: mpls axis object 
    - physical_quantity (str): The pysical quantity on the axis
    - unit (str): The unit of the pysical quantity
    - tenpower (int): The power in the scientific notation

<br>

- Set_ylabel(ax, physical_quantity, unit, tenpower=0)

    Set the physical quantity, unit and the the scientific notation for the y-label

    Paramters:
    - ax: mpls axis object 
    - physical_quantity (str): The pysical quantity on the axis
    - unit (str): The unit of the pysical quantity
    - tenpower (int): The power in the scientific notation

<br>

- Set_zlabel(ax, physical_quantity, unit, tenpower=0)

    Set the physical quantity, unit and the the scientific notation for the z-label

    Paramters:
    - ax: mpls axis object 
    - physical_quantity (str): The pysical quantity on the axis
    - unit (str): The unit of the pysical quantity
    - tenpower (int): The power in the scientific notation

<br>

### There are a few other functions in PToolkit:
<br>

- Error_function(function, variables)

    Function to determine the error of a function based on the errors of the
    variables of set function.

    Paramters:
    - function (sympy.core.add.Add):  A sympy expression of which the error function should be determined
    - variables (list): A list of all the variables used in the expression

<br>

- Find_nearest(array, value)

    Find the nearest variable in a list based on a input value

    Paramters:
    - array (np.darray): A numpy array in which to search
    - value: The value to find in the array

<br>

- Round_sigfig(x, fig, type_rounding="Normal", format="numerical")

    Function to round a number (or array) to n significant digits

    Paramters:
    - x (float): a number that needs to be rounded 
    - fig (int): the number of significant digits
    - type (str): the type of rounding
        - "Normal": rounds to the closest number
        - "Up": rounds up
        - "Down": rounds down
    - format (str): the data type it should return (**only use numerical !!**)



# Example 1
Lets say we measured the resistance as function of temperature. We can use the plotter class to style and config our plot:
```
import matplotlib.pyplot as plt
import numpy as np
from PToolkit import Plotter

P = Plotter()

fig, ax = plt.subplots()

P.Decimal_format_axis(ax)

x = np.linspace(0, 10, 10)
y = np.linspace(0, 10, 10)

P.Set_xlabel(ax, "T", "$\degree$")
P.Set_ylabel(ax, "R", "$\Omega$")

plt.errorbar(x, y, xerr=0.2, yerr=1)
plt.show()
```

The Result of the code above:

[image]: _Figures/Figure1.png
![image] 

# Example 2
Lets say we want to round a array of numbers we can use the Round_sigfig function:

```
from PToolkit import Round_sigfig
to_round = np.array([1.52, 163, 1.7776, 1.98, 1090.897481242155221, 20.6])
sigfig = 2
rounded = Round_sigfig(to_round, sigfig)

print(rounded)
```
The result:
[1.5, 160.0, 1.8, 2.0, 1100.0, 21.0]

# Example 3
Lets say we want to know the error in the voltage function. We knwo the that by Ohms law the voltage over a resistance is equal to:

$V = IR$

So we can use the Error_function:
```
from PToolkit import Error_function
import sympy as sy

I, R = sy.symbols("I, R")
V = I*R

error = Error_function(V, [I, R])
```
$\Delta V = \sqrt{\left|{I}\right|^{2} \left|{\Delta R}\right|^{2} + \left|{R}\right|^{2} \left|{\Delta I}\right|^{2}}$


Ofcourse this is a simpel example but it also works on complex functions.

# Roadmap
PToolkit has three main goals:
- Reduce the time it takes to style plots
- Reduce the time writing latex
- Create general purpose functions used in the field of science and engineering


1. Vector field plot style
2. Polar plot style
3. Boxplot style
4. Custom colour map
5. Custom dataframe (pandas) to latex converter

# Install
```
pip install PToolkit
```