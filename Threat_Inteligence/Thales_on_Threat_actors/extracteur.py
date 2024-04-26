import re
import os

# Fonction pour extraire les données ATK120 du titre
def extraire_atk120(contenu_html):
    motif_atk120 = re.compile(r'<title>([^|]+) \| Cyber Solutions By Thales</title>')
    resultat = motif_atk120.search(contenu_html)
    return resultat.group(1) if resultat else None

# Fonction pour extraire les données Txxxx du texte
def extraire_txxxx(contenu_html):
    motif_txxxx = re.compile(r'<li>(T\d{4}) - .+?</li>')
    return motif_txxxx.findall(contenu_html)

# Exemple d'utilisation
if __name__ == "__main__":
    dossier = os.getcwd()  # Remplacez par le chemin vers le dossier contenant vos fichiers HTML
    print (dossier)
    fichier = 'resultat.csv'
    for fichier_html in os.listdir(dossier):
        if fichier_html.endswith('.html'):
            with open(os.path.join(dossier, fichier_html), 'r', encoding='utf-8') as file:
                contenu_html = file.read()
                atk120 = extraire_atk120(contenu_html)
                txxxx = extraire_txxxx(contenu_html)
                print(f'Dans {fichier_html}: ATK trouvé - {atk120}, Txxxx trouvés - {txxxx}')
                # line = f'{atk120}, {txxxx.replace("[","").replace("]","")}\n'
                line = atk120 +','+ ','.join(txxxx) + '\n'

                with open(fichier, 'a', encoding='utf-8') as file:
                    file.write(line)
