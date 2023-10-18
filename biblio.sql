-- Création de la base de données "BibliothequeDB"
CREATE DATABASE Biblio;

-- Utilisation de la base de données
USE Biblio;

-- Création de la table "Auteurs"
CREATE TABLE Auteurs (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    Nom VARCHAR(100),
    Prenom VARCHAR(100)
);

-- Création de la table "Editeurs"
CREATE TABLE Editeurs (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    NomEditeur VARCHAR(100)
);

-- Création de la table "Categories"
CREATE TABLE Categories (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    NomCategorie VARCHAR(50)
);

-- Création de la table "Livres"
CREATE TABLE Livres (
    ISBN VARCHAR(13) PRIMARY KEY,
    Titre VARCHAR(255),
    AuteurID INT,
    AnneePublication INT,
    QuantiteDisponible INT,
    CategorieID INT,
    EditeurID INT,
    FOREIGN KEY (AuteurID) REFERENCES Auteurs(ID),
    FOREIGN KEY (CategorieID) REFERENCES Categories(ID),
    FOREIGN KEY (EditeurID) REFERENCES Editeurs(ID)
);

-- Création de la table "Utilisateurs"
CREATE TABLE Utilisateurs (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    Nom VARCHAR(50),
    Prenom VARCHAR(50),
    Email VARCHAR(100),
    DateInscription DATE
);

-- Création de la table "Emprunts"
CREATE TABLE Emprunts (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    LivreISBN VARCHAR(13),
    UtilisateurID INT,
    DateEmprunt DATE,
    DateRetourPrevu DATE,
    FOREIGN KEY (LivreISBN) REFERENCES Livres(ISBN),
    FOREIGN KEY (UtilisateurID) REFERENCES Utilisateurs(ID)
);

-- Ajout de données dans la table "Auteurs"
INSERT INTO Auteurs (Nom, Prenom)
VALUES
    ('Verne', 'Jules'),
    ('Hugo', 'Victor'),
    ('Camus', 'Albert');

-- Ajout de données dans la table "Categories"
INSERT INTO Categories (NomCategorie)
VALUES
    ('Roman'),
    ('Science-Fiction'),
    ('Poésie');

-- Ajout de données dans la table "Editeurs"
INSERT INTO Editeurs (NomEditeur)
VALUES
    ('Gallimard'),
    ('Folio'),
    ('Le Livre de Poche');

-- Ajout de données dans la table "Livres"
INSERT INTO Livres (ISBN, Titre, AuteurID, AnneePublication, QuantiteDisponible, CategorieID, EditeurID)
VALUES
    ('9782013233707', 'Vingt mille lieues sous les mers', 1, 1870, 10, 2, 1),
    ('9782070408055', 'Les Misérables', 2, 1862, 5, 1, 1),
    ('9782070369561', 'L''Étranger', 3, 1942, 8, 1, 3);

-- Ajout de données dans la table "Utilisateurs"
INSERT INTO Utilisateurs (Nom, Prenom, Email, DateInscription)
VALUES
    ('Dupont', 'Marie', 'marie.dupont@email.com', '2023-01-15'),
    ('Martin', 'Pierre', 'pierre.martin@email.com', '2023-02-20');
