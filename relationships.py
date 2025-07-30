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

        print("✅ I've learned something new.")

    except Exception as e:
        for fact in temp_assertions:
            prolog.retract(fact)
        print("❌ That's impossible! One or more statements contradict known facts.")

def normalize(*args):
    return [a.lower() for a in args]


def mother(A,B):
    A, B = normalize(A,B)
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
    normalize(A,B,C,D)
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
        return []
    else:
        print("❌ I can’t confirm that unless I know who their shared parent is.")
        return []

def sister(A, B):
    A, B = normalize(A, B)
    
    query = f"parent_of(X, {A}), parent_of(X, {B}), {A} \\= {B}"
    results = list(prolog.query(query))

    if results:
        assertions = [f"female({A})"]
        return assertions
    else:
        print("❌ I can’t confirm she’s a sister unless I know a shared parent.")
        return []

def brother(A, B):
    A, B = normalize(A, B)

    query = f"parent_of(X, {A}), parent_of(X, {B}), {A} \\= {B}"
    results = list(prolog.query(query))

    if results:
        assertions = [f"male({A})"]
        return assertions
    else:
        print("❌ I can’t confirm he’s a brother unless I know a shared parent.")
        return []
    
def grandfather(A, B):
    A, B = normalize(A, B)
    assertions = []

    query = f"parent_of({A}, Z), parent_of(Z, {B})"
    results = list(prolog.query(query))

    if results:
        assertions.append(f"male({A})")
        return assertions
    else:
        print("❌ I can’t confirm he’s a grandfather unless I know the parent and grandparent links.")
        return []

def grandmother(A, B):
    A, B = normalize(A, B)
    assertions = []

    query = f"parent_of({A}, Z), parent_of(Z, {B})"
    results = list(prolog.query(query))

    if results:
        assertions.append(f"female({A})")
        return assertions
    else:
        print("❌ I can’t confirm she’s a grandmother unless I know the parent and grandparent links.")
        return []
    

def uncle(A, B):
    A, B = normalize(A, B)
    assertions = []

    query = f"parent_of(Z, {B}), brother_of({A}, Z)"
    results = list(prolog.query(query))

    if results:
        assertions.append(f"male({A})")
        return assertions
    else:
        print("❌ I can’t confirm he’s an uncle unless I know who the shared parent and sibling are.")
        return []

def aunt(A, B):
    A, B = normalize(A, B)
    assertions = []

    query = f"parent_of(Z, {B}), sister_of({A}, Z)"
    results = list(prolog.query(query))

    if results:
        assertions.append(f"female({A})")
        return assertions
    else:
        print("❌ I can’t confirm she’s an aunt unless I know who the shared parent and sibling are.")
        return []
  

