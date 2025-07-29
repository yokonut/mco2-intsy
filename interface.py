from pyswip import Prolog
from relationships import prolog, assertz, mother, father, son, daughter, child, children


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
    text = text.strip().lower()

    if " is the mother of " in text:
        A, B = text.split(" is the mother of ")
        assertz(mother(A.strip(), B.strip()))
        return "✅ Got it!"

    elif " is the father of " in text:
        A, B = text.split(" is the father of ")
        assertz(father(A.strip(), B.strip()))
        return "✅ Got it!"

    elif " is the son of " in text:
        A, B = text.split(" is the son of ")
        assertz(son(A.strip(), B.strip()))
        return "✅ Got it!"

    elif " is the daughter of " in text:
        A, B = text.split(" is the daughter of ")
        assertz(daughter(A.strip(), B.strip()))
        return "✅ Got it!"

    elif " is the child of " in text:
        A, B = text.split(" is the child of ")
        assertz(child(A.strip(), B.strip()))
        return "✅ Got it!"

    elif " are children of " in text:
        names, parent = text.split(" are children of ")
        names = names.replace(",", "").split(" and ")
        if len(names) == 3:
            A, B, C = [n.strip() for n in names]
            assertz(children(A, B, C, parent.strip()))
            return "✅ Got it!"
        
    if " is the mother of " in text:
        A, B = text.split(" is the mother of ")
        assertz(mother(A.strip(), B.strip()))
        return "✅ Got it!"

    return None


import re

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
