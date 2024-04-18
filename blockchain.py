import hashlib
import json
from time import time
from uuid import uuid4
from flask import Flask, jsonify, request
from urllib.parse import urlparse
import requests


class EmiBlockchain(object):
    # On va créer un constructeur qu'on va utiliser pour créer deux listes
    def __init__(self):
        self.chaine = []  # Liste pour stocker la blockchain
        self.transactions = []  # Liste pour stocker les transactions
        self.nouveauBlock(ancienHash=1, proof=100)  # Création du premier block de la blockchain
        self.noeuds=set()

    def enregistrer_noeud(self, address):
        #Ajouter un noeud à la liste des noeuds
        url_analyse=urlparse(address)
        self.noeuds.add(url_analyse.netloc)

    def proof_of_work(self, dernierProof):
        proof = 0
        while self.valid_proof(dernierProof, proof) is False:
            proof += 1
        return proof

    def nouveauBlock(self, proof, ancienHash=None):
        # Cree un nouveau block et il l'ajoute à la blockchain
        block = {'id': len(self.chaine) + 1, 'timestamp': time(), 'transaction': self.transactions, 'proof': proof,
                 'ancienHash': ancienHash}
        self.transactions = []
        self.chaine.append(block)
        return block


    def nouvelleTransaction(self, expediteur, recepteur, montant):
        # Ajoute une nouvelle transaction à la liste des transactions
        self.transactions.append(({'expediteur': expediteur, 'recepteur': recepteur, 'montant': montant}))
        return self.dernierBlock['id']+1

    def chaine_valide(self,chaine):

        dernierBlock=chaine[0]
        indice=1
        while indice<len(chaine):
            block=chaine[indice]
            print(f'{dernierBlock}')
            print(f'{block}')
            print('\n----------------------\n')
            #Valider le hash du block
            if block['ancienHash'] != self.hash(dernierBlock):
                return False

            #vérifier si la proof of work est correcte
            if not self.valid_proof(dernierBlock['proof'], block['proof']):
                return False
            dernierBlock=block
            indice+=1
        return True

    def resoudre_problem(self):
        #cette fonction est utilisée pour choisir la longue chaine
        voisins=self.noeuds
        nouvelle_chaine=None

        #On cherche les chaines les plus longues
        max_longueur=len(self.chaine)
        #Vérifier les chaines du réseau

        for noeud in voisins:
            reponse=requests.get(f'http://{noeud}/chaine')

            if reponse.status_code == 200:
                longueur = reponse.json()['longueur']
                chaine = reponse.json()['chaine']

            #vérifier si la longueur est longue et la chaine est valide
                if longueur> max_longueur and self.chaine_valide(chaine):
                    max_longueur = longueur
                    nouvelle_chaine=chaine
        #remplacer notre chaine si on a trouvé une chaine plus longue
        if nouvelle_chaine:
            self.chaine=nouvelle_chaine
            return True
        return False


    @staticmethod
    def hash(block):
        # Utilisée pour hasher un block
        block_string = json.dumps(block, sort_keys=True).encode()
        #Créer un hash avec SHA256
        return hashlib.sha256(block_string).hexdigest()

    @property
    def dernierBlock(self):
        return self.chaine[-1]

    @staticmethod
    def valid_proof(dernierProof, proof):
        g = f'{dernierProof, proof}'.encode()
        g_hash = hashlib.sha256(g).hexdigest()
        return g_hash[:4] == "0000"


###
##################################################
###

#initialiser le noeud
app = Flask(__name__)

#Créer un identifiant unique pour le noeud
noeud_id = str(uuid4()).replace('-','')

#initialiser la blockchain
emiblockchain = EmiBlockchain()
@app.route('/noeuds/enregistrer', methods=['POST'])
def enregistrer_noeud():
    valeurs = request.get_json()

    noeuds = valeurs.get('noeuds')
    if noeuds is None:
        return "Erreur: Veuillez entrer une liste valide des noeuds", 400

    for noeud in noeuds:
        emiblockchain.enregistrer_noeud(noeud)

    reponse = {
        'message': 'des nouveaux noeuds sont ajoutés',
        'total_noeuds': list(emiblockchain.noeuds),
    }
    return jsonify(reponse), 201


@app.route('/noeuds/resoudre', methods=['GET'])
def consensus():
    remplacer = emiblockchain.resoudre_problem()

    if remplacer:
        reponse = {
            'message': 'Notre chaine est remplacée',
            'new_chain': emiblockchain.chaine
        }
    else:
        reponse = {
            'message': 'notre chaine est autorisé',
            'chain': emiblockchain.chaine
        }

    return jsonify(reponse), 200

@app.route('/miner', methods=['GET'])
def miner():
    dernierBlock = emiblockchain.dernierBlock
    dernierProof = dernierBlock['proof']
    proof = emiblockchain.proof_of_work(dernierProof)

    emiblockchain.nouvelleTransaction(
        expediteur="0",
        recepteur=noeud_id,
        montant=1,
    )

    # Forge the new Block by adding it to the chain
    ancienHash = emiblockchain.hash(dernierBlock)
    block = emiblockchain.nouveauBlock(proof, ancienHash)

    response = {
        'message': "nouveau block miné",
        'id': block['id'],
        'transaction': block['transaction'],
        'proof': block['proof'],
        'ancienHash': block['ancienHash'],
    }
    return jsonify(response), 200

@app.route('/transactions/nouvelle', methods=['POST'])
def nouvelleTransaction():

    valeurs = request.get_json()

    required = ['expediteur', 'recepteur', 'montant']
    if not all(k in valeurs for k in required):
        return 'Valeurs manquées', 400

    # Create a new Transaction
    indice = emiblockchain.nouvelleTransaction(valeurs['expediteur'], valeurs['recepteur'], valeurs['montant'])

    response = {'message': f'Transaction ajoutée au block {indice}'}
    return jsonify(response), 201

@app.route('/chaine', methods=['GET'])
def chainecomplete():
    response = {
        'chaine': emiblockchain.chaine,
        'longueur': len(emiblockchain.chaine),
        }
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)