from pyswip import Prolog

prolog = Prolog()


knowledge_base = []


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
    # Left column: Yes/No and WH-questions
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

    # Right column: WH-questions
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



def match_statement(sentence):
    for template, fact_format in statement_patterns.items():
        placeholders = [ph for ph in ("{A}", "{B}", "{C}") if ph in template]
        temp = template
        for ph in placeholders:
            temp = temp.replace(ph, "{}")
        parts = temp.split("{}")

        working = sentence
        for part in parts:
            working = working.replace(part, "§", 1)
        args = [x.strip() for x in working.split("§") if x.strip()]

        if len(args) == len(placeholders):
            values = dict(zip(["A", "B", "C"], args))
            fact_code = fact_format.format(**values)
            for fact in fact_code.split("\n"):
                fact = fact.lower()
                if fact not in knowledge_base:
                    knowledge_base.append(fact)
                    prolog.assertz(fact)
            return f"Oh OKAY! I'm taking down notes.. "
    return None



def ask_question(question):
    for template, builder in question_patterns.items():
        # Support up to {D}
        placeholders = [ph for ph in ("{A}", "{B}", "{C}", "{D}") if ph in template]
        temp = template
        for ph in placeholders:
            temp = temp.replace(ph, "{}")
        parts = temp.split("{}")

        working = question
        for part in parts:
            working = working.replace(part, "§", 1)
        args = [x.strip() for x in working.split("§") if x.strip()]
        if len(args) == len(placeholders):
            query = builder(*args)
            results = list(prolog.query(query))
            if "X" in query:
                return [r["X"] for r in results] or "No results"
            return "Yes!!" if results else "No I don't think so.."
    return "I don't understand the question..."


def process_input(text):
    if text.endswith("?"):
        return ask_question(text)
    else:
        result = match_statement(text)
        if result:
            return result
        else:
            return "I don't understand the statement..."

# --- 6. Sample runs
print(process_input("Yohans is the father of Siu."))
print(process_input("Michelle is the mother of Siu."))
print(process_input("Yohan and Siu are siblings."))
print(process_input("Is Yohan the father of Siu?"))  
print(process_input("Is Michelle the mother of Siu?"))       

print("👋 Family Relationship Bot (type 'exit' to quit)\n")

while True:
    user_input = input("🧠 Enter a sentence or question: ").strip()
    
    if user_input.lower() in {"exit", "quit"}:
        print("👋 Goodbye!")
        break

    response = process_input(user_input)
    print("🔍", response)
