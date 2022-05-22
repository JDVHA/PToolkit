import os
import matplotlib.ticker as mticker
import sympy as sy
import matplotlib as mpl
from math import floor, log10, ceil
from locale import setlocale, LC_NUMERIC
import numpy as np


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

def Error_function(function, variables):
    """
    Functie die van elke wiskundige functie de onauwkeurigheid bepaald.
    Door elke variable appart te diffrentieren.
    
    input:
        function (sympy.core.add.Add): een sympy vergelijking waar de totale diffrentiaal van 
        moet woden bepaald.
        variables (list): een list met daarin de sympy variable waar voor moet worden gedifferentieerd

    return:
        de onauwkeurigheids vergelijking voor een functie in de vorm van een sympy vergelijking

    """
    # Defineer de totale diffrentiaal
    total_diffrential = 0

    # Loop door elke variable en bepaal de diffrentiaal voor 1 variable
    for variable in variables:
        total_diffrential += sy.Abs(sy.diff(function, variable))**2 * sy.Abs(sy.Symbol(f"\Delta {variable}"))**2

    return sy.sqrt(total_diffrential)




def Config_plot_style(local=False):
    # Zet de grid aan
    mpl.rcParams["axes.grid"] = True

    # Zet de standaard kleur en set de cyler voor de linestyles
    mpl.rc('axes',
        prop_cycle=(
            mpl.cycler(color=['k', 'k', 'k', 'k']) +
            mpl.cycler(linestyle=['--', ':', '-.', '-'])
        )
        )

    # Check voor locale en verander naar comma WERKT NIET
    if local:
        setlocale(LC_NUMERIC)
        mpl.rcParams['axes.formatter.use_locale'] = True

def Find_nearest(array, value):
    """
    Vind de waarde die het digst bij value zit in de array
    """
    idx = (np.abs(array - value)).argmin()
    return array[idx]



# W.I.P
def Round_sigfig(x, fig, type="Normal"):
    """
    Input:
        x: het getal wat moet worden afgerond op een significat cijfer. 
        fig: het aantal significante cijfers
        type: soort van afronding
            "Normal": gebruikt round om af te ronden
            "Up": Rond af naar boven
            "Down": Rond af naar beneden

    Output:
        (float/int) een op een x aantal significat cijfer afrond cijfer.

    Werking: 
    
    De shifter bepaald met welke factor 10 x moet worden verschoven om een getal voor de comma te krijgen.
    Door x te delen door de shifter komt de waarde van x in de vorm staan van: 4.7584 vervolgens kan er geround worden
    op het aantal signifacte cijfers min 1 omdat het cijfer voor wel een significat fig is maar geen decimaal. Vervolgens
    wordt de waarde terug geschoven met behulp van shifter.
    """

    # Bepaal hoevaak een int van 10 in x past
    int_aantal_10 = np.floor(np.log10(np.abs(x)))

    # Gebruik normale afronding
    if type == "Normal":
        
        # Bepaal shifting factor
        shifter = 10**int_aantal_10

        # Rond af en return
        return np.round(x / shifter, fig-1)*shifter
    
    # Rond af naar boven
    elif type == "Up":

        # Bepaal shifting factor
        shifter = 10**(fig - int_aantal_10 - 1)

        # Rond af en return
        return np.ceil(x * shifter)/shifter

    # Rond af naar beneden
    elif type == "Down":

        # Bepaal shifting factor en return
        shifter = 10**(fig - int_aantal_10 - 1)

        # Rond af en return
        return np.floor(x * shifter)/shifter
