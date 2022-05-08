import os
import matplotlib.ticker as mticker
import sympy as sy

class AxisFormatter(mticker.Formatter):
    """
    Formatter class om de punten op de assen te vervangen
    door comma's op basis van de hoeveelheid decimaal
    """
    def __init__(self, decimaal):
        """Initilaze formatter class"""
        self.decimaal = decimaal


    def __call__(self, x, pos=None):
        """
        Methode om de punten om de assen te vervangen met comma's

        input:
            x (float): een getal waarvan de punt naar comma moet worden verandert
            pos: matplotlib variable
        
        return:
            een getal waarvan de punt is veranvangen door een comma

        """
        s = str(round(x, self.decimaal))
        return f"${s.replace('.', '{,}')}$"


def get_root_dir():
    """W.I.P Functie om de dirname van de main file te krijgen"""
    return os.path.dirname(os.path.abspath(__file__))

def Diffrential(function, variables):
    """
    Functie die van elke wiskundige functie de totale diffrentiaal bepaald.
    Door elke variable appart te diffrentieren
    
    input:
        function (sympy.core.add.Add): een sympy vergelijking waar de totale diffrentiaal van 
        moet woden bepaald.
        variables (list): een list met daarin de sympy variable waar voor moet worden gedifferentieerd

    return:
        de totale diffrentiaal van de gegeven functie in de vorm van een sympy vergelijking

    """
    # Defineer de totale diffrentiaal
    total_diffrential = 0

    # Loop door elke variable en bepaal de diffrentiaal voor 1 variable
    for variable in variables:
        total_diffrential += sy.Abs(sy.diff(function, variable)) * sy.Symbol(f"\Delta {variable}")

    return total_diffrential