import sqlite3 #Importiamo la libreria sqlite3

#connettiamo python al database già creato e popolato presente sulla memoria del PC
#Potremo farlo inserendo il percorso file all'interno di una stringa, come primo argomento della funzione connect
conn = sqlite3.connect("C:\\Users\\Alessandro\\Desktop\\Database-relazionale_Sistema-universitario\\Sistema-universitario.db")

#creiamo il cursore che ci servirà per eseguire gli statement ed estrarre risultati con fetch
cursor = conn.cursor()

#Definiamo una funzione che ci faciliterà l'utilizzo degli statement
#Automatizzando il processo di recupero (fetch = andare a prendere) e  stampa (print) dei risultati
#Permettendoci anche di dare anche un titolo all' output rendendolo più leggibile
def query(statement, Titolo_risultato):
  A_Capo = '''______________________________________________     

  '''
  cursor.execute(statement
  )
  Righe = cursor.fetchall()
  print(Titolo_risultato + '''
  '''
  )
  for i in Righe:
    print(i)
  print(A_Capo)

#Facciamo partire una query molto semplice
query('''SELECT * FROM Studenti LIMIT 25''', '''LISTA STUDENTI''')

#Ora una più complessa
query('''SELECT Nome_studente, Cognome_studente, Studenti.Matricola, Data_di_nascita, Codice_corso, Anno_iscrizione
FROM Studenti
JOIN Iscritto_A 
ON Studenti.Matricola = Iscritto_A.Matricola
WHERE Data_di_nascita < '1997-0-0' AND Codice_corso = 'L-7' AND Anno_iscrizione >= '2026-0-0' ''',
'''Un nuovo bando, permette a degli studenti di riceve una borsa di studio pari a €2.500.
I requisiti sono quelli di :
- essere uno studente iscritto al primo anno della facolta di Ingegneria civile 
- avere un\' età pari o superiore ad anni 30

Gli studenti che rispettano i precedenti requisiti sono elencati di seguito.''')
#Il risultato dello statement è l' elenco di studenti compatibili con le richieste del bando per la borsa di studio