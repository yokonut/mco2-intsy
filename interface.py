from pyswip import Prolog
import re
from relationships import *

family = Prolog()
family.consult("rules.pl",relative_to=__file__)

# Update the relationships module to use our family instance
import relationships
relationships.prolog = family

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

# Initialize some test data
family.retractall("male(_)")
family.retractall("female(_)")
family.retractall("parent_of(_,_)")

family.assertz("male(jerry)")
family.assertz("male(ben)")
family.assertz("female(sarah)")
family.assertz("female(emma)")
family.assertz("parent_of(ben, jerry)")
family.assertz("parent_of(sarah, jerry)")
family.assertz("parent_of(ben, emma)")
family.assertz("parent_of(sarah, emma)")

# Test query to verify setup
try:
    results = list(family.query("son_of(jerry, X)"))
    print("son_of():", results)
    print("Result is:", "True" if results else "False")
except Exception as e:
    print(f"Prolog setup error: {e}")

def process_statement(user_input):
    """Process statements and return emoji responses like in relationships.py"""
    try:
        # Extract names from the input using regex - exclude common words
        all_words = re.findall(r'\b[A-Za-z]+\b', user_input)
        # Filter out common words that are not names
        exclude_words = {'is', 'are', 'the', 'a', 'an', 'of', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'with', 'by', 'from', 'up', 'down', 'out', 'off', 'over', 'under', 'mother', 'father', 'son', 'daughter', 'sister', 'brother', 'grandfather', 'grandmother', 'uncle', 'aunt', 'child', 'children', 'sibling', 'siblings'}
        names = [word for word in all_words if word.lower() not in exclude_words]
        
        if len(names) < 2:
            return "❓ I need at least two names to understand the relationship."
        
        # Determine the relationship type and call appropriate function
        if "mother" in user_input.lower():
            assertions = mother(names[0], names[1])
            return assertz(assertions)
        elif "father" in user_input.lower():
            assertions = father(names[0], names[1])
            return assertz(assertions)
        elif "son" in user_input.lower():
            assertions = son(names[0], names[1])
            return assertz(assertions)
        elif "daughter" in user_input.lower():
            assertions = daughter(names[0], names[1])
            return assertz(assertions)
        elif "child" in user_input.lower():
            assertions = child(names[0], names[1])
            return assertz(assertions)
        elif "sibling" in user_input.lower():
            return sibling(names[0], names[1])
        elif "sister" in user_input.lower():
            return sister(names[0], names[1])
        elif "brother" in user_input.lower():
            return brother(names[0], names[1])
        elif "grandfather" in user_input.lower():
            return grandfather(names[0], names[1])
        elif "grandmother" in user_input.lower():
            return grandmother(names[0], names[1])
        elif "uncle" in user_input.lower():
            return uncle(names[0], names[1])
        elif "aunt" in user_input.lower():
            return aunt(names[0], names[1])
        else:
            return "🤔 I don't understand that relationship. Try using words like mother, father, son, daughter, sibling, etc."
    except Exception as e:
        return f"❌ Error processing statement: {str(e)}"

def process_question(user_input):
    """Process questions and return emoji responses"""
    try:
        # Extract names from the input using regex - exclude common words
        all_words = re.findall(r'\b[A-Za-z]+\b', user_input)
        # Filter out common words that are not names
        exclude_words = {'is', 'are', 'the', 'a', 'an', 'of', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'with', 'by', 'from', 'up', 'down', 'out', 'off', 'over', 'under', 'mother', 'father', 'son', 'daughter', 'sister', 'brother', 'grandfather', 'grandmother', 'uncle', 'aunt', 'child', 'children', 'sibling', 'siblings'}
        names = [word for word in all_words if word.lower() not in exclude_words]
        
        if len(names) < 2:
            return "❓ I need at least two names to answer that question."
        
        # Convert to lowercase for Prolog queries
        names = [name.lower() for name in names]
        
        # Determine the question type and query
        if "sibling" in user_input.lower():
            results = list(family.query(f"siblings({names[0]}, {names[1]})"))
            return "✅ Yes, they are siblings!" if results else "❌ No, they are not siblings."
        elif "sister" in user_input.lower():
            results = list(family.query(f"sister_of({names[0]}, {names[1]})"))
            return "✅ Yes, she is the sister!" if results else "❌ No, she is not the sister."
        elif "brother" in user_input.lower():
            results = list(family.query(f"brother_of({names[0]}, {names[1]})"))
            return "✅ Yes, he is the brother!" if results else "❌ No, he is not the brother."
        elif "mother" in user_input.lower():
            results = list(family.query(f"mother_of({names[0]}, {names[1]})"))
            return "✅ Yes, she is the mother!" if results else "❌ No, she is not the mother."
        elif "father" in user_input.lower():
            results = list(family.query(f"father_of({names[0]}, {names[1]})"))
            return "✅ Yes, he is the father!" if results else "❌ No, he is not the father."
        elif "son" in user_input.lower():
            results = list(family.query(f"son_of({names[0]}, {names[1]})"))
            return "✅ Yes, he is the son!" if results else "❌ No, he is not the son."
        elif "daughter" in user_input.lower():
            results = list(family.query(f"daughter_of({names[0]}, {names[1]})"))
            return "✅ Yes, she is the daughter!" if results else "❌ No, she is not the daughter."
        elif "grandfather" in user_input.lower():
            results = list(family.query(f"grandfather_of({names[0]}, {names[1]})"))
            return "✅ Yes, he is the grandfather!" if results else "❌ No, he is not the grandfather."
        elif "grandmother" in user_input.lower():
            results = list(family.query(f"grandmother_of({names[0]}, {names[1]})"))
            return "✅ Yes, she is the grandmother!" if results else "❌ No, she is not the grandmother."
        elif "uncle" in user_input.lower():
            results = list(family.query(f"uncle_of({names[0]}, {names[1]})"))
            return "✅ Yes, he is the uncle!" if results else "❌ No, he is not the uncle."
        elif "aunt" in user_input.lower():
            results = list(family.query(f"aunt_of({names[0]}, {names[1]})"))
            return "✅ Yes, she is the aunt!" if results else "❌ No, she is not the aunt."
        elif "child" in user_input.lower():
            results = list(family.query(f"child_of({names[0]}, {names[1]})"))
            return "✅ Yes, they are child and parent!" if results else "❌ No, they are not child and parent."
        else:
            return "🤔 I don't understand that question. Try asking about relationships like siblings, mother, father, etc."
    except Exception as e:
        return f"❌ Error processing question: {str(e)}"

def handle_user_input(user_input):
    """Main function to handle user input and return appropriate response"""
    user_input = user_input.strip()
    
    # Check if it's a question (contains "?" or question words)
    if "?" in user_input or any(word in user_input.lower() for word in ["who", "what", "when", "where", "why", "how"]):
        return process_question(user_input)
    # Check if it's a statement (contains words like "is", "are", "of")
    elif any(word in user_input.lower() for word in ["is", "are", "of"]):
        return process_statement(user_input)
    else:
        return "🤔 Please ask a question or make a statement about family relationships."    