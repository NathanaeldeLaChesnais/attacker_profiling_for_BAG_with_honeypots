import json
import csv

# Charger le JSON depuis un fichier (remplacez 'chemin/vers/le/fichier.json' par le chemin réel)
with open('Threat_Inteligence/CVE_skills/CVE_all.json') as f:
    data = json.load(f)

# Ouvrir un fichier CSV en mode écriture
with open('Threat_Inteligence/CVE_skills/donnees.csv', mode='w', newline='') as csv_file:
    fieldnames = ['id', 'access complexity']  # Les noms des colonnes dans le fichier CSV
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    writer.writeheader()  # Écrire l'en-tête du fichier CSV

    # Parcourir chaque vulnérabilité dans le JSON
    for vulnerability in data['vulnerabilities']:
        try :
            cve = vulnerability['cve']
            cvss_metrics = cve['metrics']['cvssMetricV2'][0]
            cve_id = cve['id']
            access_complexity = cvss_metrics['cvssData']['accessComplexity']
        except KeyError:
            continue

        # Écrire les données dans le fichier CSV
        writer.writerow({'id': cve_id, 'access complexity': access_complexity})

print("Les données ont été écrites dans le fichier CSV avec succès !")
