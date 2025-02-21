const fs = require('fs');
const path = require('path');
const Database = require('better-sqlite3');

// Connexion à la base de données SQLite
const db = new Database('base_de_donnees.db');

// Chemin du fichier local sur ton PC
const cheminLocal = 'C:/MesFichiersSTL/modele_local.stl';

// Vérification si le fichier existe
if (fs.existsSync(cheminLocal)) {
    // Récupération des métadonnées
    const nom = path.basename(cheminLocal);        // Nom du fichier
    const taille = fs.statSync(cheminLocal).size;  // Taille en octets
    const description = "Fichier local lié";

    // Insertion dans la base de données
    const stmt = db.prepare(`
        INSERT INTO fichiers_stl (nom, chemin, description, taille) 
        VALUES (?, ?, ?, ?)
    `);
    stmt.run(nom, cheminLocal, description, taille);

    console.log('Fichier local lié à la base de données.');
} else {
    console.log('Fichier introuvable.');
}
