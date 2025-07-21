from pyswip import Prolog

prolog = Prolog()
prolog.consult("logic.pl",relative_to=__file__)



