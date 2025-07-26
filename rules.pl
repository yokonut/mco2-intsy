%Male or Female
male(X) :- brother_of(X,_).
male(X) :- father_of(X,_).
male(X) :- grandfather_of(X,_).
male(X) :- son_of(X,_).
male(X) :- grandson_of(X,_).
male(X) :- uncle_of(X,_).
male(X) :- nephew_of(X,_).
female(X) :- sister_of(X,_).
female(X) :- mother_of(X,_).
female(X) :- grandmother_of(X,_).
female(X) :- granddaughter_of(X,_).
female(X) :- daughter_of(X,_).
female(X) :- aunt_of(X,_).
female(X) :- niece_of(X,_).

%Relationship Rules
parent_of(X,Y) :- child_of(Y,X),
    X\=Y.

son_of(X,Y) :- male(X),
    parent_of(Y,X).

daughter_of(X,Y) :- female(X),
    parent_of(Y,X).

father_of(X,Y) :- male(X), 
    parent_of(X,Y).

mother_of(X,Y) :- female(X),
    parent_of(X,Y).

grandparent_of(X,Y) :- parent_of(X,Z),
    parent_of(Z,Y).

grandfather_of(X,Y) :- male(X),
    grandparent_of(X,Y).

grandmother_of(X,Y) :- female(X),
    grandparent_of(X,Y).

grandson_of(X,Y) :- male(X),
    grandparent_of(Y,X).

granddaughter_of(X,Y) :- female(X),
    grandparent_of(Y,X).

siblings(X,Y) :- parent_of(Z,X),
    parent_of(Z,Y),
    X \= Y.

sister_of(X,Y) :- female(X),
    siblings(X,Y).

brother_of(X,Y) :- male(X),
    siblings(X,Y).

uncle_of(X,Y) :- male(X),
    parent_of(Z,Y),
    brother_of(X,Z).

aunt_of(X,Y) :- female(X),
    parent_of(Z,Y),
    sister_of(X,Z).

nephew_of(X,Y) :- male(X),
    (uncle_of(Y,X) ; aunt_of(Y,X)).

niece_of(X,Y) :- female(X),
    (uncle_of(Y,X) ; aunt_of(Y,X)).

    
%From main program
