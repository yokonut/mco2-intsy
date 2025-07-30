#!/usr/bin/env python3
"""
Test script to verify the fixes for the three issues
"""

from interface import handle_user_input, family
from relationships import *

def reset_knowledge_base():
    """Reset the knowledge base"""
    family.retractall("male(_)")
    family.retractall("female(_)")
    family.retractall("parent_of(_, _)")
    family.retractall("siblings(_, _)")

print("=== Testing the Three Fixes ===")

# Fix 1: Test sibling relationship
print("\n1. Testing sibling relationship (should return ✅ Yes):")
reset_knowledge_base()
family.assertz("male(jerry)")
family.assertz("male(mike)")
family.assertz("female(emma)")
family.assertz("parent_of(john, jerry)")
family.assertz("parent_of(john, mike)")
family.assertz("parent_of(john, emma)")

response = handle_user_input("Are Jerry and Mike siblings?")
print(f"   Input: Are Jerry and Mike siblings?")
print(f"   Response: {response}")

# Fix 2: Test contradiction detection
print("\n2. Testing contradiction detection (should return ❌ Contradiction):")
reset_knowledge_base()
family.assertz("male(charlie)")
family.assertz("female(diana)")
family.assertz("parent_of(charlie, diana)")

response = handle_user_input("Diana is the mother of Charlie")
print(f"   Input: Diana is the mother of Charlie")
print(f"   Response: {response}")

# Fix 3: Test WHO question with deduplication
print("\n3. Testing WHO question deduplication (should not have duplicates):")
reset_knowledge_base()
family.assertz("male(jerry)")
family.assertz("male(mike)")
family.assertz("female(emma)")
family.assertz("parent_of(john, jerry)")
family.assertz("parent_of(john, mike)")
family.assertz("parent_of(john, emma)")

response = handle_user_input("Who are the siblings of Jerry?")
print(f"   Input: Who are the siblings of Jerry?")
print(f"   Response: {response}")

print("\n=== Fix Verification Complete ===")
print("✅ All three issues should now be resolved!") 