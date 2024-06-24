import csv
import re
from pathlib import Path
from BAG_Code_tw520.BayesianAttackGraph import parse_dot, rmv_node, evidences_to_string
from BAG_Code_tw520.createANDtable import create_AND_table
from BAG_Code_tw520.createORtable import create_OR_table
from BAG_Code_tw520.Tools_tree import kts_layer_original
import BAG_Code_tw520.Loopy as Loopy

from pgmpy.inference.ExactInference import BeliefPropagation
from pgmpy.factors.discrete import TabularCPD

# Name of the simulation
simulation = "Big"

# Constante for probability one
ONE = 0.999


def to_dot(BAG, nodes, evidences, path, basename, display_kts=False, calculate_probabilities=False):
    nodes_BAG = BAG.nodes()
    evidences = {str(k): 1 for k in evidences}
    dot = 'digraph G {\nranksep=0.2;\n'
    regex_rule = r"\d+:RULE \d+ \((.*?)\):\d+\.\d+"
    regex_state = r"\d+:(.*?):\d+"
    # Exact inference
    if calculate_probabilities ==1:
        nodes_wo_evidences = [n for n in nodes_BAG.keys() if n not in evidences.keys()]
        nodes_1 = nodes_wo_evidences[:len(nodes_wo_evidences)//3]
        nodes_2 = nodes_wo_evidences[len(nodes_wo_evidences)//3:(len(nodes_wo_evidences)*2)//3]
        nodes_3 = nodes_wo_evidences[(len(nodes_wo_evidences)*2)//3:]
        prop = BeliefPropagation(BAG)
        total_prob1 = prop.query(nodes_1, evidence=evidences)
        total_prob2 = prop.query(nodes_2, evidence=evidences)
        total_prob3 = prop.query(nodes_3, evidence=evidences)
    # Loopy propagation
    if calculate_probabilities == 2:
        marginals = Loopy.RunLBP(Loopy.CreateFactorGraph(Loopy.ToMarkov(BAG)), evidences)
        marginals = list(marginals.values())[0]
    # Return to general case
    honeynodes = [str(n) for n in range(15,52)]
    dynamic_nodes = [str(n) for n in [20, 21,26]]

    def node_to_dot(node):
        prob = 1
        if node not in evidences.keys() and calculate_probabilities == 1:
            # prob = prop.query([node], evidence=evidences).values[1]
            if node in nodes_1:
                prob = total_prob1.marginalize([n for n in nodes_1 if n != node], inplace=False).values[1]
            elif node in nodes_2:
                prob = total_prob2.marginalize([n for n in nodes_2 if n != node], inplace=False).values[1]
            elif node in nodes_3:
                prob = total_prob3.marginalize([n for n in nodes_3 if n != node], inplace=False).values[1]
        elif calculate_probabilities == 2:
            prob = marginals[node][1]
        else:
            prob = 1
        probH = int(prob * 255)
        color = '#' + format(probH, '02X') +''+ format(255-probH, '02X') + '00'
        try:
            CVE = nodes[node]['CVE']
            shape = nodes[node]['shape']
            LABEL = nodes[node]['label']
        except:
            CVE = ''
            shape = ''
            LABEL = ''
        color = 'lightblue' if node in dynamic_nodes else 'blue' if node in honeynodes else color
        prob = "{:.4f}".format(prob)
        if CVE != 'null':
            return f'  \"{node}\" [label=\"{node}\\n{CVE}\\n{prob}\", color=\"{color}\", penwidth=3, shape=\"{shape}\"];\n'
        else:
            rule = re.search(regex_rule, LABEL)
            state = re.search(regex_state, LABEL)
            if rule:
                return f'  \"{node}\" [label=\"{node}\\n{rule.group(1)}\\n{prob}\", color=\"{color}\", penwidth=3, shape=\"{shape}\"];\n'
            elif state:
                return f'  \"{node}\" [label=\"{node}\\n{state.group(1)}\\n{prob}\", color=\"{color}\", penwidth=3, shape=\"{shape}\"];\n'
            else:
                return f'  \"{node}\" [label="{node}\\n{LABEL}\\n{prob}", color="{color}", penwidth=3, shape="{shape}"];\n'
            
    # Display the nodes
    if display_kts:
        for node in BAG.nodes():
            dot += node_to_dot(node)
    else:
        for node in nodes.keys():
            dot += node_to_dot(node)
    # Display the edges 
    for edge in BAG.edges():
        if display_kts or edge[0] in nodes.keys():
            dot += f'  \"{edge[0]}\" -> \"{edge[1]}\";\n'
    dot += '}' # End of the dot file
    # Write the dot file
    with open(path / (basename + evidences_to_string(evidences) + ".dot"), 'w') as f:
        f.write(dot)

        
# Path to the folder containing the tree
path = Path.cwd() / ("Personnal_simulations/output_" + simulation + "/strongly_connected_components/")
file_name = "ag-nocycles.dot"
path_to_dot = path / file_name
basename = "classic"

# We all read from the file, adding probabilities in the same time
BAG, edges, nodes = parse_dot(open(path_to_dot, 'r').read(), ONE)

# This is the reference BAG, before the attacker has compromised any node
BAG_ref = BAG.copy()
prop0 = BeliefPropagation(BAG_ref)

# We create a dictionary to get the node number from the label
inverted_nodes = {int(v['label'].split(':')[0]): k for k, v in nodes.items()}
kts_layer_original(BAG, ONE, nodes)


evidences = [[11]]
import time
for i in range(1, 6):
    timer = time.time()
    BAG_changeant, edges, nodes = parse_dot(open(path / ("ag-nocycles" + str(i) +".dot" ), 'r').read(), ONE)
    kts_layer_original(BAG_changeant, ONE, nodes)
    for evidence in evidences:
        to_dot(BAG_changeant, nodes, evidence, path, basename, display_kts=False, calculate_probabilities=True)
    print("Time for the iteration", i, "and bag:", BAG_changeant, "is ", time.time() - timer)