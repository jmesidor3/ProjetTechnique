from datetime import datetime
from fastapi import FastAPI, HTTPException, Depends, Response
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
import os
import logging

from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from instrument_logging import LogsInstrumentor
from instrument_tracing import TracesInstrumentor
from instrument_metrics import MetricsInstrumentor
from prometheus_client import Counter, Histogram, Gauge, Summary
import uvicorn
from sqlalchemy.orm import Session
from models import Base
from crud import (
    get_all_books as all_books, 
    get_book_by_id as book_by_id, 
    get_books_by_author as books_by_author, 
    get_books_by_category as books_by_category,
    get_books_by_title as books_by_title,
    getBooksCategories as booksCategories)
from database import SessionLocal, engine

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Flask Front-end origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency pour la session DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

service_name = "biblio-api"
otlp_endpoint = os.environ.get("OTLP_GRPC_ENDPOINT", "http://tempo:4317")

# Instrument tracing
tracer = TracesInstrumentor(app=app, service_name=service_name, otlp_endpoint=otlp_endpoint, excluded_urls="/metrics")

# Instrument logging
handler = LogsInstrumentor(service_name=service_name)
logging.getLogger(__name__).addHandler(handler)

# Send test message to log
logging.info(f"{service_name} started, listening on port 8082")

# Instrument metrics
MetricsInstrumentor(app=app, service_name=service_name)

# Define Prometheus metrics
REQUESTS = Counter('biblio_api_requests_total', 'Total number of requests received')
RESPONSES = Counter('biblio_api_responses_total', 'Total number of responses sent')
EXCEPTIONS = Counter('biblio_api_exceptions_total', 'Total number of exceptions encountered')
REQUESTS_PROCESSING_TIME = Histogram('biblio_api_requests_duration_seconds', 'Time taken to process requests')
REQUESTS_IN_PROGRESS = Gauge('biblio_api_requests_in_progress', 'Number of requests in progress')
REQUEST_TIME = Summary('biblio_api_request_processing_seconds', 'Time spent processing requests')

# Instrument database
SQLAlchemyInstrumentor().instrument(
    engine=engine,
    tracer_provider=tracer,
    enable_commenter=True,
    commenter_options={},
)

# Route 1: Récupérer un livre par ID
@app.get('/getBookById/{book_id}')
def get_book_by_id(book_id, db: Session = Depends(get_db)):
    REQUESTS.inc()
    REQUESTS_IN_PROGRESS.inc()
    start_time = datetime.now()

    with REQUESTS_PROCESSING_TIME.time():
        try:
            livre = book_by_id(book_id, db)
            if livre:
                RESPONSES.inc()
                logging.info(f"Livre ID {book_id} récupéré avec succès")
                return livre
            else:
                logging.warning(f"Livre ID {book_id} non trouvé")
                raise HTTPException(status_code=404, detail="Livre non trouvé")
        except Exception as e:
            EXCEPTIONS.inc()
            logging.error(f"Erreur lors de la récupération du livre ID {book_id} : {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            REQUESTS_IN_PROGRESS.dec()

# Route 2: Rechercher des livres par titre
@app.get('/getBooksByTitle/{search_title}')
def get_books_by_title(search_title, db: Session = Depends(get_db)):
    REQUESTS.inc()
    REQUESTS_IN_PROGRESS.inc()
    start_time = datetime.now()

    with REQUEST_TIME.time():
        try:
            books = books_by_title(search_title, db)
            logging.info(f"{len(books)} livres trouvés pour la recherche de titre '{search_title}'")
            RESPONSES.inc()
            return books
        except Exception as e:
            EXCEPTIONS.inc()
            logging.error(f"Erreur lors de la recherche de livres par titre : {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            REQUESTS_IN_PROGRESS.dec()

# Route 3: Rechercher des livres par auteur
@app.get('/getBooksByAuthor/{search_author}')
def get_books_by_author(search_author, db: Session = Depends(get_db)):
    REQUESTS.inc()
    REQUESTS_IN_PROGRESS.inc()

    with REQUESTS_PROCESSING_TIME.time():
        try:
            books = books_by_author(search_author, db)
            logging.info(f"{len(books)} livres trouvés pour l'auteur '{search_author}'")
            RESPONSES.inc()
            return books
        except Exception as e:
            EXCEPTIONS.inc()
            logging.error(f"Erreur lors de la recherche de livres par auteur : {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            REQUESTS_IN_PROGRESS.dec()

# Route 4: Rechercher tous les livres
@app.get("/getAllBooks")
def get_all_books(db: Session = Depends(get_db)):
    REQUESTS.inc()
    REQUESTS_IN_PROGRESS.inc()

    with REQUESTS_PROCESSING_TIME.time():
        try:
            livres = all_books(db)
            if livres:
                logging.info(f"{len(livres)} livres récupérés et affichés avec succès")
                RESPONSES.inc()
                return livres
            else:
                logging.warning("Aucun livre trouvé.")
                raise HTTPException(status_code=404, detail="Aucun livre trouvé")
        except Exception as e:
            EXCEPTIONS.inc()
            logging.error(f"Erreur lors de la récupération de tous les livres-back-end : {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            REQUESTS_IN_PROGRESS.dec()

# Route 5: Rechercher des livres par catégorie
@app.get('/getBooksByCategory/{selected_category_id}')
def get_books_by_category(selected_category_id, db: Session = Depends(get_db)):
    REQUESTS.inc()
    REQUESTS_IN_PROGRESS.inc()

    with REQUESTS_PROCESSING_TIME.time():
        try:
            books = books_by_category(selected_category_id, db)
            logging.info(f"{len(books)} livres récupérés pour la catégorie ID {selected_category_id}")
            RESPONSES.inc()
            return books
        except Exception as e:
            EXCEPTIONS.inc()
            logging.error(f"Erreur lors de la récupération des livres par catégorie : {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            REQUESTS_IN_PROGRESS.dec()

# Route 6: Rechercher les catégories de livres
@app.get('/getBooksCategories/')
def get_books_categories(db: Session = Depends(get_db)):
    REQUESTS.inc()
    REQUESTS_IN_PROGRESS.inc()

    with REQUESTS_PROCESSING_TIME.time():
        try:
            books = booksCategories(db)
            logging.info(f"{len(books)} catégorie(s) de livres récupérée(s)")
            RESPONSES.inc()
            return books
        except Exception as e:
            EXCEPTIONS.inc()
            logging.error(f"Erreur lors de la récupération des catégories de livres : {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            REQUESTS_IN_PROGRESS.dec()

# Vérification de la connexion à MySQL
try:
    db = SessionLocal()
    db.execute(text('SELECT 1'))
    logging.info('---****** Connexion à MySQL réussie ******')
    print('\n\n---****** Connexion à MySQL réussie ******')
except Exception as e:
    logging.error(f'----------- Connexion échouée ! ERROR : {e}')
    print('\n\n----------- Connexion échouée ! ERROR : ', e)
finally:
    db.close()

if __name__ == "__main__":
    log_config = uvicorn.config.LOGGING_CONFIG
    uvicorn.run(app, host="0.0.0.0", port=8082, log_config=log_config)
