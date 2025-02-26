#Les librairies que j'ai utilisé:
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
import subprocess

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modèle des objets imprimables
class Objet3D(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    libelle = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    chemin_fichier = db.Column(db.String(200), nullable=False)

# Modèle des paramètres d'un objet 3D:
class Parametre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    objet_id = db.Column(db.Integer, db.ForeignKey('objet3D.id'), nullable=False)
    code_variable = db.Column(db.String(50), nullable=False)
    libelle = db.Column(db.String(100), nullable=False)
    valeur_defaut = db.Column(db.Float, nullable=False)
    min_valeur = db.Column(db.Float, nullable=False)
    max_valeur = db.Column(db.Float, nullable=False)

# Modèle des commandes
class Commande(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_nom = db.Column(db.String(100), nullable=False)
    adresse = db.Column(db.String(200), nullable=False)
    date_commande = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_livraison = db.Column(db.DateTime, nullable=True)
    objet_id = db.Column(db.Integer, db.ForeignKey('objet3D.id'), nullable=False)
    parametres = db.Column(db.Text, nullable=False)  # Stocke les paramètres choisis sous format JSON

# Route principale pour lier l'ensemble et s'y retrouver:
@app.route('/')
def index():
    objets = Objet3D.query.all()
    return render_template('index.html', objets=objets)

# Route pour commander un objet
@app.route('/commande/<int:objet_id>', methods=['GET', 'POST'])
def commander(objet_id):
    objet = Objet3D.query.get_or_404(objet_id)
    parametres = Parametre.query.filter_by(objet_id=objet_id).all()
    
    if request.method == 'POST':
        client_nom = request.form['client_nom']
        adresse = request.form['adresse']
        valeurs_parametres = {param.code_variable: request.form[param.code_variable] for param in parametres}
        
        # Création de la commande
        nouvelle_commande = Commande(
            client_nom=client_nom,
            adresse=adresse,
            objet_id=objet.id,
            parametres=str(valeurs_parametres)
        )
        db.session.add(nouvelle_commande)
        db.session.commit()
        
        # Générer le fichier STL avec OpenSCAD
        chemin_modele = objet.chemin_fichier
        chemin_sortie = f'static/generated/{objet.libelle}.stl'
        
        openscad_code = f"""
        use <{chemin_modele}>;
        scale([1,1,1]) object();
        """
        with open("temp.scad", "w") as f:
            f.write(openscad_code)
        
        subprocess.run(["openscad", "-o", chemin_sortie, "temp.scad"])
        os.remove("temp.scad")
        
        return redirect(url_for('index'))
    
    return render_template('commande.html', objet=objet, parametres=parametres)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
