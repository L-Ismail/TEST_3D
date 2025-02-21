const express = require('express');
const { Pool } = require('pg');
const app = express();

// Configuration de la connexion à PostgreSQL
const pool = new Pool({
    user: 'ton_utilisateur',       // Ton utilisateur PostgreSQL
    host: 'localhost',
    database: 'impression3d',
    password: 'ton_mot_de_passe',  // Ton mot de passe PostgreSQL
    port: 5432
});

// Configuration d'Express et EJS
app.use(express.urlencoded({ extended: true }));
app.use(express.static('public'));
app.set('view engine', 'ejs');

// Page d'accueil
app.get('/', (req, res) => {
    res.render('index');
});

// Page pour afficher les fichiers STL
app.get('/fichiers', async (req, res) => {
    const result = await pool.query('SELECT * FROM fichiers_stl ORDER BY date_ajout DESC');
    res.render('fichiers', { fichiers: result.rows });
});

// Lancer le serveur en local
app.listen(3000, () => {
    console.log('Serveur démarré sur http://localhost:3000');
});
