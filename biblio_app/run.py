# appel du package app qui a le fichier __init__.py et views.py
from biblio import app
import os
if __name__ == "__main__":
    # app.run(host='localhost', port=os.environ.get("FLASK_SERVER_PORT"), debug=True)
    app.run(host="localhost", debug=True, port=8081, use_reloader=False)