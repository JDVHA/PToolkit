import os
import matplotlib.ticker as mticker
import sympy as sy
import matplotlib as mpl
from math import floor, log10, ceil
from scipy.integrate import quad
import numpy as np
from scipy.special import gamma
from scipy.optimize import curve_fit
import warnings
import inspect


def Deprecated(message="", type="removed"):
    def wrapper(func):
        if inspect.isclass(func):
            fmt = "class"
        
        elif inspect.ismethod(func):
            fmt = "method"

        elif inspect.isfunction:
            fmt = "function"
        warnings.warn(f"The {fmt} {func.__name__} will be {type} in future versions of PToolkit please use a diffrent {fmt} or read the new documentation. {message}", DeprecationWarning)
        return func
    
    return wrapper


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
    return array[idx], idx



def Round_sigfig(x, fig, type_rounding="Normal", format="str"):
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
        raise ValueError("Unkown type of rounding only: Normal, Up and Down are available")

    if format == "numerical":
        return result
    elif format == "str":
        try:
            return str(result)[:fig]
        except:
            return str(result)
    else:
        raise ValueError("Unkown type of format only: numerical and str are available")
    

def Dataframe_to_latex(dataframe, sep=","):
    """
    Function to convert a pandas datafrrame in a latex table

    Input:
    dataframe (pandas dataframe): The dataframe thats needs to be converted
    sep (string): The seperator sign

    """

    # Create a string to store the latex table
    latex_string = "" 

    # Get the headers from pandas dataframe
    headers = dataframe.columns

    # Get the column count of the pandas dataframe
    column_count = len(dataframe.columns)

    # Add the top side of the pandas dataframe
    latex_string = "\\begin{table}[h]\n  \\centering\n  \\caption{Caption}\n   \\begin{tabular}" + "{" + "c"*column_count + "}" + "\n"
    
    # Create a header variable
    header = "       "

    # Loop through all headers and add the column name to the header variabla
    for i, h in enumerate(headers):

        # Add column name to the header
        header += h

        # Check if it is the last column
        if i != len(headers)-1:

            # If not the last add &
            header += " & "  
        else:
            # If last then add \\ to the end
            header += "\\\ \n"

    # Add the header to the dataframe
    latex_string += header

    # Add the hline to the latex string
    latex_string += "       \\hline \n"


    # Loop over all rows in the dataframe
    for row in dataframe.itertuples(index=False):

        # Create row string variable
        row_string= "       "
        
        # Loop over all elements in a row
        for i, element in enumerate(row):


            # Add element to the row string
            row_string += str(element).replace(".", sep)

            # Check if it is the last element
            if i != len(row)-1:

                # If it is not the last element add &
                row_string += " & "  
            else:
                # If it is the last element add \\
                row_string += "\\\ \n"

        # Add the row string to the latex string
        latex_string += row_string
    
    # Add to botem of the latex table to the string
    latex_string += "   \\end{tabular}\n   \\label{tab:my_label}\n\\end{table}"

    # Print the string so the user can copy it
    print(latex_string)

def Chi_square_test(theorie, mean, error):
    """
    Function to perform a Chi^2 test


    Input (must be a numpy array):
        Theoretical values (float): Theoretical value of a data point
        Mean data (float): The mean of that data point
        Error (float): The error of that data point

    Output:
        The value of Chi^2 test
    """
    return np.sum(((theorie-mean)/error)**2)

def Chi_square_dist(x, d):
    """
    Function to calculate the values on a Chi^2 dist

    Input:
        x (float): The Chi^2 value
        d (int): Degrees of freedom

    Output:
        The value at a given point in the Chi^2 dist
    """
    return (x**(d/2-1)*np.exp(-x/2))/(2**(d/2)*gamma(d/2))


def Calculate_degrees_of_freedom(n, v):
    """
    Function to calculte the number of degrees of freedom

    Input:
        n (int): Amount of independent data points
        v (int): Amount of parameters

    Output:
        Amount of degrees of freedom
    """
    return n-v


def Calculate_p_value(chi, d):
    """
    Function to calculte the p value based on a chi^2 dist

    Input:
        chi (float): The value found for chi^2
        d (int): Degrees of freedom

    Output (float):
        The p value for a fiven chi^2
    """
    v = lambda x: (x**(d/2-1)*np.exp(-x/2))/(2**(d/2)*gamma(d/2))
    p = quad(v, chi, np.Inf)[0]
    return p


def Remove_ramp(signal, gues=None):
    """
    Function to remove a ramp from a signal

    Input:
        signal (float): The signal that needs a ramp removed
        gues (float): geus for the ramp in the signal 

    Output (float):
        Signal without a ramp
    """

    # Create a x array
    x = np.linspace(0, len(signal), len(signal))

    # Define the ramp it self
    line_func = lambda x, a, b: a*x+b  

    # Curve fit the ramp to the signal
    popt, pcov = curve_fit(line_func, x, signal, p0=gues)

    # Get a and b
    a, b = popt

    # Calculate the difference between the fit and the signal
    return signal - line_func(x, a, b)


def Smooth(signal, box_pts):
    """
    Function to smooth out a signal.

    Input:
        signal (float): Signal to be smoothed
        box_pts (int): Smoothess of the curve

    Return:
        Smoothed signal

    Credits to scrx2: https://stackoverflow.com/a/26337730 
    """
    box = np.ones(box_pts)/box_pts
    signal_smooth = np.convolve(signal, box, mode='same')
    return signal_smooth