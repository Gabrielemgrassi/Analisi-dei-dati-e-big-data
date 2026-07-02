-- Lista Esami dati da uno studente
SELECT Nome_studente, Cognome_studente, Studenti.Matricola, Voto, Lode, Data_esame
FROM Studenti
JOIN Sostiene
ON Studenti.Matricola = Sostiene.Matricola
WHERE Nome_studente = 'Leonardo' AND Cognome_studente = 'Rossi';

-- Totale di studenti iscritti divisi per Cdl
SELECT Nome_corso, COUNT(Matricola) as Totale
FROM Iscritto_A
JOIN Cdl
ON Iscritto_A.Codice_corso = Cdl.Codice_corso 
GROUP BY Nome_corso
ORDER BY Totale DESC

--Docente più severo agli esami, sulla base della media aritmetica di tutti gli studenti che lo hanno superato
SELECT Nome_docente, Cognome_docente , Nome_insegnamento, Email_istituzionale , AVG(Voto) As Media_Esame
FROM Docenti
JOIN Insegnamento
ON Docenti.Codice_docente = Insegnamento.Codice_docente 
JOIN Sostiene
ON Insegnamento.Codice_insegnamento = Sostiene.Codice_insegnamento 
GROUP BY Sostiene.Codice_insegnamento
ORDER BY Media_esame ASC
LIMIT 1

/*
Un nuovo bando, permette a degli studenti di riceve una borsa di studio pari a €2.500.
I requisiti sono quelli di :
- essere uno studente iscritto al primo anno della facolta di Ingegneria civile 
- avere un\' età pari o superiore ad anni 30
*/
Gli studenti che rispettano i precedenti requisiti sono elencati di seguito.
SELECT Nome_studente, Cognome_studente, Studenti.Matricola, Data_di_nascita, Codice_corso, Anno_iscrizione --BUONA
FROM Studenti
JOIN Iscritto_A 
ON Studenti.Matricola = Iscritto_A.Matricola
WHERE Data_di_nascita <= '1997-01-01' AND Codice_corso = 'L-7' AND Anno_iscrizione >= '2026-09-01'

/* Un nuovo bando permette agli studenti di partecipare ad un'esperienza di tirocinio all'estero.
Lo studente che fa domanda deve essere :
- Iscritto a Data Science
- Under 30
- No fuori corso
- Con media sopra il 25
*/
SELECT Nome_studente, Cognome_studente, Studenti.Matricola, Data_di_nascita, Codice_corso, Anno_iscrizione, AVG(Voto) as Media --BUONA
FROM Studenti
JOIN Iscritto_A 
ON Studenti.Matricola = Iscritto_A.Matricola
JOIN Sostiene
ON Studenti.Matricola = Sostiene.Matricola
WHERE Data_di_nascita >= '1996-12-31' AND Codice_corso = 'LM-DATA' AND Anno_iscrizione >= '2024-0-0'
GROUP BY Studenti.Matricola
HAVING Media > 25
