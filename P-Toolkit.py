import os
import matplotlib.ticker as mticker

class AxisFormatter(mticker.Formatter):
    """
    Formatter class om de punten op de assen te vervangen
    door comma's op basis van de hoeveelheid decimaal
    """
    def __init__(self, d):
        """Initilaze formatter class"""
        self.decimaal = d


    def __call__(self, x, pos=None):
        """
        Methode om de punten om de assen te vervangen met comma's

        input:
            x (float): een getal waarvan de punt naar comma moet worden verandert
        
        return:
            een getal waarvan de punt is veranvangen door een comma

        """
        s = str(round(x, self.decimaal))
        return f"${s.replace('.', '{,}')}$"


def get_root_dir():
    """W.I.P Functie om de dirname van de main file te krijgen"""
    return os.path.dirname(os.path.abspath(__file__))
