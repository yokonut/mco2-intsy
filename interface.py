from pyswip import Prolog
from relationships import (
    prolog, assertz,
    mother, father, son, daughter, child, children,
    sibling, aunt, uncle, sister, brother,
    grandmother, grandfather, parent
)

import re


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
    "{A} and {B} are siblings": "sibling({A}, {B})",
    "{A} is a sister of {B}": "sister({A},{B})",
    "{A} is the mother of {B}": "mother({A},{B})",
    "{A} is a grandmother of {B}": "grandmother({A},{B})",
    "{A} is a child of {B}": "child({A},{B})",
    "{A} is a daughter of {B}": "daughter({A},{B})",
    "{A} is an uncle of {B}": "uncle({A},{B})",
    "{A} is a brother of {B}": "brother({A},{B})",
    "{A} is the father of {B}": "father({A},{B})",
    "{A} and {B} are the parents of {C}": "parent({A},{B},{C})",
    "{A} is a grandfather of {B}": "grandfather({A},{B})",
    "{A},{B} and {C} are children of {D}": "children({A},{B},{C},{D})",
    "{A} is a son of {B}": "son({A},{B})",
    "{A} is an aunt of {B}": "aunt({A},{B})"
}


question_patterns = {
    
    "Are {A} and {B} siblings?": lambda A, B: f"sibling({A.lower()}, {B.lower()})",
    "Is {A} a sister of {B}?": lambda A, B: f"sister({A.lower()}, {B.lower()})",
    "Is {A} a brother of {B}?": lambda A, B: f"brother({A.lower()}, {B.lower()})",
    "Is {A} the mother of {B}?": lambda A, B: f"mother({A.lower()}, {B.lower()})",
    "Is {A} the father of {B}?": lambda A, B: f"father({A.lower()}, {B.lower()})",
    "Are {A} and {B} the parents of {C}?": lambda A, B, C: f"parent({A.lower()}, {C.lower()}) , parent({B.lower()}, {C.lower()})",
    "Is {A} a grandmother of {B}?": lambda A, B: f"grandmother({A.lower()}, {B.lower()})",
    "Is {A} a daughter of {B}?": lambda A, B: f"daughter({A.lower()}, {B.lower()})",
    "Is {A} a son of {B}?": lambda A, B: f"son({A.lower()}, {B.lower()})",
    "Is {A} a child of {B}?": lambda A, B: f"child({A.lower()}, {B.lower()})",
    "Are {A}, {B} and {C} children of {D}?": lambda A, B, C, D: f"child({A.lower()}, {D.lower()}) , child({B.lower()}, {D.lower()}) , child({C.lower()}, {D.lower()})",
    "Is {A} an uncle of {B}?": lambda A, B: f"uncle({A.lower()}, {B.lower()})",
    "Who are the siblings of {A}?": lambda A: f"sibling(X, {A.lower()})",
    "Who are the sisters of {A}?": lambda A: f"sister(X, {A.lower()})",
    "Who are the brothers of {A}?": lambda A: f"brother(X, {A.lower()})",
    "Who is the mother of {A}?": lambda A: f"mother(X, {A.lower()})",
    "Who is the father of {A}?": lambda A: f"father(X, {A.lower()})",
    "Who are the parents of {A}?": lambda A: f"parent(X, {A.lower()})",
    "Is {A} a grandfather of {B}?": lambda A, B: f"grandfather({A.lower()}, {B.lower()})",
    "Who are the daughters of {A}?": lambda A: f"daughter(X, {A.lower()})",
    "Who are the sons of {A}?": lambda A: f"son(X, {A.lower()})",
    "Who are the children of {A}?": lambda A: f"child(X, {A.lower()})",
    "Is {A} an aunt of {B}?": lambda A, B: f"aunt({A.lower()}, {B.lower()})",
    "Are {A} and {B} relatives?": lambda A, B: f"relative({A.lower()}, {B.lower()})"
}



def match_statement(text):
    text = text.strip().lower().rstrip(".,")  # normalize input

    for pattern, logic in statement_patterns.items():
        regex = pattern
        regex = regex.replace("{A}", r"(?P<A>\w+)")
        regex = regex.replace("{B}", r"(?P<B>\w+)")
        regex = regex.replace("{C}", r"(?P<C>\w+)")
        regex = regex.replace("{D}", r"(?P<D>\w+)")

        match = re.fullmatch(regex, text, flags=re.IGNORECASE)
        if match:
            groups = {k: v.lower() for k, v in match.groupdict().items()}

            # Dispatch to correct logic function
            try:
                if "mother(" in logic:
                    return assertz(mother(groups['A'], groups['B']))
                elif "father(" in logic:
                    return assertz(father(groups['A'], groups['B']))
                elif "daughter(" in logic:
                    return assertz(daughter(groups['A'], groups['B']))
                elif "son(" in logic:
                    return assertz(son(groups['A'], groups['B']))
                elif "child(" in logic:
                    return assertz(child(groups['A'], groups['B']))
                elif "sibling(" in logic: 
                    return sibling(groups['A'], groups['B'])   
                elif "brother(" in logic:
                    return assertz(brother(groups['A'], groups['B'])) 
                elif "sister(" in logic:
                    return assertz(sister(groups['A'], groups['B'])) 
                elif "uncle(" in logic:
                    return assertz(uncle(groups['A'], groups['B'])) 
                elif "aunt(" in logic:
                    return assertz(aunt(groups['A'], groups['B'])) 
                elif "grandmother(" in logic:
                    return assertz(grandmother(groups['A'], groups['B'])) 
                elif "grandfather(" in logic:
                    return assertz(grandfather(groups['A'], groups['B'])) 
                elif "children(" in logic:
                    return assertz(children(groups['A'],groups['B'],groups['C'],groups['D']))
                elif "parent(" in logic:
                    return assertz(parent(groups['A'], groups['B'], groups['C']))
            except Exception as e:
                return f"❌ Error while asserting: {e}"

    return "❓ I didn't understand that statement."



def ask_question(text):
    for pattern, query_func in question_patterns.items():
        # Convert human-friendly patterns to regex
        regex = pattern
        regex = regex.replace("{A}", r"(?P<A>\w+)")
        regex = regex.replace("{B}", r"(?P<B>\w+)")
        regex = regex.replace("{C}", r"(?P<C>\w+)")
        regex = regex.replace("{D}", r"(?P<D>\w+)")

        match = re.fullmatch(regex, text.strip(), re.IGNORECASE)
        if match:
            groups = {k: v.lower() for k, v in match.groupdict().items()}
            query = query_func(**groups)

            results = []

            for sub_query in [q.strip() for q in query.split("&&")]:  # use && for chaining multiple checks
                if re.search(r'\bX\b', sub_query):  # retrieve query
                    for solution in prolog.query(sub_query):
                        results.append(solution['X'].capitalize())
                else:  # yes/no query
                    if not list(prolog.query(sub_query)):
                        return "❌ No."

            return f"📋 Answer: {', '.join(results)}" if results else "✅ Yes."

    return "❓ I don't understand the question."



#TO DO: Figure out how to parse sentences and determine which sentences are valid
# Deal with some flaws of implications and with contingencies and contradictions


def process_input(text):
    if text.endswith("?"):
        return ask_question(text)
    else:
        result = match_statement(text)
        if result:
            return result
        else:
            return "I don't understand the statement..."

if __name__ == "__main__":
    print("👨‍👩‍👧 Family Tree Chatbot\nType 'exit' to quit.")
    while True:
        inp = input("🗨️  You: ")
        if inp.lower() == "exit":
            break
        response = process_input(inp)
        print("Bot:", response)
