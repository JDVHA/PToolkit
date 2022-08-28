from gettext import install
from setuptools import setup


setup(
    name="PToolkit",
    version="1.0",
    description="A set of tools than is usefull in lots of diffrent fields. This toolkit contains functions to make professional looking matplotlib plot without spending time on the looks of the plot. Not only that this toolkit also provides functions for rounding and determining errors.",
    url="https://github.com/JDVHA/PToolkit",
    author="H.A.J de Vries",
    author_email="",
    license="MIT",
    install_requires=[
        "numpy",
        "matplotlib",
        "sympy"
    ]
)

