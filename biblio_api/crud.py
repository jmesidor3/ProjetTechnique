from fastapi import HTTPException
import logging
from sqlalchemy.orm import Session
from models import Auteur, Categorie, Livre

def livre_to_dict(book: Livre):
    """Convertir un objet Livre en dictionnaire pour JSON"""
    return {
        'id': book.id,
        'titre': book.titre,
        'description': book.description,
        'isbn': book.isbn,
        'annee_apparition': book.annee_apparition,
        'image': book.image,
        'editeur': {
            'id': book.editeur.id if book.editeur else None,
            'nom': book.editeur.nom if book.editeur else None
        },
        'categories': [{'id': categorie.id, 'nom': categorie.nom} for categorie in book.categories],
        'auteurs': [{'id': auteur.id, 'nom': auteur.nom} for auteur in book.auteurs]
    }

# Récupérer un livre par son ID avec les détails complets
def get_book_by_id(book_id, db: Session):
    try:
        book = db.query(Livre).filter(Livre.id == book_id).first()
        if book:
            return livre_to_dict(book)
        return None
    except Exception as e:
        logging.error(f"Erreur lors de la récupération d'un livre par son ID : {str(e)}")
        raise HTTPException(status_code=500, detail="Erreur interne du serveur")


# Récupérer les livres par titre
def get_books_by_title(search_title, db: Session):
    try:
        books = db.query(Livre).filter(Livre.titre.ilike(f'%{search_title}%')).all()
        return [livre_to_dict(book) for book in books]
    except Exception as e:
        logging.error(f"Erreur lors de la récupération des livres par titre : {str(e)}")
        raise HTTPException(status_code=500, detail="Erreur interne du serveur")

# Récupérer les livres par auteur (avec jointure)
def get_books_by_author(search_author, db: Session):
    try:
        books = db.query(Livre).join(Livre.auteurs).filter(Auteur.nom.ilike(f'%{search_author}%')).all()
        return [livre_to_dict(book) for book in books]
    except Exception as e:
        logging.error(f"Erreur lors de la récupération des livres par auteur : {str(e)}")
        raise HTTPException(status_code=500, detail="Erreur interne du serveur")

# Récupérer tous les livres avec toutes les relations
def get_all_books(db: Session):
    try:
        books = db.query(Livre).all()
        return [livre_to_dict(book) for book in books]
    except Exception as e:
        logging.error(f"Erreur lors de la récupération des livres : {str(e)}")
        raise HTTPException(status_code=500, detail="Erreur interne du serveur")


# Récupérer les livres par catégorie (avec jointure)
def get_books_by_category(selected_category_id, db: Session):
    try:
        books = db.query(Livre).join(Livre.categories).filter(Categorie.id == selected_category_id).all()
        return [livre_to_dict(book) for book in books]
    except Exception as e:
        logging.error(f"Erreur lors de la récupération des livres par categorie: {str(e)}")
        raise HTTPException(status_code=500, detail="Erreur interne du serveur")
    
def getBooksCategories(db: Session):
    return db.query(Categorie).all()

