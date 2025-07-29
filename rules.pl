%Declaring predicates as dynamic
:- dynamic parent_of/2.
:- dynamic child_of/2.
:- dynamic father_of/2.
:- dynamic mother_of/2.
:- dynamic son_of/2.
:- dynamic daughter_of/2.
:- dynamic grandparent_of/2.
:- dynamic grandfather_of/2.
:- dynamic grandmother_of/2.
:- dynamic grandson_of/2.
:- dynamic granddaughter_of/2.
:- dynamic siblings/2.
:- dynamic brother_of/2.
:- dynamic sister_of/2.
:- dynamic uncle_of/2.
:- dynamic aunt_of/2.
:- dynamic nephew_of/2.
:- dynamic niece_of/2.
:- dynamic male/1.
:- dynamic female/1.

%Relationship Rules
child_of(X,Y) :- parent_of(Y,X),
    X \= Y.

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

relatives(X,Y) :- siblings(X,Y).

relatives(X,Y) :- parent_of(X,Y).

relatives(X,Y) :- parent_of(Y,X).

relatives(X,Y) :- grandparent_of(X,Y).

relatives(X,Y) :- grandparent_of(Y,X).

