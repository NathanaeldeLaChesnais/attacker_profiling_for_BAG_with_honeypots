import numpy as np
import numpy.random as rn
import matplotlib.pyplot as plt
import networkx as nx
import re
import sys
import os
import csv
from pgmpy.models import BayesianNetwork
from BAG_Code_tw520.createANDtable import create_AND_table
from BAG_Code_tw520.createORtable import create_OR_table
from BAG_Code_tw520.drawRandomCVSS import draw_random_CVSS
from Threat_Inteligence.CWE_tree.parse import parse_xml
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference.ExactInference import BeliefPropagation

rn.seed(1)

def CreateBAG(N, max_edges):
    """
    Create the adjacency matrix (at random, limiting the number of parents per node to max_edges)
    
    # Visualisation purposes
    # i   dif  aux 
    # 2   1   [1]
    # 3   2   [1,2]
    # 4   3   [1,2,3]
    # 5   4   [1,2,3,4]

    params:
    N: Number of nodes in the Bayesian Attack Graph
    max_edges: Maximum number of parents allowed per node in the Bayesian Attack Graph
    """
    
    # Initialise adjacency matrix
    DAG = np.zeros([N, N], dtype=int)

    for i in range(1, N):
        # Randomly decide how many parents the node has 
        parents = rn.randint(1, max_edges+1)
        # Enumerate all of the parent indices 0 to node-1
        aux = np.arange(0,i) 
        # Shuffle parent indices
        rn.shuffle(aux)
        # Take first min(parents, len(aux)) indices to be parents
        ind = aux[:min(parents, len(aux))]
        # Set entries in adjacency matrix
        DAG[ind, i] = 1

    return DAG
    

def plotConnectivityMatrix(A):
    """
    Plots connectivity matrix for BAG.

    params:
    A: Adjacency matrix for BAG
    """

    y, x = np.where(A > 0)
    print(list(zip(y, x)))
    plt.scatter(x, y)
    plt.xlabel('to')
    plt.ylabel('from')
    plt.ylim(N, 0)
    plt.xlim(0, N)
    plt.tight_layout()
    plt.show()

# model.get_random_cpds()
    
def GenerateBAG(N, max_edges):
    """
    Instantiates BAG with CPT values sampled from CVSS scores. 

    params:
    N: Number of nodes in the Bayesian Attack Graph
    max_edges: Maximum number of parents allowed per node in the Bayesian Attack Graph

    returns:
    BAG: Bayesian Network object representing the Bayesian Attack Graph
    """

    # Create DAG
    DAG = CreateBAG(N, max_edges)

    # Names of the nodes (in this case, just the number of the node but can easily be modified)
    nodes = list(range(1, N))
    # plotConnectivityMatrix(DAG)
    s, t = np.where(DAG > 0)
    edges = list(zip(s, t))

    print(edges)

    # Visualise the network
    # G = nx.DiGraph()
    # G.add_nodes_from(nodes)
    # G.add_edges_from(edges)

    # pos = nx.spring_layout(G)
    # nx.draw(G, pos=pos, with_labels=True)
    # plt.show()

    # Initialise Bayesian Network
    model = BayesianNetwork(edges)

    # Create CPDs according to specification 
    # Probability of having AND-type conditional probability tables
    pAND = 0.2 

    for i in range(N):
        npa = np.sum(DAG[:, i])
        r = rn.rand() > pAND
    
        #We draw the probability from the distribution of CVSS scores
        probs = draw_random_CVSS(npa)
        if r:
            cpt = create_OR_table(probs)
        else:
            cpt = create_AND_table(probs)
        
        if npa:
            cpd = TabularCPD(i, 2, cpt.T, evidence=np.where(DAG[:,i])[0], evidence_card=2*np.ones(npa))
        else:
            cpd = TabularCPD(i, 2, cpt.T)

        #Insert the conditional probability table into the Bayesian Network object
        model.add_cpds(cpd)
    
    return model


def ToMarkov(model):
    # Create Markov Network through pgmpy's moralization
    mrf = model.to_markov_model()

    # Create Factor Graph through pgmpy's functions
    factors = mrf.get_factors()
    # print(len(factors))
    for f in factors:
        # # print(f)
        # print(f.variables)
        # print(f.values)
        # print(np.log(f.values))
        # print(f.values.flatten())
        continue

    return mrf

# 5. Check the factors and try to derive relationship between them

# -----------------------------------------------------------------------------
# 6. Begin inference 

import functools
import itertools

import jax
import matplotlib.pyplot as plt
import numpy as np

# Load PGMax
from pgmax import fgraph, fgroup, infer, vgroup, factor
from time import time 
 
# My implementation
    
def CreateFactorGraph(mrf):
    variables = vgroup.VarDict(num_states=2, variable_names=tuple(mrf.nodes))
    fg = fgraph.FactorGraph(variable_groups=[variables])

    for f in mrf.get_factors():
        npa = len(f.variables)
        fact = factor.EnumFactor(
        variables=[variables[i] for i in list(f.variables)],
        factor_configs=np.array(list(itertools.product(np.arange(2), repeat=npa))),
        log_potentials=np.log(f.values.flatten()),
        )
        
        fg.add_factors(fact)

    return fg


def RunLBP(fg, MAP=False):
    if not MAP:
        bp = infer.build_inferer(fg.bp_state, backend="bp")
        start_time=time()
        bp_arrays = bp.run(bp.init(), num_iters=5, damping=0.5, temperature=1.0)
        beliefs = bp.get_beliefs(bp_arrays)
        marginals = infer.get_marginals(beliefs)
        end_time=time()
        # print(marginals)
        print(f'Time for Sum-Product LBP: {end_time-start_time} seconds')
    else: 
        bp = infer.build_inferer(fg.bp_state, backend="bp")
        start_time=time()
        bp_arrays = bp.run(bp.init(), num_iters=5, damping=0.5, temperature=0.0)
        beliefs = bp.get_beliefs(bp_arrays)
        map_states = infer.decode_map_states(beliefs)
        end_time=time()
        # print(map_states)

        print(f'Time for Max-Product LBP: {end_time-start_time} seconds')

    return marginals


def parse_dot(dot_string):
    nodes = {}
    edges = []

    # Définir une expression régulière pour extraire les informations de chaque nœud
    # node_pattern = re.compile("(\d+)")
    node_pattern = re.compile(r'\s+(\d+)\s+\[\s*label="([^"]+)"\s+shape="[^"]+"\s+CVE="([^"]+)"\s*\];')

    # Définir une expression régulière pour extraire les arêtes
    edge_pattern = re.compile(r'\s+(\d+)\s*->\s*(\d+)\s+\[\s+color="[^"]+"\s*\];')

    # Parcourir chaque ligne du texte
    for line in dot_string.split('\n'):
        # Vérifier si la ligne correspond à un nœud
        node_match = node_pattern.match(line)
        # Vérifier si la ligne correspond à une arête
        edge_match = edge_pattern.match(line)
        if node_match:
            node_id = int(node_match.group(1))
            label = node_match.group(2)
            print(label)
            node_type = 'AND' if label == "ellipse" else 'OR'
            cveID = node_match.group(3).strip("\'")
            nodes[node_id] = {'label': label, 'type': node_type, 'CVE': cveID}

        elif edge_match:
            source = int(edge_match.group(1))
            target = int(edge_match.group(2))
            edges.append((source, target))

    model = BayesianNetwork(edges)

    # Read the probabilities for each CVE
    cvss_dict = {}
    with open('C:/Users/docuser/Documents/ImperialWork/Threat_Inteligence/epss_scores-2024-04-25.csv', mode='r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            cvss_dict[row['cve']] = row['epss']
    
    for elem in nodes.items():
        r = elem[1]['type'] == 'OR'
        print(elem)
        print(r)

        #We look for the source nodes
        source = []
        probs = []
        for edge in edges:
            if edge[1] == elem[0]:
                source.append(edge[0])
                if elem[1]['CVE'] == "null":
                    # We use the probability associated to the rule if not null
                    tmp = float(elem[1]['label'].split(':')[2])
                    if tmp != 0:
                        probs.append(float(tmp))
                    else: 
                        probs.append(1)
                else:
                    probs.append(float(cvss_dict[elem[1]['CVE']]))

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


def change_prob(BAG, edges, nodes, src_node, dst_node, inverted_nodes, cwe_dict, Gcwe, prop0, factor):
    for dst_n in dst_node:
        dst_k = inverted_nodes[dst_n]
        dst_cve = nodes[dst_k]['CVE']
        if dst_cve == "null":
            continue
        print(dst_cve)
        dst_cwe = cwe_dict[dst_cve]
        if dst_cwe != 'NVD-CWE-Other' and dst_cwe != "NVD-CWE-noinfo":
            for e in edges:
                if e[1] == dst_k:
                    source = [e[0]]
                    new_prob = BAG.get_cpds(dst_k).values[1][1]
                    for s in src_node:
                        src_k = inverted_nodes[s]
                        src_cve = nodes[src_k]['CVE']
                        if src_cve == "null":
                            continue
                        src_cwe = cwe_dict[src_cve]
                        if src_cwe != 'NVD-CWE-Other' and src_cwe != "NVD-CWE-noinfo":
                            dist = nx.shortest_path_length(Gcwe, source=src_cwe.split('-')[1], target=dst_cwe.split('-')[1])
                            tmp_prob = factor**(dist+1) * prop0.query([src_k]).values[1]
                            new_prob = tmp_prob + new_prob - new_prob*tmp_prob
                    props = create_OR_table([new_prob])
                    BAG.remove_cpds(dst_k)
                    BAG.add_cpds(TabularCPD(dst_k, 2, props.T, source, evidence_card=2*np.ones(1)))