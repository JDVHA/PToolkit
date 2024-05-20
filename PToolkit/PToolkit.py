import os
import matplotlib.ticker as mticker
import sympy as sy
import matplotlib as mpl
from math import floor, log10, ceil
from scipy.integrate import quad
import numpy as np
from scipy.special import gamma
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
    return array[idx], idx



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

    return result

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

    @Deprecated()
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

    @Deprecated()
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

    @Deprecated()
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


@Deprecated()
def Fourier_series_cos_term(func, k, omega_0):
    """
    Decorator to convert any function to a intergrant for a fourier series (cos)

    Input:
        func (python function object): A function that needs te be converted
        k (int): The index of the fourier sereies
        omega_0 (float): The ground radial velocity

    Output:
        A function multiplied by the cosine term in a fourier series 
    """

    # Create a wrapper and take all arguments from the function
    def wrapper(*args, **kwargs):
        # Convert  the function by passing all arguments in to the function 
        # Then multipli the function by cosine and give it as input the 
        # The index multiplied by the ground radial velocity and t (args[0] must be the variable)
        result = func(*args, **kwargs)*np.cos(k*omega_0*args[0])

        # Return the result of the function
        return result

    # Return the wrapper as the new function
    return wrapper

@Deprecated()
def Fourier_series_sin_term(func, k, omega_0):
    """
    Decorator to convert any function to a intergrant for a fourier series (sin)

    Input:
        func (python function object): A function that needs te be converted
        k (int): The index of the fourier sereies
        omega_0 (float): The ground radial velocity

    Output:
        A function multiplied by the sine term in a fourier series 
    """

    # Create a wrapper and take all arguments from the function
    def wrapper(*args, **kwargs):
        # Convert  the function by passing all arguments in to the function 
        # Then multipli the function by cosine and give it as input the 
        # The index multiplied by the ground radial velocity and t (args[0] must be the variable)
        result = func(*args, **kwargs)*np.sin(k*omega_0*args[0])

        # Return the result of the function
        return result

    # Return the wrapper as the new function
    return wrapper


@Deprecated()
def Fourier_series(func, T, n):
    """
    A function to calculate the coefficients of the fourier series for any function numerically
    Input:
        func (python function object): The function of which the fourier series has te be
            calculated
        T (float): The period of the 
        n (int): the amount of terms of the fourier series
    """

    # Calculate the ground radial velocity
    omega_0 = 2*np.pi/T

    # Create arrays for the coefficients of the fourier series
    array_a_n = []
    array_b_n = []

    # Calculate a_0 of the fourier series
    a_0 = 1/T*quad(func, 0, T)[0]

    # Loop over the terms
    for k in range(n):

        # Convert the function given to the intergrand for the value k
        func_cos = Fourier_series_cos_term(func, omega_0, k)
        func_sin = Fourier_series_sin_term(func, omega_0, k)

        # Calculate the intergral using scipy 
        a_n = 2/T*quad(func_cos, 0, np.pi)[0]
        b_n = 2/T*quad(func_sin, 0, np.pi)[0]

        # Append the coefficients to there respected arrays
        array_a_n.append(a_n)
        array_b_n.append(b_n)

    # Return a_0 and the coefficient arrays
    return a_0, array_a_n, array_b_n


@Deprecated("Nunpy it self can do this operation faster")
def Standaard_error_per_index(*arrays):
    """
    A function to calculate the standaard error per index

    Input (list or numpy array): Lists for wich the standaard error has 
    to be calculeted per index.

    Output (umpy array): A list of standaard errors per index
    """

    # Create a matrix with the given arrays
    M = np.array([*arrays])

    # Determine the shape of the matrix 
    rows = M.shape[0]
    columns = M.shape[1]
    
    # Create a array to store the std per column
    E = np.array([])

    # Loop over all the columns in the matrix
    for i in range(columns):

        # Calculate the std for all columns
        s = np.std(M[:,i], ddof=1)

        # Append the std to the array
        E = np.append(E, s)

    # Calculate the standaard error
    return E/np.sqrt(rows)

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
        theorie (float): Theoretical value of a data point
        mean (float): The mean of that data point
        error (float): The error of that data point

    Output:
        The value of Chi^2 test
    """
    return np.sum(((theorie-mean)/error)**2)

def Chi_square_dist(x, d):
    """
    Function to calculate the values on a Chi^2 dist

    Input:
        x (float): De Chi^2 value
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
