Tools
=====

General purpose functions
*************************

.. py:function:: Dataframe_to_latex(dataframe, sep=",")

   A function to convert a pandas dataframe to a latex table. When running
   this function the output will be printed.

   :param seperator: The dataframe that needs to be converted
   :type kind: pandas.Dataframe

   :param seperator: The seperator the type used can be "." or ",".
   :type kind: str

.. py:function:: Find_nearest(array, value)

   A function to convert a pandas dataframe to a latex table. When running
   this function the output will be printed.

   :param array: The array in which to search for a given value
   :type kind: numpy.array

   :param value: The value to search for
   :type kind: float

   :return: A tuple containing the value closest to the value and the index on where to find it.
   :rtype: Tuple

.. py:function:: Remove_ramp(signal, gues=None)

    Function to remove a ramp from a signal. Signal must be a numpy array.

    :param float signal: The signal that needs a ramp removed
    :param float gues: geus for the ramp in the signal 

    :return: Signal without a ramp
    :rtype: float

.. py:function:: Smooth(signal, gues=None)

    Function to smooth out a signal. Signal must be numpy array.

    
    :param float signal: Signal to be smoothed
    :param float box_pts: Smoothess of the curve

    :return: Smoothed signal
    :rtype: float



Error analysis and statistics
*****************************


.. py:function:: Error_function(function, variables)

   Function to determine the error of a function based on the errros of the variables of that function.

   :param function: A sympy expression of which the error function should be determined
   :type kind: sympy.core.add.Add

   :return: A sympy expression of the error function
   :rtype: sympy.core.add.Add

Example::

    from PToolkit import Error_function
    import sympy as sy

    I, R = sy.symbols("I, R")
    V = I*R

    error = Error_function(V, [I, R])

The outpur of the code:

.. math::

   \Delta V = \sqrt{\left|{I}\right|^{2} \left|{\Delta R}\right|^{2} + \left|{R}\right|^{2} \left|{\Delta I}\right|^{2}}

.. py:function:: Round_sigfig(x, fig, type_rounding="Normal", format="numerical")

   Function to determine the error of a function based on the errros of the variables of that function.
   This function also works with numpy arrays

   :param x: A float that needs to be rounded
   :type kind: float

   :param fig: The number of significant digits
   :type kind: int

   :param type: The type of rounding: "Normal" rounds to the closest number, "Up" rounds up, "Down" rounds down
   :type kind: str

   :param format: Unused param
   :type kind: str

   :return: A number rounded to a n significant digits
   :rtype: float


.. py:function:: Chi_square_test(theorie, mean, error)

   Function to perform a Chi^2 test

   :param float theorie:  Theoretical value of a data point
   :param float mean: The mean of that data point
   :param float error: The error of that data point



.. py:function:: Chi_square_dist(x, d)
    
    Function to calculate the values on a Chi^2 distribution

   :param float x:  The Chi^2 value
   :param int d: Degrees of freedom

   :return: The value at a given point in the Chi^2 distribution
   :rtype: float



.. py:function:: Calculate_degrees_of_freedom(n, v)
    
    Function to calculte the number of degrees of freedom

    :param int n: Amount of independent data points
    :param int v: Amount of parameters

    :return: Degrees of freedom
    :rtype: int

.. py:function:: Calculate_p_value(chi, d)

    Function to calculate the p value of a Chi^2 distribution

    :param float chi: The value found for chi^2
    :param int d: Degrees of freedom

    :return: p value
    :rtype: float





