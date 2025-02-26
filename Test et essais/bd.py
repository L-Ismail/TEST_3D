CREATE DATABASE impression3d
# \c impression3d;

CREATE TABLE fichiers_stl (
    id SERIAL PRIMARY KEY,
    nom TEXT NOT NULL,
    chemin TEXT NOT NULL,
    description TEXT,
    taille INTEGER,
    date_ajout TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
