from pyswip import Prolog
prolog = Prolog()


def is_descendant_of(descendant, ancestor):
    try:
        return bool(list(prolog.query(f"ancestor({ancestor.lower()}, {descendant.lower()})")))
    except Exception:
        return False

def are_siblings(name1, name2):
    try:
        result = list(prolog.query(f"siblings({name1.lower()}, {name2.lower()})"))
        return len(result) > 0
    except Exception:
        return False



def creates_cycle(child, parent):
    try:
        
        cycle = list(prolog.query(f"ancestor({child}, {parent})"))
        return bool(cycle)
    except:
        return False


def assertz(assertions):
    temp_assertions = [] 
    messages = []
    try:
        for fact in assertions:
            if not fact.strip():
                continue

            # 🛑 Skip malformed sentences
            if " is " in fact or " of " in fact:
                continue

            # 🧠 Only allow core predicates
            pred_name = fact.split('(')[0]
            if pred_name not in {"parent_of", "male", "female", "mother_of", "father_of"}:
                continue

            # ✅ Already known?
            existing = list(prolog.query(fact))
            if existing:
                messages.append(f"✅ I already knew {fact}.")
                continue

            # 🧠 NEW: Ask Prolog if this fact is invalid
            invalid_check = list(prolog.query(f"invalid({fact.strip()})"))
            if invalid_check:
                return f"❌ That contradicts logic: {fact} is invalid."

            # 🧠 Extra safety for parent_of-style facts
            if fact.startswith(("mother_of(", "father_of(", "parent_of(")):
                inner = fact[fact.index('(')+1:fact.index(')')]
                parent, child = [x.strip() for x in inner.split(',')]

                if parent == child:
                    return f"❌ That contradicts logic: someone cannot be their own parent."

                if are_siblings(parent, child):
                    return f"❌ That contradicts known facts: {parent} and {child} are siblings, so one can't be the parent of the other."

                if is_descendant_of(parent, child):
                    return f"❌ That contradicts known facts: {parent} is a descendant of {child}, so can't be their parent."

                if creates_cycle(child, parent):
                    return f"❌ That creates an impossible cycle: {parent} cannot be both ancestor and descendant of {child}."

            # ✅ Passes all checks → assert
            prolog.assertz(fact)
            temp_assertions.append(fact)

        if temp_assertions:
            messages.append("✅ I've learned something new.")
        else:
            messages.append("🤔 No new information was added.")
        
        return "\n".join(messages) if messages else ""

    except Exception as e:
        # Roll back any partially added facts
        for fact in temp_assertions:
            prolog.retract(fact)
        return f"❌ That's impossible! One or more statements contradict known facts.\n⚠️ {e}"





def normalize(*args):
    return [a.lower() for a in args]


def mother(A,B):
    A, B = normalize(A,B)
    
    if list(prolog.query(f"parent_of({B}, {A})")):
        return "❌ Contradiction: Can't be mother and child."
    
    assertions = []
    assertions.append(f"parent_of({A},{B})")
    assertions.append(f"female({A})")
    return assertions

def father(A,B):
    A, B = normalize(A,B)
    
    if list(prolog.query(f"parent_of({B}, {A})")):
        return "❌ Contradiction: Can't be father and child."
    
    assertions = []
    assertions.append(f"parent_of({A},{B})")
    assertions.append(f"male({A})")
    return assertions

def son(A,B):
    A, B = normalize(A,B)
    
    if list(prolog.query(f"parent_of({A}, {B})")):
        return "❌ Contradiction: Can't be son and parent."
    
    assertions = []
    assertions.append(f"parent_of({B},{A})")
    assertions.append(f"male({A})")
    return assertions

def daughter(A,B):
    A, B = normalize(A,B)
    
    if list(prolog.query(f"parent_of({A}, {B})")):
        return "❌ Contradiction: Can't be daughter and parent."
    
    assertions = []
    assertions.append(f"parent_of({B},{A})")
    assertions.append(f"female({A})")
    return assertions

def child(A,B):
    A, B = normalize(A,B)
    
    if list(prolog.query(f"parent_of({A},{B})")):
        return "❌ Contradiction: Can't be child and parent."
    
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
        return f"✅ I already knew they were siblings!"
    else:
        return f"❌ I can't confirm that unless I know who their shared parent is."

def sister(A, B):
    A, B = normalize(A, B)
    
    query = f"parent_of(X, {A}), parent_of(X, {B}), {A} \\= {B}"
    results = list(prolog.query(query))

    if results:
        is_female = list(prolog.query(f"female({A})"))
        if is_female:
            return f"✅ I already knew she was a sister."
        else:
            return [f"female({A})"]
    else:
        return f"❌ I can't confirm she's a sister unless I know a shared parent."


def brother(A, B):
    A, B = normalize(A, B)

    query = f"parent_of(X, {A}), parent_of(X, {B}), {A} \\= {B}"
    results = list(prolog.query(query))

    if results:
        is_male = list(prolog.query(f"male({A})"))
        if is_male:
            return f"✅ I already knew he was a brother."
        else:
            return [f"male({A})"]
    else:
        return f"❌ I can't confirm he's a brother unless I know a shared parent."


def grandmother(A, B):
    A, B = normalize(A, B)

    query = f"parent_of({A}, Z), parent_of(Z, {B})"
    results = list(prolog.query(query))

    if results:
        is_female = list(prolog.query(f"female({A})"))
        if is_female:
            return f"✅ I already knew she was a grandmother."
        else:
            return [f"female({A})"]
    else:
        return f"❌ I can't confirm she's a grandmother unless I know the parent and grandparent links."

def grandfather(A, B):
    A, B = normalize(A, B)

    
    query = f"parent_of({A}, Z), parent_of(Z, {B}), male({A})"
    results = list(prolog.query(query))

    if results:
        return f"✅ I already knew he was a grandfather."

    
    partial_query = f"parent_of({A}, Z), parent_of(Z, {B})"
    partial_results = list(prolog.query(partial_query))

    if partial_results:
        return [f"male({A})"]
    else:
        return f"❌ I can't confirm he's a grandfather unless I know the parent and grandparent links."



def uncle(A, B):
    A, B = normalize(A, B)

    
    query = f"parent_of(Z, {B}), parent_of(X, Z), parent_of(X, {A}), male({A}), {A} \\= Z"
    results = list(prolog.query(query))

    if results:
        return f"✅ I already knew he was an uncle."
    
    
    query_partial = f"parent_of(Z, {B}), parent_of(X, Z), parent_of(X, {A}), {A} \\= Z"
    partial_results = list(prolog.query(query_partial))

    if partial_results:
        return [f"male({A})"]
    else:
        return f"❌ I can't confirm he's an uncle unless I know who the shared parent and sibling are."

    
def aunt(A, B):
    A, B = normalize(A, B)

    query = f"parent_of(Z, {B}), parent_of(X, Z), parent_of(X, {A}), female({A}), {A} \\= Z"
    results = list(prolog.query(query))

    if results:
        return f"✅ I already knew she was an aunt."
    else:
        query_partial = f"parent_of(Z, {B}), parent_of(X, Z), parent_of(X, {A}), {A} \\= Z"
        partial_results = list(prolog.query(query_partial))
        if partial_results:
            return [f"female({A})"]
        else:
            return f"❌ I can't confirm she's an aunt unless I know who the shared parent and sibling are."


def parent(A, B, C):
    A, B, C = normalize(A, B, C)
    
    if A == B:
        return f"❌ Parents must be different individuals."
    
    assertions = []
    assertions.append(f"parent_of({A}, {C})")
    assertions.append(f"parent_of({B}, {C})")
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
    return f"relatives({A}, {B})"


def infer_and_assert_siblings_from_parent(parent):
    try:
        children = [res["X"] for res in prolog.query(f"parent_of({parent}, X)")]
        for i in range(len(children)):
            for j in range(i+1, len(children)):
                a = children[i]
                b = children[j]
                try:
                    prolog.assertz(f"siblings({a}, {b})")
                    prolog.assertz(f"siblings({b}, {a})")
                except:
                    pass
    except Exception as e:
        return f"⚠️ Failed to infer siblings from parent {parent}: {e}"



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
