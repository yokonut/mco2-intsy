from pyswip import Prolog

family = Prolog()
family.consult("rules.pl",relative_to=__file__)

language = Prolog()
language.consult("language.pl",relative_to=__file__)

#TO DO: Figure out how to parse sentences and determine which sentences are valid
# Deal with some flaws of implications and with contingencies and contradictions

family.retractall
family.assertz("male(jerry)")
family.assertz("parent_of(ben,jerry)")

results = list(family.query("son_of(jerry, X)"))
print("son_of():", results)
print("Result is:", "True" if results else "False")
    