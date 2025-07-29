:- dynamic father/2.
:- dynamic mother/2.
:- dynamic child/2.
:- dynamic grandparent/2.
:- dynamic grandfather/2.
:- dynamic grandmother/2.
:- dynamic sibling/2.
:- dynamic brother/2.
:- dynamic sister/2.
:- dynamic son/2.
:- dynamic daughter/2.
:- dynamic uncle/2.
:- dynamic aunt/2.
:- dynamic parent/2.
:- dynamic male/1.
:- dynamic female/1.
:- dynamic ancestor/2.
:- dynamic relative/2.

father(X, Y) :- male(X), parent(X, Y).
mother(X, Y) :- female(X), parent(X, Y).
child(X, Y) :- parent(Y, X).

grandparent(X, Y) :- parent(X, Z), parent(Z, Y).
grandfather(X, Y) :- male(X), grandparent(X, Y).
grandmother(X, Y) :- female(X), grandparent(X, Y).

sibling(X, Y) :- parent(Z, X), parent(Z, Y), X \= Y.
sibling(X, Y) :- parent(X, Z), aunt(Y, Z).
sibling(X, Y) :- parent(X, Z), uncle(Y, Z).

brother(X, Y) :- male(X), sibling(X, Y).
sister(X, Y) :- female(X), sibling(X, Y).

son(X, Y) :- male(X), child(X, Y).
daughter(X, Y) :- female(X), child(X, Y).

uncle(X, Y) :- parent(P, Y), brother(X, P).
aunt(X, Y) :- parent(P, Y), sister(X, P).

ancestor(X, Y) :- parent(X, Y).
ancestor(X, Y) :- parent(X, Z), ancestor(Z, Y).

relative(X, Y) :- ancestor(X, Y).
relative(X, Y) :- ancestor(Y, X).

relative(X, Y) :- sibling(X, Y).

relative(X, Y) :- parent(X, Y).
relative(X, Y) :- parent(Y, X).

relative(X, Y) :- uncle(X, Y).
relative(X, Y) :- uncle(Y, X).

relative(X, Y) :- aunt(X, Y).
relative(X, Y) :- aunt(Y, X).