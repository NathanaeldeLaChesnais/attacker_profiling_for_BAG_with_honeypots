import numpy as np
import numpy.random as rn
import itertools
from pgmax import fgraph, fgroup, infer, vgroup, factor
from time import time
from BAG_Code.BayesianAttackGraph import parse_dot
from pathlib import Path

rn.seed(1)


def ToMarkov(model):
    # Create Markov Network through pgmpy's moralization
    mrf = model.to_markov_model()

    # Create Factor Graph through pgmpy's functions
    factors = mrf.get_factors()
    # print(len(factors))
    for f in factors:
        continue

    return mrf

# TAO implementation
    
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


def RunLBP(fg, evidence, MAP=False):
    if not MAP:
        bp = infer.build_inferer(fg.bp_state, backend="bp")
        variables = fg.variable_groups[0]
        start_time=time()
        bp_arrays = bp.run(bp.init(evidence_updates={variables[n]:np.array([1-v, v]) for n,v in evidence.items() }), num_iters=5, damping=0.5, temperature=1.0)
        beliefs = bp.get_beliefs(bp_arrays)
        marginals = infer.get_marginals(beliefs)
        end_time=time()
        print('marginals', marginals)
        return marginals
        print(f'Time for Sum-Product LBP: {end_time-start_time} seconds')
    else: 
        bp = infer.build_inferer(fg.bp_state, backend="bp")
        start_time=time()
        bp_arrays = bp.run(bp.init(), num_iters=5, damping=0.5, temperature=0.0)
        beliefs = bp.get_beliefs(bp_arrays)
        map_states = infer.decode_map_states(beliefs)
        end_time=time()
        print('map_states', map_states)
        return map_states
        print(f'Time for Max-Product LBP: {end_time-start_time} seconds')

    return end_time-start_time


if __name__ == '__main__':
    # Example usage:
    N = 5
    max_edges = 3

    BAG = parse_dot(open(Path.cwd() / ("Personnal_simulations/output_HighLevel/strongly_connected_components/"), 'r').read(), 0.9999)
    print(BAG)
    MRF = ToMarkov(BAG)
    FG = CreateFactorGraph(MRF)
    
    RunLBP(FG)