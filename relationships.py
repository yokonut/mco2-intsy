from pyswip import Prolog
prolog = Prolog()

def assertz(assertions):
    temp_assertions = [] 
    try:
        for fact in assertions:
            print(f"➡️ Asserting: {fact}")  # DEBUG LINE
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
        print(f"❌ That's impossible! One or more statements contradict known facts.\n{e}")


def normalize(A,B):
    return A.lower(), B.lower()

def mother(A,B):
    A,B = normalize(A,B)
    assertions = []
    assertions.append(f"parent_of({A},{B})")
    assertions.append(f"female({A})")
    return assertions

def father(A,B):
    A,B = normalize(A,B)
    assertions = []
    assertions.append(f"parent_of({A},{B})")
    assertions.append(f"male({A})")
    return assertions

def son(A,B):
    A,B = normalize(A,B)
    assertions = []
    assertions.append(f"parent_of({B},{A})")
    assertions.append(f"male({A})")
    return assertions

def daughter(A,B):
    A,B = normalize(A,B)
    assertions = []
    assertions.append(f"parent_of({B},{A})")
    assertions.append(f"female({A})")
    return assertions

def child(A,B):
    A,B = normalize(A,B)
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