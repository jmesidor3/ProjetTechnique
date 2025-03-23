-- Création de la base de données
CREATE DATABASE IF NOT EXISTS gestion_bibliotheque CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Utilisation de la base de données
USE gestion_bibliotheque;

-- Création de la table editeur
CREATE TABLE IF NOT EXISTS editeur (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nom VARCHAR(255) NOT NULL UNIQUE   
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Création de la table categorie
CREATE TABLE IF NOT EXISTS categorie (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nom VARCHAR(255) NOT NULL UNIQUE   
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Création de la table auteur
CREATE TABLE IF NOT EXISTS auteur (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nom VARCHAR(255) NOT NULL UNIQUE     
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Création de la table livre
CREATE TABLE IF NOT EXISTS livre (
    id INT PRIMARY KEY AUTO_INCREMENT,
    titre VARCHAR(255) NOT NULL,
    description TEXT,
    isbn VARCHAR(20) NOT NULL,
    annee_apparition INT,
    image VARCHAR(255),
    id_editeur INT,
    FOREIGN KEY (id_editeur) REFERENCES editeur(id),
    INDEX (id_editeur),
    CONSTRAINT fk_livre_editeur FOREIGN KEY (id_editeur) REFERENCES editeur(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Création de la table livrecategorie
CREATE TABLE IF NOT EXISTS livrecategorie (
    id_livre INT,
    id_categorie INT,
    PRIMARY KEY (id_livre, id_categorie),
    FOREIGN KEY (id_livre) REFERENCES livre(id),
    FOREIGN KEY (id_categorie) REFERENCES categorie(id),
    INDEX (id_categorie, id_livre ),
    CONSTRAINT fk_livrecategorie_livre FOREIGN KEY (id_livre) REFERENCES livre(id) ON DELETE CASCADE,
    CONSTRAINT fk_livrecategorie_categorie FOREIGN KEY (id_categorie) REFERENCES categorie(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Création de la table livreauteur
CREATE TABLE IF NOT EXISTS livreauteur (
    id_livre INT,
    id_auteur INT,
    PRIMARY KEY (id_livre, id_auteur),
    FOREIGN KEY (id_livre) REFERENCES livre(id),
    FOREIGN KEY (id_auteur) REFERENCES auteur(id),
    INDEX (id_auteur, id_livre ),
    CONSTRAINT fk_livreauteur_livre FOREIGN KEY (id_livre) REFERENCES livre(id) ON DELETE CASCADE,
    CONSTRAINT fk_livreauteur_auteur FOREIGN KEY (id_auteur) REFERENCES auteur(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Insertion des données dans la table editeur
    ALTER TABLE editeur AUTO_INCREMENT=1;
    INSERT INTO editeur (nom) VALUES
    ('Addison Wesley'),
    ('O’REILLY'),
    ('Wiley'),
    ('Prentice Hall'),
    ('Cambridge'),
    ('MK'),
    ('The MIT Press'),
    ('Pitman'),
    ('Silicon Press'),
    ('Dunod'),
    ('Hayden Books'),
    ('Computer Science Press'),
    ('McGraw-Hill'),
    ('EYROLLES');

    -- Insertion des données dans la table categorie
    ALTER TABLE categorie AUTO_INCREMENT=1;
    INSERT INTO categorie (nom) VALUES
    ('Programming'),
    ('Programming Languages'),
    ('Web'),
    ('Distributed Systems'),
    ('Operating Systems'),
    ('Databases'),
    ('Data Structures'),
    ('Java'),
    ('C++'),
    ('Algorithms'),
    ('Rust'),
    ('Computer Science'),
    ('Compilers'),
    ('Python'),
    ('C'),
    ('UNIX');

    -- Insertion des données dans la table auteur
    ALTER TABLE auteur AUTO_INCREMENT=1;
    INSERT INTO auteur (nom) VALUES
    ('David Thomas'),
    ('Andrew Hunt'),
    ('Mark Lutz'),
    ('David Gourley'),
    ('Brian Totty'),
    ('Chris Loosley'),
    ('Frank Douglas'),
    ('Andrew S. Tanenbaum'),
    ('Albert S. Woodhull'),
    ('Jean Bacon'),
    ('M. Herlihy'),
    ('V. Luchangco'),
    ('N. Shavit'),
    ('M.Spear'),
    ('Allen B. Downey'),
    ('Thomas A. Standish'),
    ('Frank M.Carrano'),
    ('Janet J. Prichard'),
    ('Peter Brass'),
    ('E. Horowitz'),
    ('S. Sahni'),
    ('Sara Baase'),
    ('Thomas H. Cormen'),
    ('Charles E. Leiserson'),
    ('Ronald L. Rivest'),
    ('Clifford Stein'),
    ('Bjarne Stroustrup'),
    ('Jim Blandy'),
    ('Jason Orendorff'),
    ('Leonora F. S. Tindall'),
    ('Alfred V. Aho'),
    ('Jeffrey D. Ullman'),
    ('Robert Sedgewick'),
    ('Kevin Wayne'),
    ('Ravi Sethi'),
    ('W. Richard Stevens'),
    ('Brian W. Kernighan'),
    ('Dennis M. Ritchie'),
    ('Paul Anderson'),
    ('Gail Anderson'),
    ('Stephen G. Kochan'),
    ('Patrick H. Wood'),
    ('Michel Gabassi'),
    ('Bertrand Dupouy'),
    ('Jean-Marie Rifflet'),
    ('S. Anderson-Freed');

    -- Insertion des données dans la table livre
    ALTER TABLE livre AUTO_INCREMENT=1;
    INSERT INTO livre (titre, description, isbn, annee_apparition, image, id_editeur) VALUES
    ('The Pragmatic Programmer', '', '135957052', '2019', NULL, 1),
    ('Learning Python', '', '978-1-449-35573-9', '2013', NULL, 2),
    ('HTTP The Definitive Guide', '', '978-1-56592-509-0', '2002', NULL, 2),
    ('High-Performance Client/Server', '', '0-471-16269-8', '1998', NULL, 3),
    ('Operating Systems', '', '0-13-638677-6', '1997', NULL, 4),
    ('Concurrent Systems', '', '0-321-11788-3', '2003', NULL, 1),
    ('The Art of Multiprocessor Programming', '', '978-0-12-415950-1', '2121', NULL, 6),
    ('Think Python', '', '978-1-491-93936-9', '2016', NULL, 2),
    ('Data Structures in Java', '', '0-201-30564-X', '1998', NULL, 1),
    ('Data Abstraction and Problem Solving with Java', '', '0-201-70220-7', '2001', NULL, 1),
    ('Advanced Data Structures', '', '978-1-108-73551-3', '2019', NULL, 5),
    ('Fundamentals of Data Structures', '', '0-914894-20X', '1976', NULL, 8),
    ('Computer Algorithms', '', '0-201-06035-3', '1988', NULL, 1),
    ('Algorithms Unlocked', '', '978-0-262-51880-2', '2013', NULL, 7),
    ('Introduction to Algorithms', '', '978-0-262-04630-5', '2022', NULL, 7),
    ('Programming', '', '978-0-321-99278-9', '2014', NULL, 1),
    ('Programming Rust', '', '978-1-492-05259-3', '2021', NULL, 2),
    ('Foundations of Computer Science', '', '0-7167-8233-2', '1992', NULL, 12),
    ('Computer Science', '', '978-0-13-407642-3', '2017', NULL, 1),
    ('Compilers', '', '0-201-10088-6', '1988', NULL, 1),
    ('Advanced Programming in the UNIX Environment', '', '0-201-56317-7', '1999', NULL, 1),
    ('Fundamentals of Data Structures in C', '', '9780-929306-40-7', '2008', NULL, 9),
    ('Le Langage C', '', '978-2-10-071577-0', '2014', NULL, 10),
    ('Advanced C', '', '0-672-48417-X', '1988', NULL, 11),
    ('Topics in C Programming', '', '0-672-46290-7', '1987', NULL, 11),
    ('L’informatique répartie sous Unix', '', '0399-4198', '1992', NULL, 14),
    ('La Communication sous UNIX', '', '2-7042-1240-6', '1990', NULL, 13);
    -- Insérer les associations entre livres et catégories
    INSERT INTO livrecategorie (id_livre, id_categorie) VALUES
    (1, 1), 
    (2, 2),(2,14), 
    (3, 3), 
    (4, 4), 
    (5, 5),
    (6, 5), (6,4),(6,6), 
    (7, 1), 
    (8, 2),(8,14), 
    (9, 7),(9,8),(9,1), 
    (10, 1),(10,7),(10,8),
    (11, 7), 
    (12, 7), 
    (13, 10), 
    (14, 10), 
    (15, 10),
    (16, 1), (16,9),
    (17, 1), (17,2),(17,11), 
    (18, 12), 
    (19, 12), 
    (20, 13),
    (21, 1), (21, 2), (21, 15),(21, 16),
    (22, 7), (22,15), 
    (23, 1), (23, 2), (23, 15), 
    (24, 1), (24, 2), (24, 15), 
    (25, 1), (25, 2), (25, 15),
    (26, 1), (26, 2), (26, 4), (26, 15), (26, 16), 
    (27, 1), (27, 2), (27, 4), (27, 15), (27, 16);

    -- Insérer les associations entre livres et auteurs
    -- (Pour simplifier, je n'ajoute pas de logique pour gérer les auteurs multiples dans la colonne auteurs)
    INSERT INTO livreauteur (id_livre, id_auteur) VALUES
    (1, 1), (1, 2), 
    (2, 3), 
    (3, 4), (3, 5), 
    (4, 7), (4, 6), 
    (5, 9), (5, 8),
    (6, 10), 
    (7, 11), (7, 12), (7, 13), (7, 14), 
    (8, 15), 
    (9, 16),  
    (10, 17), (10, 18), 
    (11, 19),
    (12, 20), (12, 21),
    (13, 22), 
    (14, 23), 
    (15, 23), (15, 24), (15, 25), (15, 26), 
    (16, 27),
    (17, 28), (17, 29), (17, 30), 
    (18, 31), (18, 32),
    (19, 33), (19, 34),
    (20, 31), (20, 35), (20, 32),
    (21, 36),
    (22, 20), (22, 21), (22, 46),
    (23, 37), (23, 38),
    (24, 39), (24, 40),
    (25, 41), (25, 42),
    (26, 43), (26, 44),
    (27, 45);