from pyswip import Prolog
prolog = Prolog()

def assertz(assertions):
    temp_assertions = [] 
    try:
        for fact in assertions:
            if not fact.strip():  # Skip empty facts
                continue

            existing = list(prolog.query(fact))
            if existing:
                print(f"📌 I already knew: {fact}")
                continue

            prolog.assertz(fact)
            temp_assertions.append(fact)

        if temp_assertions:
            return "✅ I've learned something new."
        else:
            return "🤔 No new information was added."

    except Exception as e:
        for fact in temp_assertions:
            prolog.retract(fact)
        return "❌ That's impossible! One or more statements contradict known facts."


def normalize(*args):
    return [a.lower() for a in args]


def mother(A,B):
    A, B = normalize(A,B)
    
    if list(prolog.query(f"parent_of({B}, {A})")):
        print("❌ Contradiction: Can't be mother and child.")
        return []
    
    if list(prolog.query(f"male({A})")):
        print("❌ Contradiction: A male cannot be a mother.")
        return []
    
    assertions = []
    assertions.append(f"parent_of({A},{B})")
    assertions.append(f"female({A})")
    return assertions

def father(A,B):
    A, B = normalize(A,B)
    
    if list(prolog.query(f"parent_of({B}, {A})")):
        print("❌ Contradiction: Can't be father and child.")
        return []
    
    if list(prolog.query(f"female({A})")):
        print("❌ Contradiction: A female cannot be a father.")
        return []
    
    assertions = []
    assertions.append(f"parent_of({A},{B})")
    assertions.append(f"male({A})")
    return assertions

def son(A,B):
    A, B = normalize(A,B)
    
    if list(prolog.query(f"parent_of({A}, {B})")):
        print("❌ Contradiction: Can't be son and parent.")
        return []
    
    if list(prolog.query(f"female({A})")):
        print("❌ Contradiction: A female cannot be a son.")
        return []
    
    assertions = []
    assertions.append(f"parent_of({B},{A})")
    assertions.append(f"male({A})")
    return assertions

def daughter(A,B):
    A, B = normalize(A,B)
    
    if list(prolog.query(f"parent_of({A}, {B})")):
        print("❌ Contradiction: Can't be daughter and parent.")
        return []
    
    if list(prolog.query(f"male({A})")):
        print("❌ Contradiction: A male cannot be a daughter.")
        return []
    
    assertions = []
    assertions.append(f"parent_of({B},{A})")
    assertions.append(f"female({A})")
    return assertions

def child(A,B):
    A, B = normalize(A,B)
    
    if list(prolog.query(f"parent_of({A},{B})")):
        print("❌ Contradiction: Can't be child and parent.")
        return []
    
    assertions = []
    assertions.append(f"parent_of({B},{A})")
    return assertions

def children(A, B, C, D):
    A, B, C, D = normalize(A, B, C, D)

    if len({A, B, C}) < 3:
        print("❌ Contradiction: All three children must be distinct.")
        return []

    if D in {A, B, C}:
        print("❌ Contradiction: A person cannot be their own child.")
        return []

    # Check for child-parent reversals
    for child in [A, B, C]:
        if list(prolog.query(f"parent_of({child}, {D})")):
            print(f"❌ Contradiction: {child} cannot be a parent of {D}.")
            return []

    assertions = [
        f"parent_of({D}, {A})",
        f"parent_of({D}, {B})",
        f"parent_of({D}, {C})"
    ]
    return assertions


def sibling(A, B):
    A, B = normalize(A, B)

    query = f"parent_of(X, {A}), parent_of(X, {B}), {A} \\= {B}"
    results = list(prolog.query(query))

    if results:
        return "✅ I already knew they were siblings!"
    else:
        print("❌ I can’t confirm that unless I know who their shared parent is.")
        return []

def sister(A, B):
    A, B = normalize(A, B)
    
    query = f"parent_of(X, {A}), parent_of(X, {B}), {A} \\= {B}"
    results = list(prolog.query(query))

    if results:
        is_female = list(prolog.query(f"female({A})"))
        if is_female:
            return "✅ I already knew she was a sister."
        else:
            return [f"female({A})"]
    else:
        print("❌ I can’t confirm she’s a sister unless I know a shared parent.")
        return []


def brother(A, B):
    A, B = normalize(A, B)

    query = f"parent_of(X, {A}), parent_of(X, {B}), {A} \\= {B}"
    results = list(prolog.query(query))

    if results:
        is_male = list(prolog.query(f"male({A})"))
        if is_male:
            return "✅ I already knew he was a brother."
        else:
            return [f"male({A})"]
    else:
        print("❌ I can’t confirm he’s a brother unless I know a shared parent.")
        return []


def grandmother(A, B):
    A, B = normalize(A, B)

    query = f"parent_of({A}, Z), parent_of(Z, {B})"
    results = list(prolog.query(query))

    if results:
        is_female = list(prolog.query(f"female({A})"))
        if is_female:
            return "✅ I already knew she was a grandmother."
        else:
            return [f"female({A})"]
    else:
        print("❌ I can’t confirm she’s a grandmother unless I know the parent and grandparent links.")
        return []

def grandfather(A, B):
    A, B = normalize(A, B)

    # Check if A is already known to be a grandfather of B
    query = f"parent_of({A}, Z), parent_of(Z, {B}), male({A})"
    results = list(prolog.query(query))

    if results:
        return "✅ I already knew he was a grandfather."

    # Check if the parent-child chain is known (A → Z → B), but male(A) is not known
    partial_query = f"parent_of({A}, Z), parent_of(Z, {B})"
    partial_results = list(prolog.query(partial_query))

    if partial_results:
        return [f"male({A})"]
    else:
        print("❌ I can’t confirm he’s a grandfather unless I know the parent and grandparent links.")
        return []



def uncle(A, B):
    A, B = normalize(A, B)
    
    if list(prolog.query(f"female({A})")):
        print("❌ Contradiction: A female cannot be an uncle.")
        return []

    # Full condition: A is male and A is a sibling of B's parent
    query = f"parent_of(Z, {B}), parent_of(X, Z), parent_of(X, {A}), male({A}), {A} \\= Z"
    results = list(prolog.query(query))
    
    
    if results:
        return "✅ I already knew he was an uncle."
    
    # Partial check: shared parent with B's parent (sibling of parent)
    query_partial = f"parent_of(Z, {B}), parent_of(X, Z), parent_of(X, {A}), {A} \\= Z"
    partial_results = list(prolog.query(query_partial))

    if partial_results:
        return [f"male({A})"]
    else:
        print("❌ I can’t confirm he’s an uncle unless I know who the shared parent and sibling are.")
        return []

    
def aunt(A, B):
    A, B = normalize(A, B)
    
    if list(prolog.query(f"male({A})")):
        print("❌ Contradiction: A male cannot be an aunt.")
        return []

    query = f"parent_of(Z, {B}), parent_of(X, Z), parent_of(X, {A}), female({A}), {A} \\= Z"
    results = list(prolog.query(query))

    if results:
        return "✅ I already knew she was an aunt."
    else:
        query_partial = f"parent_of(Z, {B}), parent_of(X, Z), parent_of(X, {A}), {A} \\= Z"
        partial_results = list(prolog.query(query_partial))
        if partial_results:
            return [f"female({A})"]
        else:
            print("❌ I can’t confirm she’s an aunt unless I know who the shared parent and sibling are.")
            return []


def parent(A, B, C):
    A, B, C = normalize(A, B, C)

    if A == B:
        print("❌ Contradiction: Parents must be two different individuals.")
        return []

    if C == A or C == B:
        print("❌ Contradiction: A person cannot be their own child.")
        return []

    if list(prolog.query(f"parent_of({C}, {A})")) or list(prolog.query(f"parent_of({C}, {B})")):
        print("❌ Contradiction: A child cannot be a parent of their own parent.")
        return []

    assertions = [
        f"parent_of({A}, {C})",
        f"parent_of({B}, {C})"
    ]
    return assertions





## QUERY FUNCTIONS

def query_sibling(A, B):
    return f"parent_of(X, {A}), parent_of(X, {B}), {A} \\= {B}"

def query_sister(A, B):
    return f"parent_of(X, {A}), parent_of(X, {B}), female({A}), {A} \\= {B}"

def query_brother(A, B):
    return f"parent_of(X, {A}), parent_of(X, {B}), male({A}), {A} \\= {B}"

def query_mother(A, B):
    return f"parent_of({A}, {B}), female({A})"

def query_father(A, B):
    return f"parent_of({A}, {B}), male({A})"

def query_parents_of(A, B, C):
    return f"parent_of({A}, {C}), parent_of({B}, {C})"

def query_grandmother(A, B):
    return f"parent_of({A}, X), parent_of(X, {B}), female({A})"

def query_grandfather(A, B):
    return f"parent_of({A}, X), parent_of(X, {B}), male({A})"

def query_daughter(A, B):
    return f"parent_of({B}, {A}), female({A})"

def query_son(A, B):
    return f"parent_of({B}, {A}), male({A})"

def query_child(A, B):
    return f"parent_of({B}, {A})"

def query_children_of(A, B, C, D):
    return f"parent_of({D}, {A}), parent_of({D}, {B}), parent_of({D}, {C})"

def query_uncle(A, B):
    return f"parent_of(Z, {B}), parent_of(X, Z), parent_of(X, {A}), male({A}), {A} \\= Z"

def query_aunt(A, B):
    return f"parent_of(Z, {B}), parent_of(X, Z), parent_of(X, {A}), female({A}), {A} \\= Z"

def query_relative(A, B):
    return f"related({A}, {B})"



def query_who_siblings(A):
    return f"parent_of(X, {A}), parent_of(X, Y), {A} \\= Y"

def query_who_sisters(A):
    return f"parent_of(X, {A}), parent_of(X, Y), female(Y), {A} \\= Y"

def query_who_brothers(A):
    return f"parent_of(X, {A}), parent_of(X, Y), male(Y), {A} \\= Y"

def query_who_mother(A):
    return f"parent_of(X, {A}), female(X)"

def query_who_father(A):
    return f"parent_of(X, {A}), male(X)"

def query_who_parents(A):
    return f"parent_of(X, {A})"

def query_who_daughters(A):
    return f"parent_of({A}, X), female(X)"

def query_who_sons(A):
    return f"parent_of({A}, X), male(X)"

def query_who_children(A):
    return f"parent_of({A}, X)"
