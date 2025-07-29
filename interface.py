from pyswip import Prolog

family = Prolog()
family.consult("rules.pl", relative_to=__file__)

relationships = {
    "son",
    "daughter",
    "father",
    "mother",
    "grandson",
    "granddaughter",
    "grandfather",
    "grandmother",
    "aunt",
    "uncle",
    "nephew",
    "niece",
    "siblings",
    "sisters",
    "brothers",
}

statement_patterns = {
    "{A} and {B} are siblings.": "sibling({A},{B})",
    "{A} is a sister of {B}.": "sister({A},{B})",
    "{A} is the mother of {B}.": "mother({A},{B})",
    "{A} is a grandmother of {B}.": "grandmother({A},{B})",
    "{A} is a child of {B}.": "child({A},{B})",
    "{A} is a daughter of {B}.": "daughter({A},{B})",
    "{A} is an uncle of {B}.": "uncle({A},{B})",
    "{A} is a brother of {B}.": "brother({A},{B})",
    "{A} is the father of {B}.": "father({A},{B})",
    "{A} and {B} are the parents of {C}.": "parent({A},{B},{C})",
    "{A} is a grandfather of {B}.": "grandfather({A},{B})",
    "{A},{B} and {C} are children of {D}.": "children({A},{B},{C},{D})",
    "{A} is a son of {B}.": "son({A},{B})",
    "{A} is an aunt of {B}.": "aunt({A},{B})",
}


# TO DO: Figure out how to parse sentences and determine which sentences are valid
# Deal with some flaws of implications and with contingencies and contradictions


family.retractall
family.assertz("male(jerry)")
family.assertz("parent_of(ben,jerry)")

results = list(family.query("son_of(jerry, X)"))
print("son_of():", results)
print("Result is:", "True" if results else "False")
