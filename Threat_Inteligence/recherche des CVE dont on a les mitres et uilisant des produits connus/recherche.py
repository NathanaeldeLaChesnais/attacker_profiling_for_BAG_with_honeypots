import csv
import json
import requests

# Remplacez ceci par le chemin de votre fichier CSV
csv_file_path = 'Att&ckToCveMappings.csv'

# Cette fonction vérifie si un CVE concerne un produit Microsoft
def is_microsoft_cve(cve_id):
    url = f'https://nvd.nist.gov/vuln/detail/{cve_id}'
    response = requests.get(url)
    # print(response._content)
    if (response._content.find(b'Microsoft') != -1):
        return True
    return False
    # if response.status_code == 200:
    #     cve_data = response.json()
    #     for vendor_data in cve_data.get('result', {}).get('CVE_Items', []):
    #         for vendor in vendor_data.get('cve', {}).get('affects', {}).get('vendor', {}).get('vendor_data', []):
    #             if vendor.get('vendor_name', '').lower() == 'microsoft':
    #                 return True
    # return False

# Lire le fichier CSV et vérifier chaque CVE
with open(csv_file_path, mode='r', newline='', encoding='utf-8') as csv_file:
    with open('cve_microsoft.csv', mode='w', newline='', encoding='utf-8') as csv_file_microsoft:
        csv_writer = csv.writer(csv_file_microsoft)
        csv_reader = csv.reader(csv_file)
        i = 0
        for row in csv_reader:
            cve_id = row[0]  # Assurez-vous que l'ID CVE est dans la première colonne
            if is_microsoft_cve(cve_id):
                print(f'Le CVE {cve_id} concerne un produit Microsoft.')
                csv_writer.writerow(['cve_id', 'Microsoft'])
            else:
                csv_writer.writerow(['cve_id', 'not microsoft', i])
            i+=1
