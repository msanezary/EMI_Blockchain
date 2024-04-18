# Projet Blockchain Emi

Ce projet implémente une blockchain simple et un système de preuve de travail (Proof of Work) avec une API Flask pour interagir avec la blockchain via le web.

## Fonctionnalités

- Gestion d'une blockchain avec capacité d'ajouter des blocs après une preuve de travail valide.
- API pour créer des transactions et les ajouter à des blocs.
- Algorithmes de consensus pour résoudre les conflits dans le réseau et maintenir une chaîne cohérente.
- Interface simple pour voir l'état actuel de la blockchain et interagir avec celle-ci.

## Technologies Utilisées

- Python
- Flask
- hashlib pour les fonctions de hachage
- Requests pour la communication réseau

## Installation

Clonez ce dépôt en utilisant :

   ```bash
   git clone https://github.com/msanezary/EMI_Blockchain
   cd EMI_Blockchain
   ```


Installez les dépendances nécessaires :

   ```bash
   pip install -r requirements.txt
   ```

## Démarrage du serveur

Pour lancer le serveur, exécutez :

   ```bash
   python app.py
   ```
Le serveur démarrera localement sur `http://127.0.0.1:5000/`.

## Utilisation de l'API

### Miner un nouveau bloc

   ```bash
   GET /mine
   ```
### Ajouter une nouvelle transaction

   ```bash
   POST /transactions/new
   ```

Données requises:

   ```json
   {
    "sender": "adresse1",
    "recipient": "adresse2",
    "amount": 5
   }
   ```

### Consulter la chaîne complète

   ```bash
   GET /chain
   ```
### Enregistrer un nouveau noeud

   ```bash
   POST /nodes/register
   ```
Données requises:

   ```json
   {
    "nodes": ["http://127.0.0.1:5001"]
   }
   ```

### Résoudre les conflits

   ```bash
   GET /nodes/resolve
   ```
## License


Ce projet est publié sous la licence MIT. Pour plus de détails, consultez le fichier [LICENSE](LICENSE) inclus dans ce dépôt.

