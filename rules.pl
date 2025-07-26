%Male or Female
male(X) :- brother(X).
male(X) :- father(X).
male(X) :- grandfather(X).
male(X) :- son(X).
male(X) :- grandson(X).
male(X) :- uncle(X).
male(X) :- nephew(X).
female(X) :- sister(X).
female(X) :- mother(X).
female(X) :- grandmother(X).
female(X) :- granddaughter(X).
female(X) :- daughter(X).
female(X) :- aunt(X).
female(X) :- niece(X).

%Relationship Rules
parent_of(X,Y) :- child_of(Y,X).

son(X) :- male(X),
    child_of(Y,X).

father_of(X,Y) :- male(X), 
    parent_of(X,Y).

mother_of(X,Y) :- female(X),
    parent_of(X,Y).

grandfather_of(X,Y) :- male(X),
    parent_of(X,Z),
    parent_of(Z,Y).

grandmother_of(X,Y) :- female(X),
    parent_of(X,Z),
    parent_of(Z,Y).

siblings(X,Y) :- parent_of(Z,X),
    parent_of(Z,Y).

sister_of(X,Y) :- female(X),
    siblings(X,Y).

brother_of(X,Y) :- male(X),
    siblings(X,Y).
