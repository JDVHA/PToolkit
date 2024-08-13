Keyboards
==========

.. py:function:: ArrowKeyPad(root, commandgrid, size=(4, 4), includehome=False, design="*")

    Class that creates a widget having a variable amount of buttons that can be mapped. 
    Great for controlling movement based robots. 

    :param root: Parent window

    :param commandgrid: A 3x3 list of lists with a function or None in each of its entrys. Each of the entrys corrosponds with the button at that position.
    :type commandgrid: list

    :param size: Tuple of the size of the buttons.
    :type size: tuple

    :param includehome: If a home button must be included.
    :type includehome: bool

    :param design: The design used for the widget options: "*", "+", "<>" and "v^"
    :type design: str

Example::

    # To be added


SerialPortSelector
===========

.. py:function:: SerialPortSelector(root, commandgrid, size=(4, 4), includehome=False, design="*")

    Class that creates a widget having a variable amount of buttons that can be mapped. 
    Great for controlling movement based robots. 

    :param root: Parent window

    :param commandgrid: A 3x3 list of lists with a function or None in each of its entrys. Each of the entrys corrosponds with the button at that position.
    :type commandgrid: list

    :param size: Tuple of the size of the buttons.
    :type size: tuple

    :param includehome: If a home button must be included.
    :type includehome: bool

    :param design: The design used for the widget options: "*", "+", "<>" and "v^"
    :type design: str