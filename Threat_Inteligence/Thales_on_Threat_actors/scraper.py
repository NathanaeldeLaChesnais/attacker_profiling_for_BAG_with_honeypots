import requests

# Assurez-vous d'avoir la permission pour télécharger le contenu de ces pages.
def telecharger_page(url):
    try:
        reponse = requests.get(url)
        reponse.raise_for_status()
        return reponse.text
    except requests.HTTPError as http_err:
        print(f'Une erreur HTTP s\'est produite: {http_err}')
    except Exception as err:
        print(f'Une erreur s\'est produite: {err}')

# Fonction pour sauvegarder le contenu dans un fichier
def sauvegarder_contenu(fichier, contenu):
    with open(fichier, 'w', encoding='utf-8') as file:
        file.write(contenu)

# Exemple d'utilisation
if __name__ == "__main__":
    for i in range(627, 676):  # Modifier ici selon les numéros de pages nécessaires
        url = f'https://cds.thalesgroup.com/en/node/{i}'
        contenu_page = telecharger_page(url)
        nom_fichier = f'page_{i}.html'  # Nom du fichier où sauvegarder le contenu
        sauvegarder_contenu(nom_fichier, contenu_page)
        print(f'Contenu de {url} sauvegardé dans {nom_fichier}')
