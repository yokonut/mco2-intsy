from interface import handle_user_input, family

# Test 1: Sibling relationship
print("Test 1: Sibling relationship")
family.retractall("male(_)")
family.retractall("female(_)")
family.retractall("parent_of(_, _)")

family.assertz("male(jerry)")
family.assertz("male(mike)")
family.assertz("parent_of(john, jerry)")
family.assertz("parent_of(john, mike)")

response = handle_user_input("Are Jerry and Mike siblings?")
print(f"Input: Are Jerry and Mike siblings?")
print(f"Response: {response}")
print()

# Test 2: Contradiction detection
print("Test 2: Contradiction detection")
family.retractall("male(_)")
family.retractall("female(_)")
family.retractall("parent_of(_, _)")

family.assertz("male(charlie)")
family.assertz("female(diana)")
family.assertz("parent_of(charlie, diana)")

response = handle_user_input("Diana is the mother of Charlie")
print(f"Input: Diana is the mother of Charlie")
print(f"Response: {response}")
print()

# Test 3: WHO question deduplication
print("Test 3: WHO question deduplication")
family.retractall("male(_)")
family.retractall("female(_)")
family.retractall("parent_of(_, _)")

family.assertz("male(jerry)")
family.assertz("male(mike)")
family.assertz("female(emma)")
family.assertz("parent_of(john, jerry)")
family.assertz("parent_of(john, mike)")
family.assertz("parent_of(john, emma)")

response = handle_user_input("Who are the siblings of Jerry?")
print(f"Input: Who are the siblings of Jerry?")
print(f"Response: {response}") 