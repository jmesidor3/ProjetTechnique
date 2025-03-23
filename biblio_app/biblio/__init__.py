import datetime
from http.client import HTTPException
import json
import logging
import os
from random import randint
from urllib import response
from biblio.instrument_logging import LogsInstrumentor
from biblio.instrument_metrics import MetricsInstrumentor
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

from flask_wtf.csrf import CSRFProtect
from config import ProductionConfig
import time
from biblio.utilities import AuthorSearchForm, CategoryForm, TitleSearchForm
from flask import render_template, request, jsonify, session, Flask
import requests
from datetime import datetime
# from colorama import Fore, Back, Style
from biblio.instrument_tracing import TracesInstrumentor
# Instrument Flask, SQLAlchemy with OpenTelemetry
from opentelemetry.instrumentation.flask import FlaskInstrumentor

from opentelemetry.instrumentation.requests import RequestsInstrumentor
from prometheus_client import Counter, Histogram, Gauge, Summary


INFO = Gauge('Biblio_app_inprogress_requests', 'Description of gauge',['method', 'endpoint'])    # ce sont les parametres des labels(method=' ', endpoint='/')
REQUESTS= Counter('Biblio_app_requests_total', 'HTTP Failures', ['method', 'endpoint'])
RESPONSES = Counter('Biblio_app_responses_total', 'Description of counter', ['method', 'endpoint'])
REQUESTS_PROCESSING_TIME = Histogram('Biblio_app_requests_duration_seconds', 'Description of histogram', ['method', 'endpoint'])
EXCEPTIONS = Counter('Biblio_app_exceptions_total', 'Description of counter', ['method', 'endpoint'])
REQUESTS_IN_PROGRESS = Gauge('Biblio_app_requests_in_progress', 'Description of gauge', ['method', 'endpoint'])
REQUEST_TIME = Summary('Biblio_app_request_processing_seconds', 'Time spent processing request', ['method', 'endpoint'])



otlp_endpoint = os.environ.get("OTLP_GRPC_ENDPOINT", "http://localhost:4317")
service_name = "biblio-app"
handler = LogsInstrumentor(service_name=service_name)
logging.getLogger(__name__).addHandler(handler)

# Send test message to log
logging.info(f"{service_name} started, listening on port 8082")
  
app = Flask(__name__)
# Instrument metrics
MetricsInstrumentor(app, service_name)
# Attach OTLP handler to root logger


app.config.from_object(ProductionConfig)
Biblio_api_URL=os.environ.get("Biblio_api_URL", "http://biblio_api:8082")

# Initialize CSRF protection, database
# csrf = CSRFProtect(app)


# Instrument tracing
tracer = TracesInstrumentor(app=app, service_name=service_name, otlp_endpoint="tempo:4317", excluded_urls="/metrics")
with app.app_context(): 
    FlaskInstrumentor().instrument_app(app)   
   
    # Instrument database
    RequestsInstrumentor().instrument()    

# Routes and Models import
# from . import routes, models
# Route 1: Affichage de la date du jour avec le libellé Biblio
@INFO.labels(method='index()', endpoint='/').track_inprogress()   # j'ai connu des miseres a comprendre cela
@app.route('/')
def index():
    with INFO.labels(method='index()', endpoint='/').track_inprogress():
        logging.warning(" In index page")
        start_time = datetime.now()   
        try:
            # Start the timer
            # time.sleep(randint(1,10))
            current_time = datetime.now().strftime("%d-%m-%Y")
                      
            # Logging the event
            logging.info(f"Page d'accueil chargée avec la date {current_time}")        
            # Calculate request duration and record it
            duration = (datetime.now() - start_time).total_seconds() 
            INFO.labels(method='index()', endpoint='/').inc()  
            INFO.labels(method='index()', endpoint='/').dec(10)    # Decrement by given value
            INFO.labels(method='index()', endpoint='/').set(4.2)   #     
            return render_template('index.html', date_du_jour=current_time)
        except Exception as e:
            logging.error(f"Erreur lors de l'accès à la page d'accueil : {str(e)}")
            return jsonify({"error": "Erreur interne du serveur"}), 500


# Route 2: Health check - Heure actuelle

@app.route('/heure')
def get_time():
     with REQUEST_TIME.labels(method='/heure', endpoint='/getBookById').time():
        start_time = datetime.now()
    
        try:
            current_time = datetime.now().strftime("%H:%M:%S")       
            # Increment the counter for this request        
            # Calculate request duration and record it
            # time.sleep(randint(1,10))
            duration = (datetime.now() - start_time).total_seconds() 
            REQUEST_TIME.labels(method='/heure', endpoint='/getBookById').observe(duration)       
            logging.info("Heure actuelle récupérée avec succès")
            INFO.labels(method='index()', endpoint='/').inc(15)
            return {"Heure": current_time}
        except Exception as e:
            logging.error(f"Erreur lors de la récupération de l'heure : {str(e)}")
            return jsonify({"error": "Erreur interne du serveur"}), 500


# Route 3: Récupérer un livre par ID
@REQUEST_TIME.labels(method='get_book_by_id(book_id)', endpoint='/getBookById').time()
@app.route('/getBookById/<book_id>', methods=['GET'])
def get_book_by_id(book_id):
    with REQUEST_TIME.labels(method='get_book_by_id(book_id)', endpoint='/getBookById').time():
        try:
            # time.sleep(randint(1,10))
            response = requests.get(f"{Biblio_api_URL}/getBookById/{book_id}")  # Ajout d'ID dans l'URL
            if response.status_code == 200:
                livre = response.json()  # Obtenir les données JSON de la réponse
                REQUEST_TIME.labels(method='get_book_by_id(book_id)', endpoint='/getBookById').observe(4.7) 
                return render_template('book_by_id.html', title='Livre', livre = livre)
            else:
                logging.error(f"Erreur lors de la récupération du livre ID {book_id}: {response.status_code}")
                return jsonify({"error": f"Livre non trouvé avec l'ID {book_id}"}), 404
        except Exception as e:
            logging.error(f"Erreur lors de la récupération du livre ID {book_id}: {str(e)}")
            return jsonify({"error": "Erreur interne du serveur"}), 500
        

# Route 4: Rechercher des livres par titre
@app.route('/getBookByTitle', methods=['GET', 'POST'])
def get_books_by_title():
    form = TitleSearchForm()    
    try:
        if form.validate_on_submit():
            search_title = form.title.data
            response = requests.get(f"{Biblio_api_URL}/getBooksByTitle/{search_title}")
            if response.status_code == 200:
                livres = response.json()  # Récupérer les livres en JSON
                logging.info(f"{len(livres)} livres trouvés pour la recherche de titre '{search_title}'")
                return render_template('books_by_title.html', title='Livres par Titre', form=form, data={'livres': livres})
            else:
                logging.warning(f"Aucun livre trouvé pour le titre '{search_title}'")
                return jsonify({"error": "Aucun livre trouvé"}), 404        
        return render_template('title_search_form.html', title='Rechercher par Titre', form=form)
    except Exception as e:
        logging.error(f"Erreur lors de la recherche de livres par titre : {str(e)}")
        return jsonify({"error": "Erreur interne du serveur"}), 500

    
# Route 6: Rechercher tous les livres 

@app.route('/getAllBooks', methods=['GET'])
def get_all_books():     
    start_time = time.time()    
    REQUESTS.labels('get', '/getAllBooks') # il faut initialiser le label d'abord sinon error
    REQUESTS_PROCESSING_TIME.labels(method='get', endpoint='/getAllBooks')
    EXCEPTIONS.labels(method='get', endpoint='/getAllBooks')
    RESPONSES.labels(method='get', endpoint='/getAllBooks')
    REQUESTS_IN_PROGRESS.labels(method='get', endpoint='/getAllBooks')
    REQUESTS.labels('get', '/getAllBooks').inc()
    try:
        # pour tester 
        # time.sleep(randint(1,10))
        # raise Exception("Livre non trouvé")
        response = requests.get(f"{Biblio_api_URL}/getAllBooks")
        if response.status_code == 200:
            livres = response.json()  # Obtenir les livres en JSON
            logging.info(f"{len(livres)} livres récupérés et affichés avec succès")
            REQUESTS_PROCESSING_TIME.labels('get', '/getAllBooks').observe(time.time() - start_time)
            return render_template('bootstrap_table.html', title='Liste des livres', data={'livres': livres})
        else:
            logging.warning("Aucun livre trouvé")
            return jsonify({"error": "Aucun livre trouvé"}), 404
    except Exception as e:
        logging.error(f"Erreur lors de la récupération de tous les livres - Biblio-app : {str(e)}")
        EXCEPTIONS.labels('get', '/getAllBooks').inc()
        return jsonify({"error": "Erreur interne du serveur"}), 500 
    finally:
        RESPONSES.labels(method='get', endpoint='/getAllBooks').inc()
        REQUESTS_IN_PROGRESS.labels(method='get', endpoint='/getAllBooks').dec()

@REQUESTS.labels(method='get_books_by_author() ', endpoint='/getBookByAuthor').count_exceptions()    
@app.route('/getBookByAuthor', methods=['GET', 'POST'])
def get_books_by_author():
    with REQUESTS.labels(method='get_books_by_author() ', endpoint='/getBookByAuthor').count_exceptions():
        form = AuthorSearchForm()
        try:
            if form.validate_on_submit():
                search_author = form.author.data
                response = requests.get(f"{Biblio_api_URL}/getBooksByAuthor/{search_author}")
                if response.status_code == 200:
                    livres = response.json()  # Récupérer les livres en JSON
                    logging.info(f"{len(livres)} livres trouvés pour la recherche de l'auteur '{search_author}'")
                    return render_template('books_by_author.html', title='Livres par Auteur', form=form, data={'livres': livres})
                else:
                    logging.warning(f"Aucun livre trouvé pour l'auteur '{search_author}'")
                    return jsonify({"error": "Aucun livre trouvé"}), 404        
            return render_template('author_search_form.html', title='Rechercher par Titre', form=form)
        except Exception as e:
            logging.error(f"Erreur lors de la recherche de livres par titre : {str(e)}")
            return jsonify({"error": "Erreur interne du serveur"}), 500
    


@REQUESTS_PROCESSING_TIME.labels(method='get_books_by_category()', endpoint='/getBookByAuthor').time()
@app.route('/getBooksByCategory', methods=['GET', 'POST'])
def get_books_by_category():
    with REQUESTS_PROCESSING_TIME.labels(method='get_books_by_category()', endpoint='/getBookByAuthor').time():
        form = CategoryForm()
        try:
            # Récupérer toutes les catégories pour le formulaire
            categories_response = requests.get(f"{Biblio_api_URL}/getBooksCategories")
            categories = categories_response.json()
            form.categories.choices = [(str(categorie['id']), categorie['nom']) for categorie in categories]
            logging.info(f"{len(categories)} catégories récupérées pour la sélection")
            if form.validate_on_submit():
                selected_category_id = int(form.categories.data)
                # Récupérer les livres par catégorie
                response = requests.get(f"{Biblio_api_URL}/getBooksByCategory/{selected_category_id}")
                if response.status_code == 200:
                    # time.sleep(randint(1,10))
                    livres = response.json()  # Récupérer les livres en JSON
                    logging.info(f"{len(livres)} livres trouvés pour la recherche dans la catégorie ID '{selected_category_id}'")
                    return render_template('books_by_category.html', title='Livres par Catégorie', form=form, data={'livres': livres})
                else:
                    logging.warning(f"Aucun livre trouvé pour la catégorie ID {selected_category_id}")
                    return render_template('books_by_category.html', title='Livres par Catégorie', form=form, data={'livres': []})
            return render_template('category_form.html', title='Sélectionner une Catégorie', form=form)

        except Exception as e:
            logging.error(f"Erreur lors de la récupération des livres par catégorie : {str(e)}")
            return jsonify({"error": "Erreur interne du serveur"}), 500