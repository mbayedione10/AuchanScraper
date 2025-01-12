# Auchan Sénégal Product Scraper

Un outil de scraping web spécialisé pour extraire et analyser les données des produits du site e-commerce d'Auchan Sénégal (auchan.sn). Cette application offre une interface utilisateur conviviale et des capacités avancées de collecte de données.

## Fonctionnalités

- 🔍 Recherche de produits avec filtrage par prix
- 📊 Limitation du nombre de résultats (1-100 produits)
- 💾 Export des données au format Excel compatible Odoo
- 🎨 Interface utilisateur intuitive avec Streamlit
- 🚀 Performance optimisée avec mise en cache des sessions

## Prérequis

- Python 3.11 ou supérieur
- pip (gestionnaire de paquets Python)
- Connexion Internet stable

## Installation

1. Clonez le dépôt :
```bash
git clone <repository-url>
cd auchan-senegal-scraper
```

2. Créez un environnement virtuel (recommandé) :
```bash
python -m venv venv
source venv/bin/activate  # Sur Linux/MacOS
# ou
.\venv\Scripts\activate  # Sur Windows
```

3. Installez les dépendances requises :
Les dépendances principales incluent :
- streamlit
- requests
- beautifulsoup4
- pandas
- openpyxl

## Configuration

1. Vérifiez que le fichier `.streamlit/config.toml` existe avec la configuration suivante :
```toml
[server]
headless = true
address = "0.0.0.0"
port = 5000

[theme]
primaryColor = "#E40019"
secondaryBackgroundColor = "#007A33"
backgroundColor = "#FFFFFF"
textColor = "#000000"
```

## Utilisation

1. Lancez l'application :
```bash
streamlit run main.py
```

2. Accédez à l'interface via votre navigateur à l'adresse : `http://localhost:5000`

3. Dans l'interface :
   - Entrez un terme de recherche (ex: "riz", "huile", "lait")
   - Définissez le nombre maximum de résultats (1-100)
   - Ajustez les filtres de prix si nécessaire
   - Cliquez sur "Rechercher et Scraper"
   - Utilisez le bouton "Exporter (Excel)" pour télécharger les résultats

## Format des Données Exportées

Le fichier Excel exporté contient les colonnes suivantes :
- `name`: Nom du produit
- `default_code`: Code produit unique
- `list_price`: Prix en CFA
- `type`: Type de produit (Biens)
- `categ_id`: Catégorie du produit
- `description_sale`: Description du produit
- `image_1920`: URL de l'image du produit
- Autres métadonnées compatibles Odoo

## Structure du Projet

```
├── main.py           # Point d'entrée de l'application
├── scraper.py        # Logique de scraping
├── data_processor.py # Traitement des données
├── utils.py          # Fonctions utilitaires
└── styles.py         # Personnalisation de l'interface
```

## Dépannage

### Problèmes Courants

1. **L'application ne démarre pas**
   - Vérifiez que le port 5000 n'est pas déjà utilisé
   - Assurez-vous que toutes les dépendances sont installées

2. **Aucun résultat de recherche**
   - Vérifiez votre connexion Internet
   - Essayez avec des termes de recherche différents
   - Vérifiez que les filtres de prix ne sont pas trop restrictifs

3. **Erreur d'exportation Excel**
   - Assurez-vous qu'aucun fichier Excel n'est déjà ouvert
   - Vérifiez les permissions d'écriture dans le dossier

## Contribution

Les contributions sont les bienvenues ! Pour contribuer :

1. Fork le projet
2. Créez une branche pour votre fonctionnalité (`git checkout -b feature/AmazingFeature`)
3. Committez vos changements (`git commit -m 'Add some AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une Pull Request

## Support

Pour toute question ou problème :
- Ouvrez une issue dans le repository
- Consultez la documentation existante
- Contactez l'équipe de maintenance

## Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.