from ast import Raise
import os
import matplotlib.ticker as mticker
import sympy as sy
import matplotlib as mpl
from math import floor, log10, ceil
from locale import setlocale, LC_NUMERIC
import numpy as np


class DecimalAxisFormatter(mticker.Formatter):
    """
    Decimal axis formatter used to format the ticks on the x, y, z axis of a matplotlib plot.
    """
    def __init__(self, decimaal, separator, imaginary=False):
        """Initialization of the formatter class"""
        self.decimaal = decimaal
        self.imaginary = imaginary
        self.separator = "{" + separator + "}"


    def __call__(self, x, pos=None):
        """
        Methode used to replace the seperator in a given tick

        input:
            x (float): a number that needs to have it seperator changed to the desired seperator
        
        return:
            a number with the desired seperator

        """

        # Define a string to perform operations on and round to the desired decimal place
        s = str(round(x, self.decimaal))

        # Replace the current seperator with the desired seperator
        tick = f"${s.replace('.', self.separator)}$"

        # Check if the axis is imaginary
        if self.imaginary:
            tick += "i"

        # Return tick
        return tick

class SignificantFigureAxisFormatter(mticker.Formatter):
    """
    Significant figure axis formatter used to format the ticks on the x, y, z axis of a matplotlib plot.
    """
    def __init__(self, significant_digit, separator, imaginary=False):
        """Initialization of the formatter class"""
        self.significant_digit = significant_digit
        self.imaginary = imaginary
        self.separator = "{" + separator + "}"


    def __call__(self, x, pos=None):
        """
        Methode used to replace the seperator in a given tick

        input:
            x (float): a number that needs to have it seperator changed to the desired seperator
        
        return:
            a number with the desired seperator

        """

        # Define a string to perform operations on and round to the desired significant figure digit
        s = str(Round_sigfig(x, self.significant_digit))

        # Replace the current seperator with the desired seperator
        tick = f"${s.replace('.', self.separator)}$"

        # Check if the axis is imaginary
        if self.imaginary:
            tick += "i"

        # Return tick
        return tick



def Error_function(function, variables):
    """
    Function to determine the error of a function based on the errors of the
    variables of set function.
    
    input:
        function (sympy.core.add.Add): a sympy expression of which the error function should be determined
        variables (list): a list of all the variables used in the expression

    return:
        a error function of the given input function

    """
    # Define the total diffrential variable
    total_diffrential = 0

    # Loop through every variable and determine its partial derivative and sum it to the total diffrential variabl
    for variable in variables:
        total_diffrential += sy.Abs(sy.diff(function, variable))**2 * sy.Abs(sy.Symbol(f"\Delta {variable}"))**2

    # Return the error function
    return sy.sqrt(total_diffrential)


def Find_nearest(array, value):
    """
    Find the nearest variable in a list based on a input value
    """
    # Determine the nearest index based on the smallest distance between the array value and
    # the input value 
    idx = (np.abs(array - value)).argmin()

    # Return the nearest value
    return array[idx]



def Round_sigfig(x, fig, type_rounding="Normal", format="numerical"):
    """
    Function to round a number (or array) to n significant digits


    Input:
        x (float): a number that needs to be rounded 
        fig (int): the number of significant digits
        type (str): the type of rounding
            "Normal": rounds to the closest number
            "Up": rounds up
            "Down": rounds down
        format (str): the data type it should return

    Output:
        (float/int) a number rounded based on the amount of significant digits

    """
    
    # Define a result variable
    result = None

    # Determine the highest power of 10 that can fit in x
    int_count_10 = np.floor(np.log10(np.abs(x)))

    # Use normal rounding
    if type_rounding == "Normal":
        
        # Determine the shifting factor
        shifter = 10**int_count_10

        # Shift x by shifter round n digits and shift x back by shifter
        result = np.round(x / shifter, fig-1)*shifter
    
    # Use ceil to round
    elif type_rounding == "Up":

        # Determine the shifting factor
        shifter = 10**(fig - int_count_10 - 1)

        # Shift x by shifter round n digits up and shift x back by shifter
        result = np.ceil(x * shifter)/shifter

    # Use floor to round
    elif type_rounding == "Down":

        # Determine the shifting factor
        shifter = 10**(fig - int_count_10 - 1)

        # Shift x by shifter round n digits down and shift x back by shifter
        result = np.floor(x * shifter)/shifter

    else:
        raise ValueError("Unkown type of rounding only Normal, Up and Down are available")

    if format == "numerical":
        return result
    
    elif format == "text":
        """W.I.P"""
        if type(result).__module__ == "numpy":
            str_result = result.astype("str")
            str_result_return = []

            print(str_result)
            for r in str_result:
                i = r.index(".")
                n = len(r[i:])-1
                diff = fig - (len(r)-1)
                
                
                print(diff, len(r)-1, r, i, n)
                
                if diff < 0:
                    str_result_return.append(r[:diff])
                elif diff > 0:
                    str_result_return.append(r + "0"*diff)
                else:
                    str_result_return.append(r)

            return np.array(str_result_return)
        else:
            str_result = str(result)
            if len(str_result)-1 > fig:
                str_result = str_result[:-2]
            return str_result

    else:
        raise ValueError("Unkown format only numerical and text are available")

class Plotter():
    """
    Plotting class containing functions and settings to format a scientific looking plot.
    """
    def __init__(self, seperator=","):
        """
        Initialization of the plotter class
        and loading of basic settings
        """
        self.separator = seperator
        self.Config_plot_style()

    def Config_plot_style(self):
        """
        Function to set the basic settings of the plot using
        rcParams 

        note:
            all parameters can be overwriten using basic mpl
        """
        # Turning on the grid
        mpl.rcParams["axes.grid"] = True

        # Setting standard line style and color
        mpl.rc("axes",
            prop_cycle=(
                mpl.cycler(color=["k", "k", "k", "k"]) +
                mpl.cycler(linestyle=["--", ":", "-.", "-"])
            )
            )

        # Setting linewidth for errorbars and plot
        mpl.rcParams["lines.linewidth"] = 1

        # Setting capsize for errorbars
        mpl.rcParams["errorbar.capsize"] = 2

        # Locing the legend to upper right
        mpl.rcParams["legend.loc"] = "upper right"

    def Decimal_format_axis(self, ax, decimalx=1, decimaly=1, decimalz=None, imaginary_axis=""):
        """
        Function to format the axis of the plot using a decimal formatter

        input:
            ax: mpl axis object
            decimalx (int): n digits to round to for the x axis
            decimaly (int): n digits to round to for the y axis
            decimalz (int): n digits to round to for the z axis
            imaginary_axis (str): adds i to the end of every number 
        """
        
        # Check for imaginary x axis and apply the formatter
        if "x" in imaginary_axis:
            ax.xaxis.set_major_formatter(DecimalAxisFormatter(decimalx, self.separator, True))
        else:
            ax.xaxis.set_major_formatter(DecimalAxisFormatter(decimalx, self.separator))
        
        # Check for imaginary y axis and apply the formatter
        if "y" in imaginary_axis:
            ax.yaxis.set_major_formatter(DecimalAxisFormatter(decimaly, self.separator, True))
        else:
            ax.yaxis.set_major_formatter(DecimalAxisFormatter(decimaly, self.separator))
            
        # Check if the z axis is used 
        if decimalz != None:
            # Check for imaginary z axis and apply the formatter
            if "z" in imaginary_axis:
                ax.zaxis.set_major_formatter(DecimalAxisFormatter(decimalz, self.separator, True))
            else:
                ax.zaxis.set_major_formatter(DecimalAxisFormatter(decimalz, self.separator))

    def Significant_figure_format_axis(self, ax, sigfigx=1, sigfigy=1, sigfigz=None, imaginary_axis=""):
        """
        Function to format the axis of the plot using a  Significant figure formatter

        input:
            ax: mpl axis object
            sigfigx (int): n significant digits to round to for the x axis
            sigfigy (int): n significant digits to round to for the y axis
            sigfigz (int): n significant digits to round to for the z axis
            imaginary_axis (str): adds i to the end of every number 
        """
        
        # Check for imaginary x axis and apply the formatter
        if "x" in imaginary_axis:
            ax.xaxis.set_major_formatter(SignificantFigureAxisFormatter(sigfigx, self.separator, True))
        else:
            ax.xaxis.set_major_formatter(SignificantFigureAxisFormatter(sigfigx, self.separator))
        
        # Check for imaginary y axis and apply the formatter
        if "y" in imaginary_axis:
            ax.yaxis.set_major_formatter(SignificantFigureAxisFormatter(sigfigy, self.separator, True))
        else:
            ax.yaxis.set_major_formatter(SignificantFigureAxisFormatter(sigfigy, self.separator))
            
        # Check if the z axis is used 
        if sigfigz != None:
            # Check for imaginary z axis and apply the formatter
            if "z" in imaginary_axis:
                ax.zaxis.set_major_formatter(SignificantFigureAxisFormatter(sigfigz, self.separator, True))
            else:
                ax.zaxis.set_major_formatter(SignificantFigureAxisFormatter(sigfigz, self.separator))

    def Set_xlabel(self, ax, physical_quantity, unit, tenpower=0):
        """
        Function to create a label on the x axis

        ax: mpl axis object
        physical_quantity (str): the pysical quantity
        unit (str): the unit of the pysical quantity
        tenpower (int): the power for scientific notation
        """

        # Set label without scientific notation
        if tenpower == 0:
            ax.set_xlabel(f"${physical_quantity}$ [{unit}]", loc="center")


        # Set label using scientific notation
        elif tenpower != 0:
            ax.set_xlabel(f"${physical_quantity}$" + "$\cdot 10^{" + str(tenpower) + "}$" +  f"[{unit}]", loc="center")


    def Set_ylabel(self, ax, physical_quantity, unit, tenpower=0):
        """
        Function to create a label on the y axis

        ax: mpl axis object
        physical_quantity (str): the pysical quantity
        unit (str): the unit of the pysical quantity
        tenpower (int): the power for scientific notation
        """

        
        # Set label without scientific notation
        if tenpower == 0:
            ax.set_ylabel(f"${physical_quantity}$ [{unit}]", loc="center")

        # Set label using scientific notation
        elif tenpower != 0:
            ax.set_ylabel(f"${physical_quantity}$" + "$\cdot 10^{" + str(tenpower) + "}$" +  f"[{unit}]", loc="center")

    def Set_zlabel(self, ax, physical_quantity, unit, tenpower=0):
        """
        Function to create a label on the z axis

        ax: mpl axis object
        physical_quantity (str): the pysical quantity
        unit (str): the unit of the pysical quantity
        tenpower (int): the power for scientific notation
        """

        # Some mpl 3D stuff
        rot = 0
        ax.zaxis.set_rotate_label(False)


        # Set label without scientific notation
        if tenpower == 0:
            ax.set_zlabel(f"${physical_quantity}$ [{unit}]", rotation=rot)

        # Set label using scientific notation
        elif tenpower != 0:
            ax.set_zlabel(f"${physical_quantity}$" + "$\cdot 10^{" + str(tenpower) + "}$" +  f"[{unit}]", rotation=rot)
