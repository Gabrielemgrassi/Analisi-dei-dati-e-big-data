CREATE TABLE Studenti
(
  Nome_studente VARCHAR(15) NOT NULL,
  Cognome_studente VARCHAR(15) NOT NULL,
  Matricola CHAR(8) NOT NULL,
  Data_di_nascita DATE NOT NULL,
  PRIMARY KEY (Matricola)
);

CREATE TABLE Cdl
(
  Nome_corso VARCHAR(15) NOT NULL,
  Codice_corso VARCHAR(15) NOT NULL,
  PRIMARY KEY (Codice_corso)
);

CREATE TABLE Iscritto_A
(
  Anno_iscrizione DATE NOT NULL,
  Matricola CHAR(8) NOT NULL,
  Codice_corso VARCHAR(15) NOT NULL,
  PRIMARY KEY (Matricola, Codice_corso),
  FOREIGN KEY (Matricola) REFERENCES Studenti(Matricola),
  FOREIGN KEY (Codice_corso) REFERENCES Cdl(Codice_corso)
);

CREATE TABLE Docenti
(
  Codice_docente CHAR(5) NOT NULL,
  Nome_docente VARCHAR(15) NOT NULL,
  Cognome_docente VARCHAR(15) NOT NULL,
  Settore_scientifico VARCHAR(15) NOT NULL,
  Email_istituzionale VARCHAR(30) NOT NULL,
  PRIMARY KEY (Codice_docente)
);

CREATE TABLE Insegnamento
(
  Codice_insegnamento VARCHAR(10) NOT NULL,
  Nome_insegnamento VARCHAR(15) NOT NULL,
  CFU INT NOT NULL,
  Semestre INT NOT NULL,
  Codice_docente CHAR(5) NOT NULL,
  Codice_corso VARCHAR(15) NOT NULL,
  PRIMARY KEY (Codice_insegnamento),
  FOREIGN KEY (Codice_docente) REFERENCES Docenti(Codice_docente),
  FOREIGN KEY (Codice_corso) REFERENCES Cdl(Codice_corso)
);

CREATE TABLE Appello
(
  Data_esame DATE NOT NULL,
  Codice_insegnamento VARCHAR(10) NOT NULL,
  PRIMARY KEY (Data_esame, Codice_insegnamento),
  FOREIGN KEY (Codice_insegnamento) REFERENCES Insegnamento(Codice_insegnamento)
);

CREATE TABLE Sostiene
(
  Voto INT NOT NULL,
  Lode BOOLEAN NOT NULL,
  Matricola CHAR(8) NOT NULL,
  Data_esame DATE NOT NULL,
  Codice_insegnamento VARCHAR(10) NOT NULL,
  PRIMARY KEY (Matricola, Data_esame, Codice_insegnamento),
  FOREIGN KEY (Matricola) REFERENCES Studenti(Matricola),
  FOREIGN KEY (Data_esame, Codice_insegnamento) REFERENCES Appello(Data_esame, Codice_insegnamento)
);