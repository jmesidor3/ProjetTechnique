from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from database import Base

# Modèle pour la table Editeur
class Editeur(Base):
    __tablename__ = "editeur"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nom = Column(String(255), nullable=False)    
   

# Modèle pour la table Categorie
class Categorie(Base):
    __tablename__ = "categorie"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nom = Column(String(255), nullable=False) 
   

# Modèle pour la table Auteur
class Auteur(Base):
    __tablename__ = "auteur"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nom = Column(String(255), nullable=False)    
  

# Modèle pour la table Livre
class Livre(Base):
    __tablename__ = "livre"
    id = Column(Integer, primary_key=True)
    titre = Column(String(255), nullable=False)
    description = Column(Text)
    isbn = Column(String(20), nullable=False)
    annee_apparition = Column(Integer)
    image = Column(String(255))   
    id_editeur = Column(Integer, ForeignKey('editeur.id'))
    editeur = relationship('Editeur', backref="livres")  
    categories = relationship('Categorie', secondary='livrecategorie')
    auteurs = relationship('Auteur', secondary='livreauteur')

# Modèle pour la table livreCategorie (table de liaison)
class Livrecategorie(Base):
    __tablename__ = "livrecategorie"
    id_livre = Column(Integer, ForeignKey('livre.id'), primary_key=True)
    id_categorie = Column(Integer, ForeignKey('categorie.id'), primary_key=True)

# Modèle pour la table livreAuteur (table de liaison)
class Livreauteur(Base):
    __tablename__ = "livreauteur"
    id_livre = Column(Integer, ForeignKey('livre.id'), primary_key=True)
    id_auteur = Column(Integer, ForeignKey('auteur.id'), primary_key=True)
