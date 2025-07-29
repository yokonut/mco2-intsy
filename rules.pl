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







% General sibling rule from sister/brother
sibling(X, Y) :- sister(X, Y).
sibling(X, Y) :- sister(Y, X).
sibling(X, Y) :- brother(X, Y).
sibling(X, Y) :- brother(Y, X).

% Optionally add symmetry for sibling/2
sibling(X, Y) :- sibling(Y, X).



% Helper predicates for chatbot queries
query_who_mother(Child, X) :- mother_of(X, Child).
query_who_father(Child, X) :- father_of(X, Child).
query_who_siblings(Person, X) :- siblings(Person, X).
query_who_grandfather(Person, X) :- grandfather_of(X, Person).
query_who_grandmother(Person, X) :- grandmother_of(X, Person).
query_who_grandparent(Person, X) :- grandparent_of(X, Person).
query_who_uncle(Person, X) :- uncle_of(X, Person).
query_who_aunt(Person, X) :- aunt_of(X, Person).
query_who_children(Parent, X) :- child_of(X, Parent).



query_mother(X, Y) :- mother_of(X, Y).
query_father(X, Y) :- father_of(X, Y).
query_siblings(X, Y) :- siblings(X, Y).
query_uncle(X, Y) :- uncle_of(X, Y).
query_aunt(X, Y) :- aunt_of(X, Y).
query_brother(X, Y) :- brother_of(X, Y).
query_sister(X, Y) :- sister_of(X, Y).
query_grandparent(X, Y) :- grandparent_of(X, Y).
query_grandmother(X, Y) :- grandmother_of(X, Y).
query_grandfather(X, Y) :- grandfather_of(X, Y).
