import numpy as np
import re
import csv
from pgmpy.models import BayesianNetwork
from BAG_Code.createANDtable import create_AND_table
from BAG_Code.createORtable import create_OR_table
from pgmpy.factors.discrete import TabularCPD


def parse_dot(dot_string, ONE):
    """
    Parses a dot string representation of a Bayesian Attack Graph and returns a Bayesian Network object.

    Args:
        dot_string (str): The dot string representation of the Bayesian Attack Graph.
        ONE (float): The value to be used when an event is nearly certain.

    Returns:
        model (BayesianNetwork): The Bayesian Attack Graph object representing the Attack Graph.
        edges (list): A list of tuples representing the edges in the Attack Graph.
        nodes (dict): A dictionary containing information about each node in the Attack Graph.

    """
    nodes = {}
    edges = []

    # Définir une expression régulière pour extraire les informations de chaque nœud
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
            node_id = node_match.group(1)
            label = node_match.group(2)
            shape = node_match.group(3)
            node_type = 'AND' if shape == "ellipse" else 'OR'
            cveID = node_match.group(4).strip("\'")
            nodes[node_id] = {'label': label, 'type': node_type, 'CVE': cveID, 'shape': shape}
        elif edge_match:
            source = edge_match.group(1)
            target = edge_match.group(2)
            edges.append((source, target))
    # We create the Bayesian Network object from the edges
    model = BayesianNetwork(edges)
    # We create the conditional probability tables for each node
    for elem in nodes.items():
        r = elem[1]['type'] == 'OR'
        #We look for the parent nodes and the probability associated to the edge
        parent_nodes = []
        probs = []
        for edge in edges:
            if edge[1] == elem[0]:
                parent_nodes.append(edge[0])
                # We use the probability associated to the rule if not null
                tmp = float(nodes[edge[0]]['label'].split(':')[2])
                if tmp != 0:
                    probs.append(float(tmp))
                else: 
                    probs.append(ONE)
        npa = len(parent_nodes)
        #We draw the probability from the distribution of CVSS scores
        if r:
            cpt = create_OR_table(probs)
        else:
            cpt = create_AND_table(probs)
        # We check if the node is not a root node
        if npa:
            cpd = TabularCPD(elem[0], 2, cpt.T, parent_nodes, evidence_card=2*np.ones(npa))
        else:
            cpd = TabularCPD(elem[0], 2, cpt.T)
        #Insert the conditional probability table into the Bayesian Network object
        model.add_cpds(cpd)
    return model, edges, nodes

def rmv_node(BAG, node):
    """
    Remove a node from the Bayesian Attack Graph (BAG).

    Parameters:
    - BAG (BayesianAttackGraph): The Bayesian Attack Graph object.
    - node (str): The name of the node to be removed.

    Returns:
    None
    """
    edge = [(u,node) for u in BAG.get_parents(node)]
    BAG.remove_edges_from(edge)
    BAG.add_cpds(TabularCPD(node, 2, create_AND_table([0]).T))

def evidences_to_string(evidences):
    """
    Converts a dictionary of evidences to a string representation for naming the simulations.

    Args:
        evidences (dict): A dictionary containing the evidences.

    Returns:
        str: A string representation of the evidences, where each key is preceded by an underscore.

    Example:
        >>> evidences = {'A': True, 'B': False, 'C': True}
        >>> evidences_to_string(evidences)
        '_A_B_C'
    """
    return ''.join([f'_{k}' for k, v in evidences.items()])
