from pgmpy.factors.discrete import TabularCPD
from pgmpy.models import BayesianNetwork
from pgmpy.inference import BeliefPropagation
from createANDtable import create_AND_table
from createORtable import create_OR_table
import networkx as nx

bayesian_model = BayesianNetwork([('A', 'B'), ('A', 'C'), ('B', 'D'), ('C', 'D'), ('Imp', 'B'), ('Imp', 'C'), ('PE', 'B'), ('MITM', 'C')])

cpt_a =[[0.1], [0.9]]
cpd_a = TabularCPD('A', 2, [[0], [1]])
cpd_imp = TabularCPD('Imp', 2, cpt_a)
cpd_pe = TabularCPD('PE', 2, [[0], [1]])
cpd_mitm = TabularCPD('MITM', 2, [[0], [1]])
cpt_b = create_AND_table([0.5, 1, 1])
cpd_b = TabularCPD('B', 2, cpt_b.T, ['A', 'PE', 'Imp'], [2, 2, 2])
cpt_c = create_AND_table([0.5, 1, 1])
cpd_c = TabularCPD('C', 2, cpt_c.T, ['A', 'MITM', 'Imp'], [2, 2, 2])
cpt_d = create_OR_table([1, 1])
cpd_d = TabularCPD('D', 2, cpt_d.T, ['B', 'C'], [2, 2])

bayesian_model.add_cpds(cpd_a, cpd_b, cpd_c, cpd_d, cpd_imp, cpd_pe, cpd_mitm)
belief_propagation = BeliefPropagation(bayesian_model)
print(bayesian_model.get_cpds('Imp'))
print(belief_propagation.query(variables=['D'], show_progress=True))

nx.drawing.nx_pydot.write_dot(bayesian_model, 'bayesian_model.dot')