from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField

# Formulaire pour la sélection de catégorie
class CategoryForm(FlaskForm):
    categories = SelectField('Catégorie', choices=[])

# Formulaire pour la recherche par titre
class TitleSearchForm(FlaskForm):
    title = StringField('Titre à rechercher')
    submit = SubmitField('Rechercher')
    

# Formulaire pour la recherche par auteur
class AuthorSearchForm(FlaskForm):
    author = StringField("Nom de l'auteur à rechercher")
    submit = SubmitField('Rechercher')