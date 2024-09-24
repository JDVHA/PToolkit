Deprecated
==========

None of these classes or functions are supported and may be removed in the future.

Plotting
********

Plotter
--------


Plotting using Ptoolkit requires the use of the ``Plotter()`` object

.. py:function:: Plotter(seperator=",")

   Plotting class containing the functions and settings to format a scientific looking figure

   :param seperator: The seperator the type used on the axis can be "." or ",".
   :type kind: str


.. py:function:: Plotter.Config_plot_style()

    Method to configure the plot style of Ptoolkit. This method is automaticly run when creating a Plotter object.
    If for any reason the style is gone run this command.


Axis formatting
----------------

.. py:function:: Plotter.Decimal_format_axis(ax, decimalx=1, decimaly=1, decimalz=None, imaginary_axis="")

    Method to format the axis of the plot using a decimal formatter

    :param ax: matplotlib axis object.
    :type ax: matplotlib.axes

    :param decimalx: the amount of decimals used for each tick on the x-axis.
    :type decimalx: int

    :param decimaly: the amount of decimals used for each tick on the y-axis.
    :type decimalx: int

    :param decimalz: the amount of decimals used for each tick on the z-axis.
    :type decimalx: int

    :param imaginary_axis: string containing the axis that are imaginary
    :type imaginary_axis: str

.. py:function:: Plotter.Significant_figure_format_axis(ax, decimalx=1, decimaly=1, decimalz=None, imaginary_axis="")

    Method to format the axis of the plot using a significant figure formatter

    :param ax: matplotlib axis object.
    :type ax: matplotlib.axes

    :param sigfigx: the amount of significant digits used for each tick on the x-axis.
    :type decimalx: int

    :param sigfigy: the amount of significant digits for each tick on the y-axis.
    :type decimalx: int

    :param sigfigz: the amount of significant digits for each tick on the z-axis.
    :type decimalx: int

    :param imaginary_axis: string containing the axis that are imaginary
    :type imaginary_axis: str



.. py:function:: Plotter.Set_xlabel(ax, physical_quantity, unit, tenpower=0)

    Method to set the x label on given axis object. When using latex symbols
    it is required to add $$ only by the unit parameter.

    :param ax: matplotlib axis object.
    :type ax: matplotlib.axes

    :param physical_quantity: The physical_quantity that needs to be placed on the x axis
    :type physical_quantity: str

    :param unit: The unit of the physical_quantity that needs to be placed on the x axis
    :type unit: str

    :param tenpower: The power for scientific notation if 0 scientific notation will not be used
    :type tenpower: int


.. py:function:: Plotter.Set_ylabel(ax, physical_quantity, unit, tenpower=0)

    Method to set the y label on given axis object. When using latex symbols
    it is required to add $$ only by the unit parameter.

    :param ax: matplotlib axis object.
    :type ax: matplotlib.axes

    :param physical_quantity: The physical_quantity that needs to be placed on the y axis
    :type physical_quantity: str

    :param unit: The unit of the physical_quantity that needs to be placed on the y axis
    :type unit: str

    :param tenpower: The power for scientific notation if 0 scientific notation will not be used
    :type tenpower: int
    

.. py:function:: Plotter.Set_zlabel(ax, physical_quantity, unit, tenpower=0)

    Method to set the z label on given axis object. When using latex symbols
    it is required to add $$ only by the unit parameter.

    :param ax: matplotlib axis object.
    :type ax: matplotlib.axes

    :param physical_quantity: The physical_quantity that needs to be placed on the z axis
    :type physical_quantity: str

    :param unit: The unit of the physical_quantity that needs to be placed on the z axis
    :type unit: str

    :param tenpower: The power for scientific notation if 0 scientific notation will not be used
    :type tenpower: int

.. py:function:: Standaard_error_per_index(*arrays)

   Function to calculate the Standaard error per index. Given n arrays the standaard error
   will be calculated using the ithe elements of the given arrays.

   :param arrays: n amount of numpy arrays
   :type kind: np.array

   :return: The standaard error of each index
   :rtype: np.array
