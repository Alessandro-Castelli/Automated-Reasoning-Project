% Definizione dei ruoli
role(attaccante; difensore; centrocampista; portiere).

% Definizione delle squadre utilizzando num_squadre dal file di input
team(1..N) :- num_squadre(N).

% Assegnazione di un giocatore a una squadra e a un ruolo
{assigned(P, T, R) : team(T), role(R)} = 1 :- player(P, _, _).

% Il giocatore deve avere uno dei ruoli che preferisce
:- player(P, R1, R2), assigned(P, T, R), R != R1, R != R2.

% Ogni squadra deve avere esattamente un portiere
1 {assigned(P, T, portiere) : player(P, _, _)} 1 :- team(T).

% Ogni squadra deve avere almeno un attaccante, un difensore e un centrocampista
1 {assigned(P, T, attaccante) : player(P, _, _)} :- team(T).
1 {assigned(P, T, difensore) : player(P, _, _)} :- team(T).
1 {assigned(P, T, centrocampista) : player(P, _, _)} :- team(T).

% Vincoli di different_team
:- different_team(P1, P2), assigned(P1, T, _), assigned(P2, T, _).

% Calcolo delle penalità per le configurazioni di squadra
penalty(T, 0) :- 
    team(T),
    #count{P : assigned(P, T, difensore)} == 3, 
    #count{P : assigned(P, T, centrocampista)} == 2, 
    #count{P : assigned(P, T, attaccante)} == 1.

penalty(T, 0) :- 
    team(T),
    #count{P : assigned(P, T, difensore)} == 2, 
    #count{P : assigned(P, T, centrocampista)} == 3, 
    #count{P : assigned(P, T, attaccante)} == 1.

% Penalità non nulle per altre conformazioni
penalty(T, 1) :- 
    team(T),
    not penalty(T, 0).

% Calcolo della penalità totale per tutte le squadre
total_penalty(P) :- 
    P = #sum { P1 : penalty(T, P1), team(T) }.

% Minimizzazione della penalità totale
#minimize { P : total_penalty(P) }.

% Visualizzazione della soluzione
#show assigned/3.
#show total_penalty/1.
