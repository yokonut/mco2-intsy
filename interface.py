from pyswip import Prolog

family = Prolog()
family.consult("rules.pl",relative_to=__file__)

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
    "brothers"
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
    "{A} is an aunt of {B}.": "aunt({A},{B})"
}


# question_patterns = {
    
#     "Are {A} and {B} siblings?": lambda A, B: f"sibling({A.lower()}, {B.lower()})",
#     "Is {A} a sister of {B}?": lambda A, B: f"sister({A.lower()}, {B.lower()})",
#     "Is {A} a brother of {B}?": lambda A, B: f"brother({A.lower()}, {B.lower()})",
#     "Is {A} the mother of {B}?": lambda A, B: f"mother({A.lower()}, {B.lower()})",
#     "Is {A} the father of {B}?": lambda A, B: f"father({A.lower()}, {B.lower()})",
#     "Are {A} and {B} the parents of {C}?": lambda A, B, C: f"parent({A.lower()}, {C.lower()}) , parent({B.lower()}, {C.lower()})",
#     "Is {A} a grandmother of {B}?": lambda A, B: f"grandmother({A.lower()}, {B.lower()})",
#     "Is {A} a daughter of {B}?": lambda A, B: f"daughter({A.lower()}, {B.lower()})",
#     "Is {A} a son of {B}?": lambda A, B: f"son({A.lower()}, {B.lower()})",
#     "Is {A} a child of {B}?": lambda A, B: f"child({A.lower()}, {B.lower()})",
#     "Are {A}, {B} and {C} children of {D}?": lambda A, B, C, D: f"child({A.lower()}, {D.lower()}) , child({B.lower()}, {D.lower()}) , child({C.lower()}, {D.lower()})",
#     "Is {A} an uncle of {B}?": lambda A, B: f"uncle({A.lower()}, {B.lower()})",
#     "Who are the siblings of {A}?": lambda A: f"sibling(X, {A.lower()})",
#     "Who are the sisters of {A}?": lambda A: f"sister(X, {A.lower()})",
#     "Who are the brothers of {A}?": lambda A: f"brother(X, {A.lower()})",
#     "Who is the mother of {A}?": lambda A: f"mother(X, {A.lower()})",
#     "Who is the father of {A}?": lambda A: f"father(X, {A.lower()})",
#     "Who are the parents of {A}?": lambda A: f"parent(X, {A.lower()})",
#     "Is {A} a grandfather of {B}?": lambda A, B: f"grandfather({A.lower()}, {B.lower()})",
#     "Who are the daughters of {A}?": lambda A: f"daughter(X, {A.lower()})",
#     "Who are the sons of {A}?": lambda A: f"son(X, {A.lower()})",
#     "Who are the children of {A}?": lambda A: f"child(X, {A.lower()})",
#     "Is {A} an aunt of {B}?": lambda A, B: f"aunt({A.lower()}, {B.lower()})",
#     "Are {A} and {B} relatives?": lambda A, B: f"relative({A.lower()}, {B.lower()})"
# }

question_patterns = {
    "Are {A} and {B} siblings?": lambda A, B: f"query_sibling({A.lower()}, {B.lower()})",
    "Is {A} a sister of {B}?": lambda A, B: f"query_sister({A.lower()}, {B.lower()})",
    "Is {A} a brother of {B}?": lambda A, B: f"query_brother({A.lower()}, {B.lower()})",
    "Is {A} the mother of {B}?": lambda A, B: f"query_mother({A.lower()}, {B.lower()})",
    "Is {A} the father of {B}?": lambda A, B: f"query_father({A.lower()}, {B.lower()})",
    "Are {A} and {B} the parents of {C}?": lambda A, B, C: f"query_parents_of({A.lower()}, {B.lower()}, {C.lower()})",
    "Is {A} a grandmother of {B}?": lambda A, B: f"query_grandmother({A.lower()}, {B.lower()})",
    "Is {A} a grandfather of {B}?": lambda A, B: f"query_grandfather({A.lower()}, {B.lower()})",
    "Is {A} a daughter of {B}?": lambda A, B: f"query_daughter({A.lower()}, {B.lower()})",
    "Is {A} a son of {B}?": lambda A, B: f"query_son({A.lower()}, {B.lower()})",
    "Is {A} a child of {B}?": lambda A, B: f"query_child({A.lower()}, {B.lower()})",
    "Are {A}, {B} and {C} children of {D}?": lambda A, B, C, D: f"query_children_of({A.lower()}, {B.lower()}, {C.lower()}, {D.lower()})",
    "Is {A} an uncle of {B}?": lambda A, B: f"query_uncle({A.lower()}, {B.lower()})",
    "Is {A} an aunt of {B}?": lambda A, B: f"query_aunt({A.lower()}, {B.lower()})",
    "Are {A} and {B} relatives?": lambda A, B: f"query_relative({A.lower()}, {B.lower()})",

    # WHO-type queries
    "Who are the siblings of {A}?": lambda A: f"query_who_siblings({A.lower()})",
    "Who are the sisters of {A}?": lambda A: f"query_who_sisters({A.lower()})",
    "Who are the brothers of {A}?": lambda A: f"query_who_brothers({A.lower()})",
    "Who is the mother of {A}?": lambda A: f"query_who_mother({A.lower()})",
    "Who is the father of {A}?": lambda A: f"query_who_father({A.lower()})",
    "Who are the parents of {A}?": lambda A: f"query_who_parents({A.lower()})",
    "Who are the daughters of {A}?": lambda A: f"query_who_daughters({A.lower()})",
    "Who are the sons of {A}?": lambda A: f"query_who_sons({A.lower()})",
    "Who are the children of {A}?": lambda A: f"query_who_children({A.lower()})"
}



#TO DO: Figure out how to parse sentences and determine which sentences are valid
# Deal with some flaws of implications and with contingencies and contradictions




family.retractall
family.assertz("male(jerry)")
family.assertz("parent_of(ben,jerry)")

results = list(family.query("son_of(jerry, X)"))
print("son_of():", results)
print("Result is:", "True" if results else "False")
    