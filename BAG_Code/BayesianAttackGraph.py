import numpy as np
import re
import csv
from pgmpy.models import BayesianNetwork
from BAG_Code_tw520.createANDtable import create_AND_table
from BAG_Code_tw520.createORtable import create_OR_table
from pgmpy.factors.discrete import TabularCPD


def parse_dot(dot_string, ONE):
    nodes = {}
    edges = []

    # Définir une expression régulière pour extraire les informations de chaque nœud
    # node_pattern = re.compile("(\d+)")
    node_pattern = re.compile(r'\s+(\d+)\s+\[\s*label="([^"]+)"\s+shape="([^"]+)"\s+CVE="([^"]+)"\s*\];')

    # Définir une expression régulière pour extraire les arêtes
    edge_pattern = re.compile(r'\s+(\d+)\s*->\s*(\d+)\s+\[\s+color="[^"]+"\s*\];')

    # Parcourir chaque ligne du texte
    for line in dot_string.split('\n'):
        # Vérifier si la ligne correspond à un nœud
        node_match = node_pattern.match(line)
        # Vérifier si la ligne correspond à une arête
        edge_match = edge_pattern.match(line)
        if node_match:
            # node_id = int(node_match.group(1))
            node_id = node_match.group(1)
            label = node_match.group(2)
            shape = node_match.group(3)
            node_type = 'AND' if shape == "ellipse" else 'OR'
            cveID = node_match.group(4).strip("\'")
            nodes[node_id] = {'label': label, 'type': node_type, 'CVE': cveID, 'shape': shape}
        elif edge_match:
            # source = int(edge_match.group(1))
            # target = int(edge_match.group(2))
            source = edge_match.group(1)
            target = edge_match.group(2)
            edges.append((source, target))
    model = BayesianNetwork(edges)
    # Read the probabilities for each CVE
    cvss_dict = {}
    with open('./Threat_Inteligence/epss_scores-2024-04-25.csv', mode='r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            cvss_dict[row['cve']] = row['epss']
    for elem in nodes.items():
        r = elem[1]['type'] == 'OR'
        #We look for the source nodes
        source = []
        probs = []
        for edge in edges:
            if edge[1] == elem[0]:
                source.append(edge[0])
                if elem[1]['CVE'] in cvss_dict.keys():
                    probs.append(float(cvss_dict[elem[1]['CVE']]))
                else:
                    # We use the probability associated to the rule if not null
                    tmp = float(nodes[edge[0]]['label'].split(':')[2])
                    if tmp != 0:
                        probs.append(float(tmp))
                    else: 
                        probs.append(ONE)
        npa = len(source)
        #We draw the probability from the distribution of CVSS scores
        if r:
            cpt = create_OR_table(probs)
        else:
            cpt = create_AND_table(probs)
        if npa:
            cpd = TabularCPD(elem[0], 2, cpt.T, source, evidence_card=2*np.ones(npa))
        else:
            cpd = TabularCPD(elem[0], 2, cpt.T)
        #Insert the conditional probability table into the Bayesian Network object
        model.add_cpds(cpd)
    return model, edges, nodes

def rmv_node(BAG, node):
    edge = [(u,node) for u in BAG.get_parents(node)]
    BAG.remove_edges_from(edge)
    BAG.add_cpds(TabularCPD(node, 2, create_AND_table([0]).T))

def evidences_to_string(evidences):
    return ''.join([f'_{k}' for k, v in evidences.items()])
