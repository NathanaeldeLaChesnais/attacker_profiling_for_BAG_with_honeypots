import xml.etree.ElementTree as ET
import networkx as nx

def parse_xml(file_path, G):
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Parcourir les éléments du fichier XML
    for cwe in root.findall('.//{http://cwe.mitre.org/cwe-7}Weakness'):
        cwe_id = cwe.get('ID')
        cwe_name = cwe.get('Name')

        # Récupérer les relations parent-enfant
        children_relations = cwe.findall('.//{http://cwe.mitre.org/cwe-7}Related_Weaknesses/{http://cwe.mitre.org/cwe-7}Related_Weakness[@Nature="ParentOf"]')
        children_ids = [child.get('CWE_ID') for child in children_relations] if children_relations else []

        parent_relation = cwe.findall('.//{http://cwe.mitre.org/cwe-7}Related_Weaknesses/{http://cwe.mitre.org/cwe-7}Related_Weakness[@Nature="ChildOf"]')
        parent_id = [parent.get('CWE_ID') for parent in parent_relation] if parent_relation is not None else None
    
        # Afficher les informations de la CWE et ses relations
        for parent in parent_id:
            G.add_edge(parent, cwe_id)
        # print(f"CWE ID: {cwe_id}")
        # print(f"CWE Name: {cwe_name}")
        # print(f"Parent ID: {parent_id}")

# Appeler la fonction de parsing avec le chemin du fichier XML
G = nx.Graph()
parse_xml('1000.xml', G)

distance = nx.shortest_path_length(G, source='295', target='269')
print("Distance between nodes '1004' and '732':", distance)