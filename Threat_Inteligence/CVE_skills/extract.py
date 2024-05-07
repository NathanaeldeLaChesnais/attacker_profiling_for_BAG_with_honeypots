import os
import re
import json
import csv

# Liste des IDs de CVE à extraire
liste_cve_ids = ['CVE-2021-1234', 'CVE-2021-5678', 'CVE-2021-9012']

# Chemin du dossier contenant les fichiers CVE
dossier_cves = 'C:\\Users\\docuser\\Documents\\ImperialWork\\Threat_Inteligence\\CVE_skills\\cves'

# Parcours des fichiers du dossier cves
with open('Threat_Inteligence/CVE_skills/donnees.csv', mode='w', newline='') as csv_file:

    for cve in liste_cve_ids:
        decoupage = re.search(r'CVE-(\d+)-(\d+)', cve)
        année = decoupage.group(1)
        id = decoupage.group(2)
        id = id[:-3]
        id = id + "xxx"
        fichier = dossier_cves + "\\" + année + "\\" +  id + "\\" + cve + ".json"
        print(fichier)
        
        with open(fichier, 'r') as f:
            json_data = json.load(f)

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


