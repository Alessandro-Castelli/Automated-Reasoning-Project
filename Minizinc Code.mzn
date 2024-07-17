% Numero di giocatori (da file di input)
int: n;
% Numero di squadre (da file di input)
int: k;
% Ruoli
enum Role = {g, d, m, f};  % g=portiere, d=difensore, m=centrocampista, f= attaccante

% Giocatori e le loro opzioni di ruolo (da file di input)
array[1..n] of set of Role: roles;

% Quale giocatore va in quale squadra
array[1..n] of var 1..k: team;

% Ruolo assegnato a ciascun giocatore
array[1..n] of var Role: assigned_role;

% Requisiti per ogni squadra
constraint
    forall(t in 1..k) (
        % Ogni squadra deve avere esattamente un portiere
        sum([assigned_role[j] == g | j in 1..n where team[j] == t]) == 1 /\
        % Almeno un difensore
        sum([assigned_role[j] == d | j in 1..n where team[j] == t]) >= 1 /\
        % Almeno un centrocampista
        sum([assigned_role[j] == m | j in 1..n where team[j] == t]) >= 1 /\
        % Almeno un attaccante
        sum([assigned_role[j] == f | j in 1..n where team[j] == t]) >= 1
    );

% Ogni giocatore deve essere assegnato a uno dei suoi ruoli scelti
constraint
    forall(i in 1..n) (
        assigned_role[i] in roles[i]
    );

% Vincoli per i giocatori che devono essere in squadre diverse
int: num_pairs; % Numero di coppie di giocatori che devono essere in squadre diverse
array[1..num_pairs] of int: player1;
array[1..num_pairs] of int: player2;
constraint

    forall(i in 1..num_pairs) (
        team[player1[i]] != team[player2[i]]
    );

% Calcolo delle penalità per ogni squadra
array[1..k] of var 0..2: penalties;
constraint
    forall(t in 1..k) (
        let {
            var int: d_count = sum([assigned_role[j] == d | j in 1..n where team[j] == t]),
            var int: m_count = sum([assigned_role[j] == m | j in 1..n where team[j] == t]),
            var int: f_count = sum([assigned_role[j] == f | j in 1..n where team[j] == t])
        } in
        if d_count == 3 /\ m_count == 2 /\ f_count == 1 then
            penalties[t] = 0
        elseif d_count == 2 /\ m_count == 3 /\ f_count == 1 then
            penalties[t] = 0
        else
            penalties[t] = 1
        endif
    );

% Funzione obiettivo: minimizzare la somma delle penalità
var int: total_penalty = sum(penalties);

solve minimize total_penalty;
% Output del risultato
output [
    % Dettagli delle penalità per ogni squadra
    "Penalties per team:\n"
] ++ [
    show(t) ++ ": Penalty " ++ show(penalties[t]) ++ "\n" | t in 1..k
] ++ [
    "Total penalty: " ++ show(total_penalty) ++ "\n" ++ "-------------" ++ "\n" ++
    "Teams:\n"
] ++ [
    "Player " ++ show(i) ++ ": Team " ++ show(team[i]) ++ ", Role: " ++ show(assigned_role[i]) ++ "\n" | i in 1..n
];

