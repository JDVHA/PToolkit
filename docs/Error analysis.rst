Error analysis
==============


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


.. py:function:: Standaard_error_per_index(*arrays)

   Function to calculate the Standaard error per index. Given n arrays the standaard error
   will be calculated using the ithe elements of the given arrays.

   :param arrays: n amount of numpy arrays
   :type kind: np.array

   :return: The standaard error of each index
   :rtype: np.array