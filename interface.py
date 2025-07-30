from pyswip import Prolog
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

def parse_relationship_statement(user_input):
    """Parse user input and return appropriate response based on relationships"""
    user_input = user_input.lower().strip()
    
    # Check for common relationship queries
    if "is" in user_input and "of" in user_input:
        # Extract names and relationship
        parts = user_input.split()
        
        # Look for relationship keywords
        relationship_keywords = {
            "son": "son_of",
            "daughter": "daughter_of", 
            "father": "father_of",
            "mother": "mother_of",
            "grandfather": "grandfather_of",
            "grandmother": "grandmother_of",
            "brother": "brother_of",
            "sister": "sister_of",
            "uncle": "uncle_of",
            "aunt": "aunt_of",
            "nephew": "nephew_of",
            "niece": "niece_of"
        }
        
        for keyword, predicate in relationship_keywords.items():
            if keyword in user_input:
                # Try to extract names (simple approach)
                names = re.findall(r'\b[a-zA-Z]+\b', user_input)
                if len(names) >= 2:
                    # Find the two main names (skip common words)
                    common_words = {"is", "a", "an", "the", "of", "and", "are", "siblings"}
                    main_names = [name for name in names if name.lower() not in common_words]
                    
                    if len(main_names) >= 2:
                        person1, person2 = main_names[0], main_names[1]
                        
                        # Query the relationship
                        try:
                            results = list(family.query(f"{predicate}({person1.lower()}, {person2.lower()})"))
                            if results:
                                return f"Yes, {person1} is a {keyword} of {person2}."
                            else:
                                return f"No, {person1} is not a {keyword} of {person2}."
                        except:
                            return f"I'm not sure about the relationship between {person1} and {person2}."
    
    # Check for sibling relationships
    if "siblings" in user_input or "sibling" in user_input:
        names = re.findall(r'\b[a-zA-Z]+\b', user_input)
        common_words = {"are", "and", "siblings", "sibling"}
        main_names = [name for name in names if name.lower() not in common_words]
        
        if len(main_names) >= 2:
            person1, person2 = main_names[0], main_names[1]
            try:
                results = list(family.query(f"siblings({person1.lower()}, {person2.lower()})"))
                if results:
                    return f"Yes, {person1} and {person2} are siblings."
                else:
                    return f"No, {person1} and {person2} are not siblings."
            except:
                return f"I'm not sure about the relationship between {person1} and {person2}."
    
    # Check for parent relationships
    if "parent" in user_input:
        names = re.findall(r'\b[a-zA-Z]+\b', user_input)
        common_words = {"is", "a", "the", "parent", "of"}
        main_names = [name for name in names if name.lower() not in common_words]
        
        if len(main_names) >= 2:
            person1, person2 = main_names[0], main_names[1]
            try:
                results = list(family.query(f"parent_of({person1.lower()}, {person2.lower()})"))
                if results:
                    return f"Yes, {person1} is a parent of {person2}."
                else:
                    return f"No, {person1} is not a parent of {person2}."
            except:
                return f"I'm not sure about the relationship between {person1} and {person2}."
    
    return None  # No relationship pattern matched

# Initialize with some sample data
family.retractall("male(_)")
family.retractall("female(_)")
family.retractall("parent_of(_, _)")

# Add some sample family data
family.assertz("male(jerry)")
family.assertz("male(ben)")
family.assertz("female(sarah)")
family.assertz("female(emma)")
family.assertz("parent_of(ben, jerry)")
family.assertz("parent_of(sarah, jerry)")
family.assertz("parent_of(ben, emma)")
family.assertz("parent_of(sarah, emma)")

results = list(family.query("son_of(jerry, X)"))
print("son_of():", results)
print("Result is:", "True" if results else "False")
    