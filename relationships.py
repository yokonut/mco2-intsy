from pyswip import Prolog
prolog = Prolog()

def assertz(assertions):
    temp_assertions = [] 
    try:
        for fact in assertions:
            existing = list(prolog.query(fact))
            if existing:
                print(f"📌 I already knew: {fact}")
                continue

            prolog.assertz(fact)
            temp_assertions.append(fact)

        return "✅ I've learned something new."

    except Exception as e:
        for fact in temp_assertions:
            prolog.retract(fact)
        return "❌ That's impossible! One or more statements contradict known facts."

def normalize(*args):
    return [a.lower() for a in args]


def mother(A,B):
    A, B = normalize(A,B)
    assertions = []
    assertions.append(f"parent_of({A},{B})")
    assertions.append(f"female({A})")
    return assertions

def father(A,B):
    A, B = normalize(A,B)
    assertions = []
    assertions.append(f"parent_of({A},{B})")
    assertions.append(f"male({A})")
    return assertions

def son(A,B):
    A, B = normalize(A,B)
    assertions = []
    assertions.append(f"parent_of({B},{A})")
    assertions.append(f"male({A})")
    return assertions

def daughter(A,B):
    A, B = normalize(A,B)
    assertions = []
    assertions.append(f"parent_of({B},{A})")
    assertions.append(f"female({A})")
    return assertions

def child(A,B):
    A, B = normalize(A,B)
    assertions = []
    assertions.append(f"parent_of({B},{A})")
    return assertions

def children(A,B,C,D):
    A,B,C,D = normalize(A,B,C,D)
    assertions = []
    assertions.append(f"parent_of({D},{A})")
    assertions.append(f"parent_of({D},{B})")
    assertions.append(f"parent_of({D},{C})")
    return assertions

def sibling(A, B):
    A, B = normalize(A, B)

    query = f"parent_of(X, {A}), parent_of(X, {B}), {A} \\= {B}"
    results = list(prolog.query(query))

    if results:
        print("✅ I already knew they were siblings!")
        return [f"female({A})"]
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
            print("✅ I already knew she was a sister.")
            return []
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
            print("✅ I already knew he was a brother.")
            return []
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
            print("✅ I already knew she was a grandmother.")
            return []
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
        print("✅ I already knew he was a grandfather.")
        return []

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

    # Full condition: A is male and A is a sibling of B's parent
    query = f"parent_of(Z, {B}), parent_of(X, Z), parent_of(X, {A}), male({A}), {A} \\= Z"
    results = list(prolog.query(query))

    if results:
        print("✅ I already knew he was an uncle.")
        return []
    
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

    query = f"parent_of(Z, {B}), parent_of(X, Z), parent_of(X, {A}), female({A}), {A} \\= Z"
    results = list(prolog.query(query))

    if results:
        print("✅ I already knew she was an aunt.")
        return []
    else:
        query_partial = f"parent_of(Z, {B}), parent_of(X, Z), parent_of(X, {A}), {A} \\= Z"
        partial_results = list(prolog.query(query_partial))
        if partial_results:
            return [f"female({A})"]
        else:
            print("❌ I can’t confirm she’s an aunt unless I know who the shared parent and sibling are.")
            return []


